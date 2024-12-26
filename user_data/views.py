from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import FileResponse, HttpResponse

from my_apps.models import NewEventModelNew, AddExpenseGroup
from checklist.models import Note
from split_the_bills.models import SplitTheBills
from mysite.settings import BASE_DIR, FILES_TO_BACKUP, DATE_TIME_FORMAT

from .password_checker import PasswordChecker

from pathlib import Path
import shutil
import os
from datetime import datetime



# Create your views here.
@login_required(login_url= "my_apps:users_log_in")
def user_data(request: WSGIRequest):
    

    my_notes: QuerySet[Note] = Note.objects.filter(owner = request.user)
    my_events: QuerySet[NewEventModelNew] = NewEventModelNew.objects.filter(owner = request.user).order_by('event_date', 'event_time')
    my_groups: QuerySet[AddExpenseGroup] = SplitTheBills.objects.filter(owner = request.user)

    if 'change_pass' in request.POST:

        pass_check = PasswordChecker(request.POST['new_password1'], request.POST['new_password2'])

        if request.user.check_password(raw_password= request.POST['old_pass']):
            if not pass_check.compare_passwords():
                messages.error(request= request,  message= "Hasła nie są takie same", extra_tags= 'danger')
            
            elif pass_check.too_short():
                messages.error(request= request, message= "Hasło jest za krótkie", extra_tags= 'danger')
            
            elif not pass_check.not_only_numerical():
                messages.error(request= request, message= "Hasło nie może zawierać tylko cyfer", extra_tags= 'danger')
            
            else:
                request.user.set_password(request.POST['new_password1'])
                request.user.save()

                # Utrzymanie sesji po zmianie hasła
                update_session_auth_hash(request, request.user)
                messages.success(request= request, message= "Hasło zostało zmienione", extra_tags= 'success')

        else:
            messages.error(request= request, message= "Nieprawidłowe hasło", extra_tags= 'danger')
    
    if 'delete_account' in request.POST:
        if request.user.check_password(raw_password= request.POST['delete_account']):
            request.user.delete()
            
            messages.error(request= request, message= "Konto zostało usunięte.", extra_tags= 'danger')
            logout(request)
            return redirect(to= "my_apps:homepage")
    
        else:
            messages.error(request= request, message= "Nieprawidłowe hasło", extra_tags= 'danger')

    if request.user.is_superuser:
        backup: Backup = Backup()
        if 'make_backup' in request.POST:
            backup.make_zip()
            # tu mi wstaw cookie

        elif 'delete' in request.POST:
            backup.delete_old_backups()

        elif 'dowloand_backup' in request.POST:
            dowloand = backup.backup_to_dowloand_delete(choosen_backup= request.POST['dowloand_backup'])
            return FileResponse(open(dowloand, 'rb'), as_attachment= True)
        
        elif 'delete_backup' in request.POST:
            backup.backup_to_dowloand_delete(choosen_backup= request.POST['delete_backup'], delete= True)


    response = render(request= request, template_name= 'user_data/user_data.html',
        context= {
            'user': request.user,
            'my_notes': my_notes,
            'my_events': my_events,
            'my_groups': my_groups,
            'backups': backup.show_backups() if request.user.is_superuser else "403"
        }
    )
    # response.set_cookie('gsdgsd', 'gsdgds', max_age= 60, httponly= True, secure = True)
    return response


class Backup:
    def __init__(self):
        self.backup_folder: Path = Path(BASE_DIR, 'db_media_static_backups') 


    def make_zip(self) -> str:
        folder_for_backups: Path = self.backup_folder
        folder_for_backups_temp: Path = Path(folder_for_backups, 'temp')
        zip_name: str = str(folder_for_backups) + '/backup_from_' + datetime.now().strftime(format= DATE_TIME_FORMAT)
        paths: list = [Path(BASE_DIR, path) for path in FILES_TO_BACKUP]

        path_exist: bool = Path.exists(folder_for_backups)
        if not path_exist:
            Path.mkdir(Path(BASE_DIR, folder_for_backups))
            path_exist = True

    
        for folder_file in paths:
            if os.path.isdir(folder_file):
                shutil.copytree(folder_file, Path(folder_for_backups_temp, Path(folder_file).parts[-1]), dirs_exist_ok= path_exist)
            elif os.path.isfile(folder_file):
                shutil.copy(folder_file, folder_for_backups_temp)
        
        archive = shutil.make_archive(zip_name, 'tar', folder_for_backups_temp)
        shutil.rmtree(folder_for_backups_temp)
        return archive


    def delete_old_backups(self) -> None:
        shutil.rmtree(self.backup_folder)


    def show_backups(self) -> list[str]|bool:
        if not Path.exists(self.backup_folder):
            return False
        return os.listdir(path= self.backup_folder)[::-1]


    def backup_to_dowloand_delete(self, choosen_backup: str, delete: bool = False) -> str|None:
        path = str(self.backup_folder) + "/" + choosen_backup
        if delete:
            os.remove(path)
        else:
            return path
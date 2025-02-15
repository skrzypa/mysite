from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponseRedirect, JsonResponse, QueryDict
from django.urls import reverse

from .models import Note, InvitedToNote
from .forms import NewNoteForm, ChangeTitleForm, NewElementForm, ChangeTextForm, ChangeElementForm, ChangeGroupForm, AddToGroupForm, ChangeElementInGroupForm #TitleForm, ElementForm, SubgroupForm, SubgroupElementForm, TextNoteForm
from my_apps.models import Friendship
from mysite.settings import DEBUG


class NoteClass:
    def __init__(self, current_user: WSGIRequest):
        self.current_user: User = User.objects.get(id= current_user.id)
        self.all_notes = Note.objects\
            .filter(owner = current_user.id)\
            .union(Note.objects.filter(invitedtonote__invited_friend = current_user.id))\
            .order_by('-created')
        self.content = {"texts": [], "elements": [], "groups": []}
        self.note_style = "width: 500px; "
        self.note_class = "text-break word-wrap"
        self.friends = [f.to_friend for f in Friendship.objects.filter(from_friend = current_user)]
    

    def add_note(self, title) -> Note:
        new_note: Note = Note(
            owner = self.current_user,
            title = title,
            content = self.content,
        )
        new_note.save()
        return new_note


    def change_title(self, note: Note, new_title: str) -> None:
        note.title = new_title
        note.save()
    

    def delete_note(self, note: Note) -> None:
        # print(note)
        note.delete()
        # print(note.id is None) # True


    def added_and_not_added_to_note(self, note: Note) -> dict:
        added = [f.invited_friend for f in InvitedToNote.objects.filter(note = note)]
        not_added = [f for f in self.friends if f not in added]
        return {
            'added': added,
            'not_added': not_added,
        }
    

    # def add_friends(self, added_friends: list[str], note: Note) -> None:
    #     if self.current_user == note.owner:
    #         added_friends = [User.objects.get(id = f) for f in added_friends]
    #         for f in added_friends:
    #             InvitedToNote(
    #                 note = note,
    #                 invited_friend = f,
    #             ).save()

    def add_friend(self, id: str, note: Note) -> None:
        if self.current_user == note.owner:
            InvitedToNote(note= note, invited_friend= User.objects.get(id= id)).save()
    

    # def del_friends(self, friends_to_del: list[str], note: Note) -> None:
    #     if self.current_user == note.owner:
    #         friends_to_del = [User.objects.get(id = f) for f in friends_to_del]
    #         for f in friends_to_del:
    #             InvitedToNote.objects.get(note = note, invited_friend = f).delete()
    

    def delete_friend(self, id: str, note: Note) -> None:
        if self.current_user == note.owner:
            InvitedToNote.objects.get(note= note, invited_friend= User.objects.get(id= id)).delete()
    

    def add_element(self, note: Note, request: WSGIRequest) -> dict:
        element_form = NewElementForm(request.POST)
        if element_form.is_valid(): 
            form: dict = element_form.cleaned_data
            type_of_element, field_content = form['type_of_element_field'], form['element_field']

            if type_of_element == '1':
                return self._add_text_note(note, field_content, request)

            elif type_of_element == '2': 
                return self._add_element(note, field_content, request)

            elif type_of_element == '3': 
                return self._add_group(note, field_content, request)

    
    def change_text_note_content(self, note: Note, request: WSGIRequest) -> dict:
    
        change_text_form = ChangeTextForm(request.POST)
        note_idx, new_content = change_text_form.data['text_id'], change_text_form.data['change_text_field']
        
        if change_text_form.is_valid():
            note.content['texts'][int(note_idx)] = new_content
            note.save()
            html = self.create_list_of_text_notes(note, request)
            return {'success': True, 'html': html}
        
        return {'blank': True, 'error': change_text_form.errors['change_text_field']}

    
    def change_element_content(self, note: Note, request: WSGIRequest) -> dict:
        change_element_form = ChangeElementForm(request.POST)
        note_idx, new_content = request.POST['text_id'], request.POST['change_element_field']
        if change_element_form.is_valid():
            note.content['elements'][int(note_idx)][0] = new_content
            note.save()
            return {'success_change_element': True, 'html': self.create_list_of_elements(note, request)}
        return {'blank': True, 'error': change_element_form.errors['change_element_field']}
    
    
    def del_text_note(self, note: Note, text_index: str) -> None:
        del note.content['texts'][int(text_index)]
        note.save()

    
    def delete_element(self, note: Note, request: WSGIRequest) -> dict:
        del note.content['elements'][int(request.POST['delete_element'])]
        note.save()
        return {'success_del_element': True, 'html': self.create_list_of_elements(note, request)}

    
    def check_uncheck_element(self, note: Note, element_idx: str, request: WSGIRequest) -> dict:
        element = note.content['elements'][int(element_idx)]
        element[1] = bool(element[1] ^ 1)
        note.save()
        return {'success_element': True, 'html': self.create_list_of_elements(note, request)}


    def create_list_of_friends(self, request: WSGIRequest, note: Note) -> dict:
        added_not_added = self.added_and_not_added_to_note(note)
        return {
            'added': "".join([
                render(
                    request, 
                    'checklist/friend_button.html', 
                    {'friend': user, 'del_add': 'del_friend', 'color': 'danger', 'class': 'del'}
                ).content.decode("utf-8") for user in added_not_added['added']
            ]),

            'not_added': "".join([
                render(
                    request, 
                    'checklist/friend_button.html', 
                    {'friend': user, 'del_add': 'add_friend', 'color': 'success', 'class': 'add'}
                ).content.decode("utf-8") for user in added_not_added['not_added']
            ]),
        }
    

    def create_list_of_text_notes(self, note: Note, request: WSGIRequest) -> str:
        forms: list[ChangeTextForm] = [
            ChangeTextForm(
                initial= {'change_text_field': text}, 
                auto_id= f"change_text_note-{idx}"
            ) 
            for idx, text in enumerate(note.content['texts'], start= 0)
        ]
        
        html = [
            render(
                request, 'checklist/text_note.html', {
                    'form': form, 
                    "index": idx, 
                    'note_id': note.id, 
                    "is_owner": note.owner == self.current_user
                    }
                ).content.decode("utf-8") 
            for idx, form in enumerate(forms, start= 0)
        ]
        return "".join(html)
    

    def create_list_of_elements(self, note: Note, request: WSGIRequest) -> str:
        forms: list[ChangeElementForm, bool] = [
            [
                ChangeElementForm(
                    initial= {'change_element_field': text_bool[0]},
                    auto_id= f"change_element-{idx}"
                ),
                text_bool[1]
            ]
            for idx, text_bool in enumerate(note.content['elements'])
        ]

        html = [
            render(
                request, 'checklist/element.html', {
                    'checked': form[1],
                    'form': form[0], 
                    "index": idx, 
                    'note_id': note.id, 
                    "is_owner": note.owner == self.current_user
                }
            ).content.decode("utf-8") 
            for idx, form in enumerate(forms)
        ]
        return "".join(html)
    

    def create_list_of_groups(self, note: Note, request: WSGIRequest) -> str:
        html: list[ChangeGroupForm, list[ChangeGroupForm, bool]] = []
        for idx_g, group in enumerate(note.content['groups'], start= 0):

            html.append(
                render(
                    request, "checklist/group.html", {
                        'group_form': ChangeGroupForm(
                            initial= {"change_group_field": group[0]},
                            auto_id= f"change_group-{idx_g}",
                        ),
                        "is_owner": note.owner == self.current_user,
                        "idx_g": idx_g,
                        "note_id": note.id, 
                    }
                ).content.decode("utf-8")
            )

            for idx_e, element in enumerate(group[1], start= 0):
                html.append(
                    render(
                        request, "checklist/element_in_group.html", {
                            "element_in_group_form": ChangeElementInGroupForm(
                                initial= {"change_element_in_group_field": element[0]},
                                auto_id= f"change_element_in_group-{idx_g}_{idx_e}"
                            ),
                            "checked": element[1],
                            "idx_g": idx_g,
                            "idx_e": idx_e,
                            "is_owner": note.owner == self.current_user,
                            "note_id": note.id, 
                        }
                    ).content.decode("utf-8")
                )

            html.append(
                render(
                    request, "checklist/add_element_form.html", {
                        'form_field': AddToGroupForm(auto_id= f"add_to_group_field-{idx_g}")['add_to_group_field'],
                        'idx_g': f"{idx_g}",
                    }
                ).content.decode("utf-8")
            )
        
        return "".join(html)
    

    def delete_group(self, note: Note, request: WSGIRequest, id_group: str) -> dict:
        del note.content['groups'][int(id_group)]
        note.save()
        return {'delete_success': True, 'html': self.create_list_of_groups(note, request)}
    

    def change_group_name(self, note: Note, request: WSGIRequest, id_group: str, new_name: str) -> dict:
        form = ChangeGroupForm(request.POST)
        if form.is_valid():
            note.content['groups'][int(id_group)][0] = new_name
            note.save()
            return {'change_group_name': True, 'html': self.create_list_of_groups(note, request)}
        else:
            return {'blank': True, 'error': form.errors['change_group_field'].as_text()}



    def _add_text_note(self, note: Note, field_content: str, request: WSGIRequest) -> dict:
        text_notes: list = note.content['texts']
        text_notes.append(field_content)
        note.save()
        return {'success_notes': True, 'html': self.create_list_of_text_notes(note, request)}


    def _add_element(self, note: Note, field_content: str, request: WSGIRequest) -> None:
        elements: list = note.content['elements']
        elements.append([field_content, False])
        note.save()
        return {'success_elements': True, 'html': self.create_list_of_elements(note, request)}


    def _add_group(self, note: Note, field_content: str, request: WSGIRequest) -> dict:
        groups: list = note.content['groups']
        groups.append([field_content, []])
        note.save()
        return {'success_groups': True, 'html': self.create_list_of_groups(note, request)}


    def add_element_in_group(self, note: Note, field_content: str, group_id: str, request: WSGIRequest) -> dict:
        form = AddToGroupForm(request.POST)
        if form.is_valid():
            note.content['groups'][int(group_id)][1].append([field_content, False])
            note.save()
            return {'add_element_in_group': True, 'html': self.create_list_of_groups(note, request)}
        
        return {'blank': True, 'error': form.errors['add_to_group_field'].as_text()}


    def delete_element_in_group(self, note: Note, request: WSGIRequest) -> dict:
        element_id = [int(e) for e in request.POST['delete_element_in_group'].split("_")]
        del note.content['groups'][element_id[0]][1][element_id[1]]
        note.save()
        return {'del_element_in_group': True, 'html': self.create_list_of_groups(note, request)}


    def check_uncheck_all_group(self, note: Note, request: WSGIRequest) -> dict:
        if 'check_all_group' in request.POST:
            b = True
            group_id = int(request.POST['check_all_group'])
        elif 'uncheck_all_group' in request.POST:
            b = False
            group_id = int(request.POST['uncheck_all_group'])
        
        group = note.content['groups'][group_id][1]
        
        for g, _ in enumerate(group):
            group[g][1] = b
        note.save()

        return {'check_all': True, 'html': self.create_list_of_groups(note, request)}
    

    def check_uncheck_in_group(self, note: Note, request: WSGIRequest) -> dict:
        element_id = [int(i) for i in request.POST['check_uncheck_element_in_group'].split('_')]
        note.content['groups'][element_id[0]][1][element_id[1]][1] = bool(note.content['groups'][element_id[0]][1][element_id[1]][1] ^ 1)
        note.save()
        return {'check_element_in_group': True, 'html': self.create_list_of_groups(note, request)}
    

    def change_element_in_group(self, note: Note, request: WSGIRequest) -> dict:
        form = ChangeElementInGroupForm(request.POST)
        if form.is_valid():
            new_content = request.POST['change_element_in_group_field']
            element_id = [int(i) for i in request.POST['element_id'].split('_')]

            note.content['groups'][element_id[0]][1][element_id[1]][0] = new_content
            note.save()

            return {'change_element_in_group': True, 'html': self.create_list_of_groups(note, request)}
        return {'blank': True, 'error': form.errors['change_element_in_group_field'].as_text()}





# Create your views here.
@login_required(login_url= "my_apps:users_log_in")
def checklist(request: WSGIRequest):
    NC: NoteClass = NoteClass(request.user)
    current_user: User = NC.current_user

    if request.method == "POST" and 'new_note_field' in request.POST:
        return redirect(to= reverse(viewname= 'checklist:note', args= [NC.add_note(request.POST['new_note_field']).id]))

    all_notes = [
            {
                'id': int(note.id),
                'owner': note.owner,
                'title': note.title,
                'content': note.content,
                'created': note.created,
                'color': 'success' if current_user == note.owner else 'danger',
            }
        for note in NC.all_notes
    ]
    

    return render(
        request= request, 
        template_name= 'checklist/checklist.html', 
        context= {
            'all_notes': all_notes,
            'current_user': current_user,
            'current_user_id': current_user.id,

            'new_note_form': NewNoteForm(),
            'note_style': NC.note_style,
            'note_class': NC.note_class,

            'site_name': 'PS | checklist'
        }
    )


@login_required()
def note(request: WSGIRequest, id: int):

    try:
        current_note: Note = Note.objects.get(id= id)
        NC: NoteClass = NoteClass(current_user= request.user)

        added_not_added = NC.added_and_not_added_to_note(current_note)
        friends = NC.create_list_of_friends(request, current_note)
    except ObjectDoesNotExist:
        raise Http404
    

    if request.user != current_note.owner and request.user not in added_not_added['added']:
        raise Http404
    

    if request.method == "POST":
        if DEBUG: print(request.POST)


        if ('delete' in request.POST) and (NC.current_user == current_note.owner):
            Note.objects.get(id= request.POST['delete']).delete()
            return redirect(to= reverse(viewname= "checklist:checklist"))


        if ('change_title_field' in request.POST) and (NC.current_user == current_note.owner):
            change_title_form = ChangeTitleForm(request.POST)
            if change_title_form.is_valid():
                new_title = change_title_form.data['change_title_field']
                NC.change_title(note= current_note, new_title= new_title)
                return JsonResponse({})
            elif change_title_form.data['change_title_field'] == '':
                return JsonResponse(data= {'blank': True, 'error': change_title_form.errors['change_title_field']})


        if ('delete_text_note' in request.POST) and (NC.current_user == current_note.owner):
            NC.del_text_note(current_note, request.POST['delete_text_note'])
            return JsonResponse({'success': True, 'html': NC.create_list_of_text_notes(current_note, request)})
        

        if ("add_friend" in request.POST or "del_friend" in request.POST) and (NC.current_user == current_note.owner):
            if "add_friend" in request.POST:
                NC.add_friend(request.POST['add_friend'], current_note)
            elif "del_friend" in request.POST:
                NC.delete_friend(request.POST['del_friend'], current_note)

            friends_lists = NC.create_list_of_friends(request, current_note)
            return JsonResponse(data= {
                'success': True, 
                'added_friends': friends_lists['added'],
                'not_added_friends': friends_lists['not_added'],
                }
            )


        if ('change_text_field' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.change_text_note_content(current_note, request))
        

        if ('type_of_element_field' in request.POST) and ('element_field' in request.POST):
            return JsonResponse(data= NC.add_element(current_note, request))


        if ('change_element_field' in request.POST) and ('text_id' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.change_element_content(current_note, request))
                

        if ('delete_element' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.delete_element(current_note, request))


        if ('check_uncheck_element_note' in request.POST):
            return JsonResponse(data= NC.check_uncheck_element(current_note, request.POST['check_uncheck_element_note'], request))
        

        if ('delete_group' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.delete_group(current_note, request, request.POST['delete_group']))
        

        if ('change_group_field' in request.POST and 'group_id' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.change_group_name(current_note, request, request.POST['group_id'][0], request.POST['change_group_field']))


        if ('add_to_group_field' in request.POST and 'group_id' in request.POST):
            return JsonResponse(data= NC.add_element_in_group(current_note, request.POST['add_to_group_field'], request.POST['group_id'][0], request))


        if ('delete_element_in_group' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.delete_element_in_group(current_note, request))


        if ("uncheck_all_group" in request.POST) or ("check_all_group" in request.POST):
            return JsonResponse(data= NC.check_uncheck_all_group(current_note, request))


        if ('check_uncheck_element_in_group' in request.POST):
            return JsonResponse(data= NC.check_uncheck_in_group(current_note, request))
        

        if ('change_element_in_group_field' in request.POST) and ('element_id' in request.POST) and (NC.current_user == current_note.owner):
            return JsonResponse(data= NC.change_element_in_group(current_note, request))


        return redirect(to= reverse(viewname= "checklist:note", args= [current_note.id]))






    return render(
        request= request,
        template_name= 'checklist/note.html',
        context= {
            'note': current_note,
            'is_owner': current_note.owner == NC.current_user,

            # 'added_to_note': added_to_note,
            # 'non_added_to_note': non_added_to_note,
            'friends': friends,

            'text_notes': NC.create_list_of_text_notes(current_note, request),
            'elements': NC.create_list_of_elements(current_note, request),
            'groups': NC.create_list_of_groups(current_note, request),

            'change_title_form': ChangeTitleForm,
            'new_element_form': NewElementForm,
            'change_text_form': ChangeTextForm,

            'site_name': f'PS: note | {current_note.title[:11]}'
        }
    )

"""
@login_required
def note(request: WSGIRequest, id: int): 
    current_user = request.user
    current_user_id = current_user.id
    current_user_obj = User.objects.get(id = current_user_id)

    try:
        note: Note = Note.objects.get(id = id)
        is_owner = note.owner == current_user_obj
        invited_to_note: InvitedToNote = InvitedToNote.objects.filter(note = id)
        invited_friends_to_note: list[int] = [int(friend.invited_friend.id) for friend in invited_to_note]
        is_invited = current_user_id in invited_friends_to_note

    except ObjectDoesNotExist:
        raise Http404
    
    except KeyError:
        if not is_owner:
            raise Http404
        
        if note.content == {}:
            note.content = {"elements": [], "groups": [], 'texts': []}
            note.save()

    else:
        if not is_owner and not is_invited:
            raise Http404
    

    friends: Friendship = Friendship.objects.filter(from_friend = current_user_id)
    if friends:
        friends: list[int, str] = [(int(friend.to_friend.id), friend.to_friend.username) for friend in friends]
    

    if request.method == "POST":

        if 'delete' in request.POST and is_owner:
            note.delete()
            return redirect(to= "checklist:checklist")



        elif 'add_text_note' in request.POST:
            key = 'texts'
            note.content[key].append(
                request.POST['add_text_note_field']
            )
            note.save()

        elif 'del_text_note' in request.POST and is_owner:
            index = int(request.POST['del_text_note'])
            del note.content['texts'][index]
            note.save()
        
        elif 'edited_note_index' in request.POST and 'edited_note' in request.POST:
            index = int(request.POST['edited_note_index'])
            note.content['texts'][index] = request.POST['edited_note']
            note.save()
        

    
        elif 'add_element' in request.POST:
            key = 'elements'

            note.content[key].append(
                [f"{request.POST['add_element_field']}", False]
            )
            note.save()
 
        elif 'del_element' in request.POST:
            key = 'elements'
            index = int(request.POST['del_element'])

            del note.content['elements'][index]
            note.save()
 
        elif 'check_element' in request.POST:
            key = 'elements'
            index = int(request.POST['check_element'])

            note.content[key][index][1] = True
            note.save()
 
        elif 'uncheck_element' in request.POST:
            key = 'elements'
            index = int(request.POST['uncheck_element'])

            note.content[key][index][1] = False
            note.save()
 
        elif 'edited_element_index' in request.POST:
            key = 'elements'
            index = int(request.POST['edited_element_index'])

            note.content[key][index][0] = request.POST['edited_element']
            note.save()

           
 
        elif 'add_subgroup' in request.POST:
            key = 'groups'

            note.content[key].append(
                [request.POST['add_subgroup_field'], []]
            )
            note.save()
 
        elif 'edited_subgroup_index' in request.POST:
            key = 'groups'
            index = int(request.POST['edited_subgroup_index'])

            note.content[key][index][0] = request.POST['edited_subgroup']
            note.save()
 
        elif 'del_subgroup' in request.POST:
            key = 'groups'
            index = int(request.POST['del_subgroup'])

            del note.content[key][index]
            note.save()
 
        elif 'add_subgroup_element_index' in request.POST:
            key = 'groups'
            index = int(request.POST['add_subgroup_element_index'])

            new_element = request.POST['add_subgroup_element']
            note.content[key][index][1].append([new_element, False])
            note.save()
 
        elif 'check_subgroup_element' in request.POST:
            key = 'groups'
            index = [int(i) for i in request.POST['check_subgroup_element'].split('-')]


            note.content[key][index[0]][1][index[1]][1] = True
            note.save()
 
        elif 'uncheck_subgroup_element' in request.POST:
            key = 'groups'
            index_subgroup, index_element = [int(i) for i in request.POST['uncheck_subgroup_element'].split('-')]


            note.content[key][index_subgroup][1][index_element][1] = False
            note.save()
 
        elif 'edited_subgroup_element_index' in request.POST:
            key = 'groups'
            index_subgroup, index_element = [int(i) for i in request.POST['edited_subgroup_element_index'].split('_')]

            new_element = request.POST['edited_subgroup']

            note.content[key][index_subgroup][1][index_element][0] = new_element
            note.save()
 
        elif 'del_subgroup_element' in request.POST:
            key = 'groups'
            index_subgroup, index_element = [int(i) for i in request.POST['del_subgroup_element'].split('_')]

            del note.content[key][index_subgroup][1][index_element]
            note.save()
 


        elif 'edit_note_title' in request.POST:
            note.title = request.POST['edited_note_title']
            note.save()


        elif 'share_note' in request.POST and is_owner:
            for f in invited_to_note:
                f: InvitedToNote
                f.delete()

            try:
                checked_friends = [int(id) for id in dict(request.POST)['selected_friends']]
            except KeyError:
                pass
            else:
                for f in checked_friends:
                    InvitedToNote(note = note, invited_friend = User.objects.get(id = f)).save()

        

        elif 'check_all' in request.POST: 
            key = 'groups'
            index = int(request.POST['check_all'])
            group = note.content[key][index]

            for element in group[1]:
                element[1] = True
            note.save()

        elif 'uncheck_all' in request.POST: 
            key = 'groups'
            index = int(request.POST['uncheck_all'])
            group = note.content[key][index]

            for element in group[1]:
                element[1] = False
            note.save()



        return redirect(to= reverse(viewname= "checklist:note", args= [id]))
    

    return render(
        request= request, 
        template_name= 'checklist/note.html', 
        context= {
            'note': note,
            'is_owner': is_owner,
            'element_form': ElementForm,
            'subgroup_form' : SubgroupForm,
            'subgroup_element_form': SubgroupElementForm,
            'text_note_form': TextNoteForm,
            'friends': friends,
            'invited_friends_to_note': invited_friends_to_note,
        }
    )
"""
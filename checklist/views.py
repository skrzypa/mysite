from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Note, InvitedToNote
from .forms import TitleForm, ElementForm, SubgroupForm, SubgroupElementForm, TextNoteForm
from my_apps.models import Friendship

# Create your views here.
@login_required
def checklist(request: WSGIRequest):
    current_user = request.user
    current_user_id = current_user.id
    current_user_obj: User = User.objects.get(id = current_user_id)

    if 'title' in request.POST:
        Note(
            owner = current_user_obj,
            title = request.POST['title']
        ).save()

    all_notes = []
    for note in Note.objects.filter(owner = current_user_id).union(Note.objects.filter(invitedtonote__invited_friend = current_user_id)).order_by('-edited'):
        all_notes.append(
            {
                'id': int(note.id),
                'owner': note.owner,
                'title': note.title,
                'content': note.content,
                'edited': note.edited,
                'color': 'success' if current_user_obj == note.owner else 'danger',
            }
        )

    return render(
        request= request, 
        template_name= 'checklist/checklist.html', 
        context= {
            'all_notes': all_notes,
            'current_user': current_user,
            'current_user_id': current_user_id,

            'title_form': TitleForm,
        }
    )


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
            checked_friends = [int(id) for id in dict(request.POST)['selected_friends']]

            for f in invited_to_note:
                f: InvitedToNote
                f.delete()
            
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
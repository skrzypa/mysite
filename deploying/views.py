from django.shortcuts import render

import mysite.settings

import pathlib
import os

# Create your views here.

def deploying(request):

    path = pathlib.Path(mysite.settings.MEDIA_ROOT, 'deploying')
    if not os.path.exists(path):
        os.mkdir(path)

    
    photos = ["/media/deploying/"+str(x).split('\\')[-1] for x in sorted(path.iterdir(), key= lambda x: int((str(x).split('\\')[-1].split('.')[0])))]
    # print(photos)


    context = {
        'photos': photos,
    }

    return render(request= request, template_name="deploying/deploying.html", context= context)
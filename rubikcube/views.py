from django.shortcuts import render
from .models import Colors

import mysite.settings

import os
import pathlib

# Create your views here.

def rubiccube(request):

    path = pathlib.Path(mysite.settings.MEDIA_ROOT, 'rubikcube')

    if not os.path.exists(path):
        os.mkdir(path)

    colors = Colors.objects.last()

    context = {"chapter_class": f"text-{colors.chapter_text} border border-dark",
               "chapter_style": f"background-color: {colors.chapter_color}; padding: 10px; border-radius: 15px;",

               "content_class": f"text-{colors.content_text} text-start border border-dark fs-4",
               "content_style": f"background-color: {colors.content_color}; padding: 10px; border-radius: 15px;",
               
               "menu_class": f"text-{colors.menu_text} border border-dark",
               "menu_style": f"background-color: {colors.menu_color};",
               "menu_link": f"{colors.menu_text}",

               "alg_div_class": f"container text-center",
               "alg_div_style": f"background-color: {colors.alg_color}; margin-top: 0.5rem; margin-bottom: 0.5rem; padding: 0.5rem; border-radius: 15px;",
               "alg_class": f"h3 text-{colors.alg_text}",
               "alg_style": f"margin: 0; padding: 0;", 

               "link_color": f"{colors.content_text}"
               }

    return render(request= request, template_name= 'rubikcube/rubikcube.html', context= context)
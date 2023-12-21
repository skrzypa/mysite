from django.shortcuts import render

from .models import *

# Create your views here.

def automatictagging(request):



    context = {
        "video_link": DescribeApp.objects.last().video_link
    }

    return render(request= request, template_name= "flac_mp3_tag/flac_mp3_tag.html", context= context) 
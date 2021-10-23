import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from urllib.parse import urlparse
from .models import Url
from .utils import validate_url

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == "POST":
        print("url in request", request.POST)
        url = request.POST['link']
        if not validate_url(url):
            return HttpResponse(status=402)

        uid = str(uuid.uuid4())[:5]
        url_obj = Url(link=url, uuid=uid)
        url_obj.save()

        return HttpResponse(uid)

def go(request, pk):
    try:
        url_obj = Url.objects.get(uuid=pk)
    except:
        return render(request, '404_error.html')
        raise Http404
    link = url_obj.link
    if link.startswith("https://"):
        return redirect(url_obj.link)
    return redirect("https://" + url_obj.link)

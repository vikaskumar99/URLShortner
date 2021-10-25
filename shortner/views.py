import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth import logout
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
        url_obj = Url(link=url, uuid=uid, created_user=request.user)
        url_obj.save()

        return HttpResponse(uid)

def go(request, pk):
    try:
        url_obj = Url.objects.get(uuid=pk)
    except:
        return render(request, '404_error.html')
        raise Http404
    print("\n\n\nrequests", request.META)
    print("clicks is", url_obj.clicks)
    url_obj.clicks += 1
    url_obj.save()
    link = url_obj.link
    if link.startswith("https://"):
        return redirect(url_obj.link)
    return redirect("https://" + url_obj.link)

def logout_request(request):
    print("user details", request.user, request.user.id)
    logout(request)
    return redirect("index")

def show_login_user_links(request):
    try:
        url_obj = Url.objects.filter(created_user=request.user)
    except Exception as e:
        print("error is", e)
        return render(request, '404_error.html')
        raise Http404

    print("links are", url_obj)


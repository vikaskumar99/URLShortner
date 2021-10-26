import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from urllib.parse import urlparse
from .models import Url
from .utils import validate_url
from .forms import CreateUserForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == "POST":
        print("url in request", request.POST)
        url = request.POST['link']
        if not validate_url(url):
            return HttpResponse(status=402)
        try:
            url_obj = Url.objects.filter(link=url, created_user=request.user)
        except:
            pass
        if url_obj:
            url_obj = url_obj[0]
            print("returning existing link", url_obj)
            return HttpResponse(url_obj.uuid)
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

def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Username or Password is incorrect")

    return render(request, "login.html")

def register_user(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get("username")
            messages.success(request, f"Thanks, {name} your account has been created, please login")
            return redirect('login')

    print("\n\n\nentering register user", form)
    context = {"form": form}
    return render(request, "register.html", context)

@login_required(login_url="login")
def show_login_user_links(request):
    try:
        url_obj = Url.objects.filter(created_user=request.user)
    except Exception as e:
        print("error is", e)
        return render(request, '404_error.html')
        raise Http404
    context = {"objects": url_obj}

    print("links are", url_obj)
    return render(request, "dashboard.html", context)

def google(request):
    print("\n\n\n entering google auth\n\n\n")
    return render(request, "404.html")


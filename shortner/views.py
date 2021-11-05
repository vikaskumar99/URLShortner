import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Url
from .utils import validate_url
from .forms import CreateUserForm


def index(request):
    """ Return the homepage """
    return render(request, 'index.html')

def create(request):
    """ Create a short url and return its ID """
    if request.method == "POST":
        print("entering create method")
        url = request.POST['link']
        if not validate_url(url):
            print("returning not valid url status 402")
            return HttpResponse(status=402)
        if request.user.is_authenticated:
            url_obj = Url.objects.filter(link=url, created_user=request.user)
            print("url object search", url_obj)
            if url_obj:
                url_obj = url_obj[0]
                print("URL object of [0]")
                return HttpResponse(url_obj.uuid)
        uid = str(uuid.uuid4())[:5]
        url_obj = Url(link=url, uuid=uid, created_user=request.user)
        url_obj.save()
        print("URL object new create", url_obj)
        return HttpResponse(uid)

def go(request, pk):
    """ When the user visits the short url add a click to that URL and save it"""
    print("entering the go request")
    try:
        url_obj = Url.objects.get(uuid=pk)
    except:
        print("nothing found hence showing 404 error")
        return render(request, '404_error.html')
    url_obj.clicks += 1
    url_obj.save()
    link = url_obj.link
    if link.startswith("https://"):
        return redirect(url_obj.link)
    return redirect("https://" + url_obj.link)

def logout_request(request):
    """ Logout the user """
    logout(request)
    return redirect("index")

def login_user(request):
    """ Login the user and show the home page """
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
    """ Register the user on the platform """
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

    context = {"form": form}
    return render(request, "register.html", context)

@login_required(login_url="login")
def show_login_user_links(request):
    """ Show created URLs of the user """
    try:
        url_obj = Url.objects.filter(created_user=request.user)
    except Exception:
        return render(request, '404_error.html')
    context = {"objects": url_obj}
    return render(request, "dashboard.html", context)



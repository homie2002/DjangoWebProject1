"""
Definition of views.
"""

from datetime import datetime
from importlib.metadata import requires
from urllib.request import Request
from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from django.http import HttpRequest
import speedtest
import uuid
from .models import SpeedTestResult
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required





def home(request):
    download_speed = None
    upload_speed = None
    download_time = None
    upload_time = None
    unique_link = None
    
    if request.method == 'POST':
        file_size = float(request.POST.get('file_size', 0.01))  # Get the file size from the form, default to 0.01 MB
        st = speedtest.Speedtest()
        st.get_best_server()
        
      
        st.download()
        st.upload()
        
        download_speed = st.results.download / 1024 / 1024 
        upload_speed = st.results.upload / 1024 / 1024  

        if download_speed > 0:
            download_time = file_size / download_speed
        else:
            download_time = None

        if upload_speed > 0:
            upload_time = file_size / upload_speed
        else:
            upload_time = None

        
        unique_link = str(uuid.uuid4())
        
       
        result = SpeedTestResult(
            download_speed=download_speed,
            upload_speed=upload_speed,
            unique_link=unique_link
        )
        result.save()
    
    return render(
        request,
        'app/index.html',
        {
            'download_speed': download_speed,
            'upload_speed': upload_speed,
            'download_time': download_time,
            'upload_time': upload_time,
            'unique_link': unique_link,
        }
    )

def speed_test_result(request, unique_link):
    result = get_object_or_404(SpeedTestResult, unique_link=unique_link)
    response = f"Download Speed: {result.download_speed} Mbps<br>Upload Speed: {result.upload_speed} Mbps"
    return HttpResponse(response)

def history(request):
    results = SpeedTestResult.objects.all().order_by('-id')  
    return render(
        request,
        'app/history.html', 
        {'results': results}
    )

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'app/signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'app/signin.html')

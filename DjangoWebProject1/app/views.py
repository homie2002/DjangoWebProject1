"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import speedtest
import uuid
from .models import SpeedTestResult
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


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
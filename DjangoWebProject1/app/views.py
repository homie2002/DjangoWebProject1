"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import speedtest


def home(request):
    download_speed = None
    upload_speed = None
    download_time = None
    upload_time = None
    
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
    
    return render(
        request,
        'app/index.html',
        {
            'download_speed': download_speed,
            'upload_speed': upload_speed,
            'download_time': download_time,
            'upload_time': upload_time,
        }
    )
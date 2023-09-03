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
    
    if request.method == 'POST':
        st = speedtest.Speedtest()
        st.get_best_server()
        
       
        st.download()
        st.upload()
        
        download_speed = st.results.download / 1024 / 1024  # �������� �������� � Mbps
        upload_speed = st.results.upload / 1024 / 1024  # �������� �������� � Mbps

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
        }
    )
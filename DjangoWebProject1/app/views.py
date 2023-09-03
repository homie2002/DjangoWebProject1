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
        
        download_speed = st.results.download / 1024 / 1024  
        upload_speed = st.results.upload / 1024 / 1024  
    
    return render(
        request,
        'app/index.html',
        {
            'download_speed': download_speed,
            'upload_speed': upload_speed,
        }
    )
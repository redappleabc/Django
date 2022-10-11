from urllib import response
from django.shortcuts import render
from apps.hubstaffapihelper import employee_working_data
from django.conf import settings

from datetime import datetime, timedelta

import collections
# Create your views here.



def home(request):
    date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    if "date" in request.GET:
        date = request.GET["date"]
    auth_token = request.session[settings.AUTH_TOKEN]
    context = employee_working_data(auth_token, date)
    return render(request, "home.html", context)


from datetime import datetime, timedelta
from textwrap import indent
from django.conf import settings
from apps.hubstaffapihelper import login, employee_working_data
from django.template.loader import render_to_string


import os, sys, json
from django.core.serializers.json import DjangoJSONEncoder
def send_table_to_manager():
    '''
    A future extension may be for the program to send the table to a manager via email.
    Now I am going to save table to html file
    '''

    email = settings.ADMIN_EMAIL
    password = settings.ADMIN_PASSWORD
    response = login(email, password)

    if response.status_code == 200:
        date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        print(date, ":    login succeed")
        auth_token = response.json()["auth_token"]

        context = employee_working_data(auth_token, date)

        try:
            content = render_to_string('home.html', context)
        except:
            print(date + "   render error")
            print(str(sys.exc_info()[0]))

                   
        with open(os.path.join(os.path.abspath('/code/employeeworking'),  date + '.html'), 'w') as static_file:
            static_file.write(content)
    
    else:
        print(datetime.today(), ":    login failed")
        print(datetime.today(), ":  ", response.text)
    

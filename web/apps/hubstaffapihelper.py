from turtle import end_poly
import requests
from django.conf import settings
from datetime import datetime, timedelta

import collections

def login(email, password):
    login_endpoint = "https://mutator.reef.pl/v67/members/authentication"
    params = {"app_token":settings.APP_TOKEN}
    form_data = {"email":email, "password":password}
    r = requests.post(login_endpoint, params=params, data=form_data)
    return r


def get_organization_id(auth_token):
    endpoint = "https://mutator.reef.pl/v67/company"
    params = {"app_token":settings.APP_TOKEN, "auth_token":auth_token}
    r = requests.get(endpoint, params=params)
    return r


def get_daily_work(organization_id, auth_token, date):
    endpoint = "https://mutator.reef.pl/v67/company/" + str(organization_id) + "/action/by_day"
    params = {"app_token":settings.APP_TOKEN, "auth_token":auth_token, "date[stop]":date}
    headers = {"DateStart":date}
    r = requests.get(endpoint, params=params, headers=headers)
    return r


def get_projectname_from_id(id, auth_token):
    endpoint = "https://mutator.reef.pl/v67/tasks/" + str(id)
    params = {"app_token":settings.APP_TOKEN, "auth_token":auth_token}
    r = requests.get(endpoint, params=params)
    if r.status_code == 200:
        return r.json()["project"]["name"]
    else:
        raise ValueError('You try to access no match the project id')

def get_username_from_id(id, auth_token):

    endpoint = "https://mutator.reef.pl/v67/members/" + str(id)
    params = {"app_token":settings.APP_TOKEN, "auth_token":auth_token}
    r = requests.get(endpoint, params=params)
    if r.status_code == 200:
        return r.json()["user"]["name"]
    else:
        raise ValueError('You try to access no match the user id')


def employee_working_data(auth_token, date):
    msg = None
    data = collections.defaultdict(dict)
    table_data = None
    user_ids = []
    project_ids = []
   
    response = get_organization_id(auth_token)
    
    if response.status_code == 200:

        if len(response.json()["organizations"]) > 0:
            organization_id = response.json()["organizations"][0]["id"]
            response = get_daily_work(organization_id, auth_token, date)

            if response.status_code == 200:
                daily_activities = response.json()["daily_activities"]

                for item in daily_activities:
                    user_ids.append(item["user_id"])
                    project_ids.append(item["project_id"])
                    data[item["user_id"]][item["project_id"]] = timedelta(seconds = item["tracked"])
                
                table_data = [[ get_projectname_from_id(project_id, auth_token) + "(" + str(project_id) + ")"] + [data[user_id][project_id] if project_id in data[user_id] else 0 for user_id in user_ids] for project_id in project_ids]
                user_ids = [get_username_from_id(user_id, auth_token) + "(" + str(user_id) + ")" for user_id in user_ids]

            else:
                msg = "Unexpected error"
        else:
            msg = "You don't have organizations"
    else:
        msg = "Unexpected error"

    context = {"msg":msg, "table_data":table_data, "table_header": user_ids, "date":date}
    return context
    



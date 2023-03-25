import json
import requests
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import HttpResponse
import io
from io import BytesIO
import openpyxl
import pytesseract
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime
import pandas as pd
from django.shortcuts import render
import math
from PIL import Image

# url = 'http://192.168.68.126:8000/'


url = 'https://makemymenu.app'


# url = 'http://192.168.50.126:6000'


# Landing views here
def landing(request):
    return render(request, 'auth/signin.html')


def conditions(request):
    return render(request, 'auth/conditions.html')


def privacy(request):
    return render(request, 'auth/privacy.html')


def combo_details(request, combo_id, bid):
    error = request.GET.get('error')
    try:
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
    except:
        return HttpResponseRedirect('/sign-in/')
    combo_list = requests.get(url + '/group/api/' + combo_id + '/', headers=header).json()
    new_item_list = requests.get(url + '/item/api/', headers=header).json()
    item_list = new_item_list
    localization_info = requests.get(url + '/branch/zone/' + bid + '/', headers=header).json()
    if request.method == "POST":
        name = request.POST['item_name_update']
        status_selected = request.POST.get('item_status')
        price = request.POST['item_price_update']
        discount = request.POST['item_rate_update']
        description = request.POST['item_description_update']
        category = request.POST['item_category_update']
        payload = {'name': name, 'price': price,
                   'description': description, 'category': category, 'status': status_selected, 'discount': discount}
        try:
            combo_vid = request.POST['combo_video_update']
            if combo_vid == '':
                payload["video_link"] = ""
        except:
            combo_vid = ''
            payload["video_link"] = combo_vid
        if combo_vid != '':
            if "youtu.be" in combo_vid:
                combo_vid_code = combo_vid.split('/')[-1]
            elif "www.youtube.com/watch" in combo_vid:
                combo_vid_code = combo_vid.split('v=')[1].split('&')[0]
            elif "www.youtube.com/embed" in combo_vid:
                combo_vid_code = combo_vid.split('embed/')[1].split('"')[0]
            else:
                combo_vid_code = ''
                error = 'Invalid youtube link'
                return HttpResponseRedirect('/dashboard/?error=' + error)
            if combo_vid_code != '':
                combo_vid = "https://www.youtube.com/embed/" + combo_vid_code
                payload["video_link"] = combo_vid
        try:
            image = request.FILES['combo_image_upload_update']
            # file = [('image', image)]
            buffer = convert_to_OneToOne_ratio(image, 1)
            file = InMemoryUploadedFile(
                buffer, None, "image.png", "image/png",
                buffer.tell(), None
            )
            response = requests.patch(url + '/group/api/' + combo_id + '/', headers=header, data=payload,
                                      files={'image': file})
        except:
            image = ""
            response = requests.patch(url + '/group/api/' + combo_id + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/')
        else:
            error = "Combo Update failed"
            return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/?error=' + error)
    return render(request, 'items/combo_details.html',
                  {'combo_list': combo_list, 'new_item_list': item_list, 'localization_info': localization_info,
                   'bid': bid})


def combo_details_delete(request, combo_id, bid):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Content-Type': 'application/json', 'Authorization': key}
    combo_item = requests.get(url + '/group/api/' + combo_id + '/', headers=header).json()
    combo_item_list = combo_item["item"]
    combo_item_new_list = []
    for item_obj in combo_item_list:
        combo_item_new_list.append(str(item_obj["id"]))
    error = ""
    if request.method == "POST":
        item = request.POST.getlist('combo_items_checkbox')
        for i in item:
            try:
                combo_item_new_list.remove(i)
            except:
                print("not removed")
        payload = {'item': combo_item_new_list}
        payload = json.dumps(payload)
        response = requests.patch(url + '/group/api/' + combo_id + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/')
        else:
            error = "Item delete unsuccessful"
            return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/?error=' + error)


def combo_details_update(request, combo_id, bid):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Content-Type': 'application/json', 'Authorization': key}
    combo_item = requests.get(url + '/group/api/' + combo_id + '/', headers=header).json()
    combo_item_list = combo_item["item"]
    combo_item_new_list = []
    for item_obj in combo_item_list:
        combo_item_new_list.append(str(item_obj["id"]))
    error = ""
    if request.method == "POST":
        item = request.POST.getlist('combo_items_checkbox')
        combo_item_new_list = combo_item_new_list + item
        payload = {'item': combo_item_new_list}
        payload = json.dumps(payload)
        response = requests.patch(url + '/group/api/' + combo_id + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/')
        else:
            error = "Item delete unsuccessful"
            return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/?error=' + error)


def item_image_remove(request, item_id, bid):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Authorization': key}
    empty_file = io.BytesIO()
    response = requests.patch(url + '/item/api/' + item_id + '/', headers=header, files={'image': ('', empty_file)})
    if response.status_code == 200:
        return HttpResponseRedirect('/items/' + item_id + '/' + bid + '/')
    else:
        error = "Item image delete unsuccessful"
        return HttpResponseRedirect('/items/' + item_id + '/' + bid + '/?error=' + error)


def combo_image_remove(request, combo_id, bid):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Authorization': key}
    empty_file = io.BytesIO()
    response = requests.patch(url + '/group/api/' + combo_id + '/', headers=header, files={'image': ('', empty_file)})
    if response.status_code == 200:
        return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/')
    else:
        error = "Group image delete unsuccessful"
    return HttpResponseRedirect('/combo-details/' + combo_id + '/' + bid + '/?error=' + error)


def get_stat(request):
    header = {'Content-Type': 'application/json'}
    stat_type = request.GET.get('stat_type')
    company_info = request.GET.get('company_id')
    data_1 = int(stat_type)
    data_2 = int(company_info)
    payload = {"stat_type": data_1, "company_id": data_2}
    payload = json.dumps(payload)
    response = requests.post(url + '/menu/stats/', headers=header, data=payload)
    data = json.loads(response.text)
    # data = {
    #     "msg": "Stat data for 1",
    #     "month": {
    #         "2": 58,
    #         "3": 28
    #     },
    #     "day": {
    #         "2023-03-04": 81,
    #         "2023-03-03": 28,
    #         "2023-03-02": 18,
    #         "2023-03-01": 48,
    #         "2023-02-31": 38,
    #     }
    # }
    return JsonResponse(data)


# Signin views here
def sign_in(request):
    error = request.GET.get('error')
    if request.method == 'POST':
        header = {'Content-Type': 'application/json'}
        email = request.POST['signIn_email']
        password = request.POST['signIn_password']
        payload = {'email': email, 'password': password}
        payload = json.dumps(payload)
        response = requests.post(
            url + '/user/login/', data=payload, headers=header)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            session_key = response_dict['Token']
            request.session['key'] = session_key
            return HttpResponseRedirect('/dashboard/')
        else:
            sign_up_completion = requests.get(url + '/user/info/?email=' + email, headers=header)
            sign_up_completion_dict = json.loads(sign_up_completion.text)
            try:
                verified_status = sign_up_completion_dict[0]['verified']
            except:
                verified_status = True
                print(sign_up_completion_dict)
            if not verified_status:
                return HttpResponseRedirect('/verify/?email=' + email)
            error = response.text
            return HttpResponseRedirect('/sign-in/?error=' + error)
    return render(request, 'auth/signin.html')


# Signup views here
def sign_up(request):
    error = request.GET.get('error')
    if request.method == "POST":
        header = {'Content-Type': 'application/json'}
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['signUp_email']
        # phone = request.POST['phone-number']
        password = request.POST['signUp_password']
        payload = {'email': email, 'first_name': first_name,
                   'last_name': last_name, 'password': password}
        payload = json.dumps(payload)
        response = requests.post(url + '/user/api/', data=payload, headers=header)
        if response.status_code == 201:
            return HttpResponseRedirect('/verify/?email=' + email)
        else:
            error_obj = json.loads(response.text)
            error = ""
            if error_obj["email"]:
                error = "User with this email already existed"
                return HttpResponseRedirect('/sign-up/?error=' + error)
    return render(request, 'auth/signup.html')


def resend(request):
    user_email = request.GET.get('email')
    header = {'Content-Type': 'application/json'}
    payload = {'email': user_email}
    requests.get(url + '/user/register-verify/', params=payload, headers=header).json()
    return HttpResponseRedirect('/verify/?email=' + user_email)


# verify views here
def verify(request):
    user_email = request.GET.get('email')
    if request.method == "POST":
        header = {'Content-Type': 'application/json'}
        token_1 = request.POST['token1']
        token_2 = request.POST['token2']
        token_3 = request.POST['token3']
        token_4 = request.POST['token4']
        token_5 = request.POST['token5']
        token_6 = request.POST['token6']
        token = int(token_1 + token_2 + token_3 + token_4 + token_5 + token_6)
        payload = {'token': token, 'email': user_email}
        payload = json.dumps(payload)
        response = requests.post(url + '/user/register-verify/', data=payload, headers=header)
        if response.status_code == 202:
            response_dict = json.loads(response.text)
            session_key = response_dict['Token']
            request.session['key'] = session_key
            return HttpResponseRedirect('/create-company/')
            # payload = {'name': 'My Company', 'email': user_email,
            #            'address': 'My company address'}
            # key = "Token " + session_key
            # header = {'Content-Type': 'application/json', 'Authorization': key}
            # payload = json.dumps(payload)
            # create_test_company = requests.post(url + '/company/api/', data=payload, headers=header)
            # if create_test_company.status_code == 201:
            #     response = requests.post(url + '/branch/api/', headers=header)
            #     if response.status_code == 201:
            #         response = requests.post(url + '/subscription/api/', headers=header)
            #         return HttpResponseRedirect('/dashboard/')
            # sign_up_completion = requests.get(url + '/user/info/?email=' + user_email, headers=header)
            # sign_up_completion_dict = json.loads(sign_up_completion.text)
            # company_status = sign_up_completion_dict[2]['has_company']
            # branch_status = sign_up_completion_dict[3]['has_branch']
            # branch_subscription = sign_up_completion_dict[4]['has_subscription']
            # if company_status:
            #     if branch_subscription:
            #         if branch_status:
            #             return HttpResponseRedirect('/dashboard/')
            #         else:
            #             return HttpResponseRedirect('/create-branch/')
            #     else:
            #         return HttpResponseRedirect('/plans/')
            # else:
            #     return HttpResponseRedirect('/create-company/')
        else:
            error = json.loads(response.text)
            return render(request, 'auth/verify.html', {'error': error, 'user_email': user_email})
    return render(request, 'auth/verify.html', {'user_email': user_email})


# plans views here
def plans(request):
    error = request.GET.get('error')
    if request.method == 'POST':
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        submit_type = request.POST.get('plans_level')
        payload = {'subscription_level': submit_type}
        payload = json.dumps(payload)
        response = requests.post(url + '/subscription/api/', data=payload, headers=header)
        if response.status_code == 201:
            return HttpResponseRedirect('/create-branch/')
        else:
            error = response.text
            return HttpResponseRedirect('/plans/?error=' + error)
    return render(request, 'auth/plans.html')


# create company views here
def create_company(request):
    error = request.GET.get('error')
    if request.method == 'POST':
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        name = request.POST['create_company_name']
        user_type = request.POST['user_category_input']
        if user_type == '':
            type_status = False
            user_type = request.POST['category_name']
        else:
            type_status = True
        payload = {'name': name, 'type': user_type, 'type_status': type_status}
        payload = json.dumps(payload)
        response = requests.post(url + '/company/api/', headers=header, data=payload)
        if response.status_code == 201:
            response = requests.post(url + '/branch/api/', headers=header)
            if response.status_code == 201:
                response = requests.post(url + '/subscription/api/', headers=header)
                if response.status_code == 201:
                    return HttpResponseRedirect('/dashboard/')
        else:
            error = json.loads(response.text)
            return HttpResponseRedirect('/create-company/?error=' + error)
    return render(request, 'auth/create_company.html')


def create_branch(request):
    error = request.GET.get('error')
    if request.method == 'POST':
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        name = request.POST['branch_name']
        title = request.POST['branch_title']
        address = request.POST['branch_address']
        phone = request.POST['branch_phone']
        user_email = request.POST['branch_email']
        no_manager = request.POST.get('no-branch-manager')
        if no_manager == "1":
            payload = {'name': name, 'phone': phone, 'email': user_email, 'title': title,
                       'address': address}
        else:
            manager = request.POST['branch_manager_email']
            payload = {'name': name, 'phone': phone, 'email': user_email, 'title': title, 'manager': manager,
                       'address': address}
        payload = json.dumps(payload)
        response = requests.post(url + '/branch/api/', headers=header, data=payload)
        if response.status_code == 201:
            return HttpResponseRedirect('/dashboard/')
        else:
            error_obj = json.loads(response.text)
            if error_obj["email"]:
                error = "Email already assigned with another branch"
            else:
                error = error_obj["detail"]
            return HttpResponseRedirect('/create-branch/?error=' + error)
    return render(request, 'auth/create_branch.html')


# sidebar views here
def dashboard(request):
    error = request.GET.get('error')
    state_type_str = request.GET.get('type')
    try:
        session_key = request.session.get('key')
        key = "Token " + session_key
    except Exception as e:
        print(str(e))
        return HttpResponseRedirect('/sign-in/')
    header = {'Content-Type': 'application/json', 'Authorization': key}
    # Manager area
    # user_info = requests.get(url + '/user/api/', headers=header).json()
    # user_email = user_info[0]["email"]
    # sign_up_completion = requests.get(url + '/user/info/?email=' + user_email, headers=header)
    # sign_up_completion_dict = json.loads(sign_up_completion.text)
    # manager_status = sign_up_completion_dict[1]['is_manager']
    # if manager_status:
    #     item_list = requests.get(url + '/item/api/', headers=header).json()
    #     combo_info = requests.get(url + '/group/api/', headers=header).json()
    #     menu_info = requests.get(url + '/menu/api/', headers=header).json()
    #     branch_info = requests.get(url + '/branch/api/', headers=header).json()
    #     branch_count = len(branch_info)
    #     print(menu_info)
    #     return render(request, 'dashboard.html',
    #                   {'item_list': item_list, 'user_info': user_info[0],
    #                    'combo_info': combo_info,
    #                    'branch_info': branch_info, 'menu_info': menu_info, 'error': error,
    #                    'manager_status': manager_status, 'branch_count': branch_count})
    # else:
    item_list = requests.get(url + '/item/api/', headers=header).json()
    user_info = requests.get(url + '/user/api/', headers=header).json()
    combo_info = requests.get(url + '/group/api/', headers=header).json()
    branch_info = requests.get(url + '/branch/api/', headers=header).json()
    menu_info = requests.get(url + '/menu/api/', headers=header).json()
    bid = str(branch_info[0]["id"])
    payload = {'branch_id': bid}
    promotion = requests.get(url + '/menu/get-primary/', params=payload, headers=header).json()
    format_info = requests.get(url + '/branch/format/' + bid + '/', headers=header).json()
    user_system_settings = requests.get(url + '/branch/n-settings/' + bid + '/', headers=header).json()
    localization_info = requests.get(url + '/branch/zone/' + bid + '/', headers=header).json()
    all_country_list = country_list()
    all_time_zone_list = time_zone()
    all_currency_list = currency()
    branch_count = len(branch_info)
    new_item_list = item_list
    new_combo_list = combo_info
    new_menu_list = menu_info
    for item in new_item_list:
        date_obj = item["updated_at"]
        date_list = date_obj.split('T')
        new_date_obj = datetime.strptime(date_list[0], '%Y-%m-%d')
        formatted_date = new_date_obj.strftime('%d %B, %Y')
        item["updated_at"] = formatted_date

    for item in new_combo_list:
        date_obj = item["updated_at"]
        date_list = date_obj.split('T')
        new_date_obj = datetime.strptime(date_list[0], '%Y-%m-%d')
        formatted_date = new_date_obj.strftime('%d %B, %Y')
        item["updated_at"] = formatted_date
    for menu in new_menu_list:
        menu_length = len(menu["menu"])
        for i in range(menu_length):
            date_obj = menu["menu"][i]["updated_at"]
            date_list = date_obj.split('T')
            new_date_obj = datetime.strptime(date_list[0], '%Y-%m-%d')
            formatted_date = new_date_obj.strftime('%d %B, %Y')
            menu["menu"][i]["updated_at"] = formatted_date
    try:
        company_info = requests.get(url + '/company/api/', headers=header).json()
        company_id_stat = company_info[0]["id"]
    except:
        return HttpResponseRedirect('/create-company/')
    state_data = None
    if state_type_str:
        state_type = int(state_type_str)
        payload = {'stat_type': state_type, 'company_id': company_id_stat}
        payload = json.dumps(payload)
        header = {'Content-Type': 'application/json'}
        stat_data = requests.post(url + '/menu/stats/', headers=header, data=payload)
        if stat_data.status_code == 200:
            state_data = json.loads(stat_data.text)
    return render(request, 'dashboard.html',
                  {'item_list': new_item_list, 'user_info': user_info[0],
                   'combo_info': new_combo_list, 'localization_info': localization_info,
                   'company_info': company_info[0], 'user_system_settings': user_system_settings,
                   'branch_info': branch_info[0], 'menu_info': menu_info, 'state_data': state_data,
                   'branch_count': branch_count, 'format_info': format_info, 'country_name': all_country_list,
                   'time_zone': all_time_zone_list, 'currency_list': all_currency_list, 'promotion': promotion,
                   'company_id_stat': company_id_stat, 'error': error})


def update_multiple_item(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        item_list = request.POST.getlist('items[]')
        payload = {"items": item_list}
        status = request.POST.get('status')
        category = request.POST.get('category')
        if status != '':
            payload["status"] = status
        if category != '':
            payload["category"] = category
        payload = json.dumps(payload)
        response = requests.post(url + '/item/multiple-update/', headers=header, data=payload)
        if response.status_code == 200:
            return JsonResponse({"message": "Items updated successfully"})
        else:
            error = response.text
            return JsonResponse({"error": error}, status=response.status_code)


def update_multiple_combo(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        combo_list = request.POST.getlist('combos[]')
        payload = {"groups": combo_list}
        status = request.POST.get('status')
        category = request.POST.get('category')
        if status != '':
            payload["status"] = status
        if category != '':
            payload["category"] = category
        payload = json.dumps(payload)
        response = requests.post(url + '/group/multiple-update/', headers=header, data=payload)
        if response.status_code == 200:
            return JsonResponse({"message": "Combo updated successfully"})
        else:
            error = response.text
            return JsonResponse({"error": error}, status=response.status_code)


# items views here
def items(request, item_id, bid):
    try:
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
    except:
        return HttpResponseRedirect('/sign-in/')
    item_list = requests.get(url + '/item/api/' + item_id + '/', headers=header).json()
    localization_info = requests.get(url + '/branch/zone/' + bid + '/', headers=header).json()
    print(localization_info)
    if request.method == "POST":
        name = request.POST['item_name_update']
        status_selected = request.POST.get('item_status')
        price = request.POST['item_price_update']
        description = request.POST['item_description_update']
        category = request.POST['item_category_update']
        payload = {'name': name, 'price': price,
                   'description': description, 'category': category, 'status': status_selected}
        try:
            item_vid = request.POST['video_link_update']
            if item_vid == '':
                payload["video_link"] = ""
        except:
            item_vid = ''
            payload["video_link"] = item_vid
        if item_vid != '':
            if "youtu.be" in item_vid:
                item_vid_code = item_vid.split('/')[-1]
            elif "www.youtube.com/watch" in item_vid:
                item_vid_code = item_vid.split('v=')[1].split('&')[0]
            elif "www.youtube.com/embed" in item_vid:
                item_vid_code = item_vid.split('embed/')[1].split('"')[0]
            else:
                item_vid_code = ''
                error = 'Invalid youtube link'
                return HttpResponseRedirect('/dashboard/?error=' + error)
            if item_vid_code != '':
                item_vid = "https://www.youtube.com/embed/" + item_vid_code
                payload["video_link"] = item_vid
        try:
            discount = request.POST['item_rate_update']
            payload["discount"] = discount
        except:
            discount = 0.0
            payload["discount"] = discount
        try:
            image = request.FILES['food_image_upload_update']
            # file = [('image', image)]
            buffer = convert_to_OneToOne_ratio(image, 1)
            file = InMemoryUploadedFile(
                buffer, None, "image.png", "image/png",
                buffer.tell(), None
            )
            response = requests.patch(url + '/item/api/' + item_id + '/', headers=header, data=payload,
                                      files={'image': file})
        except:
            image = ""
            response = requests.patch(url + '/item/api/' + item_id + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/items/' + item_id + '/' + bid + '/')
        else:
            error = "Name field should not be more than 50 character"
            return HttpResponseRedirect('/items/' + item_id + '/' + bid + '/?error=' + error)
            # return render(request, 'items_details.html', {'item_list': item_list, 'error': error_value})
    return render(request, 'items_details.html',
                  {'item_list': item_list, 'localization_info': localization_info, 'bid': bid})


def remove_promo(request, bid):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Authorization': key}
    empty_file = io.BytesIO()
    payload = {'branch': bid, 'promo_name': "", 'promo_vid': ""}
    response = requests.post(url + '/menu/primary/pm_update/', headers=header, data=payload,
                             files={'promo_image': ('', empty_file)})
    print(response.text)
    if response.status_code == 200:
        return HttpResponseRedirect('/dashboard/')
    else:
        error = "Promotion remove unsuccessfully"
        print(response.text)
        return HttpResponseRedirect('/dashboard/?error=' + error)


def add_promo(request):
    if request.method == 'POST':
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        promo_name = request.POST['promo_name']
        b_id = request.POST['branch_id']
        payload = {'branch': b_id, 'promo_name': promo_name}
        promo_vid = request.POST['promo_vid']
        if promo_vid != '':
            if "youtu.be" in promo_vid:
                promo_vid_code = promo_vid.split('/')[-1]
            elif "www.youtube.com/watch" in promo_vid:
                promo_vid_code = promo_vid.split('v=')[1].split('&')[0]
            elif "www.youtube.com/embed" in promo_vid:
                promo_vid_code = promo_vid.split('embed/')[1].split('"')[0]
            else:
                promo_vid_code = ''
                error = 'Invalid youtube link'
                return HttpResponseRedirect('/dashboard/?error=' + error)
            if promo_vid_code != '':
                promo_vid = "https://www.youtube.com/embed/" + promo_vid_code
                payload['promo_vid'] = promo_vid
            if 'promo_image' in request.FILES:
                images = request.FILES['promo_image']
                file = [('promo_image', images)]
                response = requests.post(url + '/menu/primary/pm_update/', headers=header, data=payload, files=file)
            # file = [('promo_image', '')]
            response = requests.post(url + '/menu/primary/pm_update/', headers=header, data=payload)
        elif 'promo_image' in request.FILES:
            payload['promo_vid'] = ''
            images = request.FILES['promo_image']
            file = [('promo_image', images)]
            response = requests.post(url + '/menu/primary/pm_update/', headers=header, data=payload, files=file)
        elif 'promo_image' in request.FILES and 'promo_vid' in request.POST:
            images = request.FILES['promo_image']
            file = [('promo_image', images)]
            response = requests.post(url + '/menu/primary/pm_update/', headers=header, data=payload, files=file)
        else:
            payload['promo_vid'] = ''
            # file = [('promo_image', '')]
            # response = requests.post(url + '/menu/primary/pm_update/', headers=header, data=payload)
            error = "You need to enter at least video or a image"
            return HttpResponseRedirect('/dashboard/?error=' + error)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def qr_create(request):
    if request.method == 'POST':
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        canvas_data = request.POST.get('canvas_data')

        # Convert data URL to image file
        # format, imgstr = canvas_data.split(';base64,')
        # ext = format.split('/')[-1]
        # data = ContentFile(base64.b64decode(imgstr))
        # filename = 'canvas_image.' + ext
        # request.FILES[filename] = data
        # image = request.FILES[filename]
        payload = {'QR': canvas_data}
        response = requests.post(url + '/branch/api/qr_update/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
    return HttpResponseRedirect('/dashboard/')


def qr_wifi_create(request):
    if request.method == 'POST':
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        canvas_data = request.POST.get('canvas_data')

        # Convert data URL to image file
        # format, imgstr = canvas_data.split(';base64,')
        # ext = format.split('/')[-1]
        # data = ContentFile(base64.b64decode(imgstr))
        # filename = 'canvas_image.' + ext
        # request.FILES[filename] = data
        # image = request.FILES[filename]
        payload = {'Wifi': canvas_data}
        response = requests.post(url + '/branch/api/wifi_update/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
    return HttpResponseRedirect('/dashboard/')


def menu_details(request, menu_id, bid):
    try:
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
    except:
        return HttpResponseRedirect('/sign-in/')
    menu_info = requests.get(url + '/menu/api/' + menu_id + '/', headers=header).json()
    item_list = requests.get(url + '/item/api/', headers=header).json()
    combo_info = requests.get(url + '/group/api/', headers=header).json()
    new_menu_obj = menu_info
    localization_info = requests.get(url + '/branch/zone/' + bid + '/', headers=header).json()
    for item in new_menu_obj["item"]:
        date_obj = item["updated_at"]
        date_list = date_obj.split('T')
        new_date_obj = datetime.strptime(date_list[0], '%Y-%m-%d')
        formatted_date = new_date_obj.strftime('%d %B, %Y')
        item["updated_at"] = formatted_date
    for group in new_menu_obj["group"]:
        date_obj = group["updated_at"]
        date_list = date_obj.split('T')
        new_date_obj = datetime.strptime(date_list[0], '%Y-%m-%d')
        formatted_date = new_date_obj.strftime('%d %B, %Y')
        group["updated_at"] = formatted_date

    return render(request, 'menu.html',
                  {'menu_info': new_menu_obj, 'item_list': item_list, 'combo_info': combo_info,
                   'my_menu_id': menu_id, 'localization_info': localization_info, 'bid': bid})


# def phone_view(request, menu_branch_id):
#     header = {'Content-Type': 'application/json'}
#     payload = {'branch_id': menu_branch_id}
#     menu_info_id = requests.get(url + '/menu/get-primary/', params=payload, headers=header).json()
#     menu_id = menu_info_id["menu"]
#     payload = {'id': menu_id}
#     menu_info = requests.get(url + '/menu/get-category-menu/', params=payload, headers=header).json()
#     payload = {'menu_id': menu_id}
#     payload = json.dumps(payload)
#     set_counter = requests.post(url + '/menu/counter/', data=payload, headers=header)
#     print(menu_info)
#     return render(request, 'user-view/phone_view.html', {'menu_info': menu_info_id})


def offer_menu(request):
    return render(request, 'user-view/offer_menu.html')


def reset_password(request, token):
    if request.method == "POST":
        header = {'Content-Type': 'application/json'}
        pw = request.POST['reset_new_password']
        payload = {'password': pw, 'token': token}
        payload = json.dumps(payload)
        response = requests.post(url + '/user/reset/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/sign-in/')
        else:
            error = json.loads(response.text)
            return HttpResponseRedirect('/reset-pass/' + token + '/?error=' + error)
    return render(request, 'auth/forgot_password.html', {'token': token})


def reset_email_verification(request):
    if request.method == "POST":
        header = {'Content-Type': 'application/json'}
        email = request.POST["reset-pass-email-verification"]
        payload = {'email': email}
        response = requests.get(url + '/user/reset/', params=payload, headers=header)
        if response.status_code == 200:
            return HttpResponseRedirect('/sign-in/')
        else:
            error = json.loads(response.text)
            return HttpResponseRedirect('/reset-pass-email/?error=' + error)
    return render(request, 'auth/reset_pass_email_veri.html')


def post_feedback(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        # body
        subject = request.POST['feedback_subject']
        description = request.POST['feedback_description']
        payload = {'subject': subject, 'message': description}
        payload = json.dumps(payload)
        response = requests.post(url + '/user/feedback/', data=payload, headers=header)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            print(response.text)
    return HttpResponseRedirect('/dashboard/')


def contact_us(request):
    if request.method == "POST":
        header = {'Content-Type': 'application/json'}
        # body
        name = request.POST['contact_name']
        email = request.POST['contact_email']
        subject = request.POST['contact_subject']
        message = request.POST['contact_message']
        payload = {'subject': subject, 'message': message, 'name': name, 'email': email}
        payload = json.dumps(payload)
        response = requests.post(url + '/user/contact-us/', data=payload, headers=header)
        if response.status_code == 200:
            return HttpResponseRedirect('/sign-in/')

        else:
            print(response.text)
    return render(request, 'dashboard-content/contact_us.html')


def add_item(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        name = request.POST['item_name']
        price = request.POST['item_price']
        description = request.POST['item_description']
        category = request.POST['item_category']
        payload = {'name': name, 'price': price,
                   'description': description, 'category': category}
        try:
            item_vid = request.POST['item_vid_link']
            if item_vid == '':
                payload["video_link"] = ""
        except:
            item_vid = ''
            payload["video_link"] = item_vid
        if item_vid != '':
            if "youtu.be" in item_vid:
                item_vid_code = item_vid.split('/')[-1]
            elif "www.youtube.com/watch" in item_vid:
                item_vid_code = item_vid.split('v=')[1].split('&')[0]
            elif "www.youtube.com/embed" in item_vid:
                item_vid_code = item_vid.split('embed/')[1].split('"')[0]
            else:
                item_vid_code = ''
                error = 'Invalid youtube link'
                return HttpResponseRedirect('/dashboard/?error=' + error)
            if item_vid_code != '':
                item_vid = "https://www.youtube.com/embed/" + item_vid_code
                payload["video_link"] = item_vid
        try:
            image = request.FILES['item_file_image']
            # file = [('image', images)]
            buffer = convert_to_OneToOne_ratio(image, 1)
            file = InMemoryUploadedFile(
                buffer, None, "image.png", "image/png",
                buffer.tell(), None
            )
            response = requests.post(url + '/item/api/', headers=header, data=payload, files={'image': file})
        except:
            response = requests.post(url + '/item/api/', headers=header, data=payload)
        if response.status_code == 201:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = json.loads(response.text)
            error_value = error["detail"]
            return HttpResponseRedirect('/dashboard/?error=' + error_value)
    return HttpResponseRedirect('/dashboard/')


# To create Combo
def add_combo(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        name = request.POST['combo_name']
        price = request.POST['combo_price']
        category = request.POST['combo_category']
        item = request.POST.getlist('combo_items_checkbox')
        payload = {'name': name, 'price': price, 'category': category, 'item': item}
        try:
            description = request.POST['combo_description']
            payload["description"] = description
        except:
            print('none')

        try:
            combo_vid = request.POST['combo_video']
            if combo_vid == '':
                payload["video_link"] = ""
        except:
            combo_vid = ''
            payload["video_link"] = combo_vid
        if combo_vid != '':
            if "youtu.be" in combo_vid:
                combo_vid_code = combo_vid.split('/')[-1]
            elif "www.youtube.com/watch" in combo_vid:
                combo_vid_code = combo_vid.split('v=')[1].split('&')[0]
            elif "www.youtube.com/embed" in combo_vid:
                combo_vid_code = combo_vid.split('embed/')[1].split('"')[0]
            else:
                combo_vid_code = ''
                error = 'Invalid youtube link'
                return HttpResponseRedirect('/dashboard/?error=' + error)
            if combo_vid_code != '':
                combo_vid = "https://www.youtube.com/embed/" + combo_vid_code
                payload["video_link"] = combo_vid
        try:
            image = request.FILES['combo_image']
            # file = [('image', image)]
            buffer = convert_to_OneToOne_ratio(image, 1)
            file = InMemoryUploadedFile(
                buffer, None, "image.png", "image/png",
                buffer.tell(), None
            )
            response = requests.post(url + '/group/api/', headers=header, data=payload, files={'image': file})
        except:
            response = requests.post(url + '/group/api/', headers=header, data=payload)
        if response.status_code == 201:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            error_value = error
            return HttpResponseRedirect('/dashboard/?error=' + error)
    return HttpResponseRedirect('/dashboard/')


# add item in menu
def add_item_menu(request, menu_id, bid):
    if request.method == "POST":
        item_final_list = []
        combo_final_list = []

        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        # Body
        item_combo_list = requests.get(url + '/menu/api/' + menu_id + '/', headers=header).json()

        item = request.POST.getlist('update_menu_item')
        item_final_list = item
        combo = request.POST.getlist('update_menu_combo')
        combo_final_list = combo

        item_list = item_combo_list["item"]
        combo_list = item_combo_list["group"]

        for data in item_list:
            if str(data["id"]) not in item:
                item_final_list.append(str(data["id"]))

        for data in combo_list:
            if str(data["id"]) not in combo:
                combo_final_list.append(str(data["id"]))
        payload = {'item': item_final_list, 'group': combo_final_list}
        payload = json.dumps(payload)
        response = requests.patch(url + '/menu/api/' + menu_id + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/menu-details/' + menu_id + '/' + bid + '/')
        else:
            print(response.text)
    return HttpResponseRedirect('/menu-details/' + menu_id + '/' + bid + '/')


def create_menu(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}

        name = request.POST['menu_name']
        item_name = request.POST.getlist('menu_items_checkbox')
        meals = request.POST.getlist('menu_meals_checkbox')
        payload = {'name': name}
        try:
            description = request.POST['menu_description']
            payload["description"] = description
        except:
            print('None')
        if len(item_name) == 0:
            payload["group"] = meals
        elif len(meals) == 0:
            payload["item"] = item_name
        else:
            payload["group"] = meals
            payload["item"] = item_name
        try:
            image = request.FILES['menu_image']
            buffer = convert_to_aspect_ratio(image, 1.778)
            file = InMemoryUploadedFile(
                buffer, None, "image.png", "image/png",
                buffer.tell(), None
            )
            response = requests.post(url + '/menu/api/', headers=header, data=payload, files={'image': file})
        except:
            response = requests.post(url + '/menu/api/', headers=header, data=payload)
        if response.status_code == 201:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)
    return HttpResponseRedirect('/dashboard/')


def user_update(request, user_id):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        # Body
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        payload = {'first_name': first_name, 'last_name': last_name}
        try:
            phone = request.POST['phone']
            payload['phone'] = phone
        except:
            print("None")
        try:
            date_of_birth = request.POST['date_of_birth']
            payload['date_of_birth'] = date_of_birth
        except:
            print("None")
        try:
            nid = request.POST['nid_number']
            payload['nid'] = nid
        except:
            print("None")
        try:
            image = request.FILES['user_image']
            file = [('image', image)]
            response = requests.patch(url + '/user/api/' + user_id + '/', headers=header, data=payload, files=file)
        except:
            response = requests.patch(url + '/user/api/' + user_id + '/', headers=header, data=payload)

        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = json.loads(response.text)
            if error['phone']:
                print("Phone number can not be more than 11 number")
            return HttpResponseRedirect('/dashboard/')
    return HttpResponseRedirect('/dashboard/')


def company_update(request, company_id):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Authorization': key}
        try:
            trade_license = request.POST['trade_license']
        except:
            trade_license = ''
        try:
            logo = request.FILES['company_logo']
        except:
            logo = ""
        if trade_license != '' and logo != "":
            payload = {'trade_license': trade_license}
            file = [('image', logo)]
            response = requests.patch(url + '/company/api/' + company_id + '/', headers=header, data=payload,
                                      files=file)
        elif trade_license != '':
            payload = {'trade_license': trade_license}
            response = requests.patch(url + '/company/api/' + company_id + '/', headers=header, data=payload)
        elif logo != "":
            file = [('image', logo)]
            response = requests.patch(url + '/company/api/' + company_id + '/', headers=header, files=file)
        else:
            return HttpResponseRedirect('/dashboard/?error=Please provide at least one item')
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = json.loads(response.text)
            return HttpResponseRedirect('/dashboard/?error=' + error)
    return HttpResponseRedirect('/dashboard/')


def update_branch(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}

        name = request.POST['branch_update_name']
        address = request.POST['branch_update_address']
        title = request.POST['branch_update_title']
        phone = request.POST['branch_update_phone']
        bid = request.POST['edit_branch_id']
        payload = {'name': name, 'address': address, 'title': title, 'phone': phone}
        payload = json.dumps(payload)
        response = requests.patch(url + '/branch/api/' + bid + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = json.loads(response.text)
            error_value = error["detail"]
            return HttpResponseRedirect('/dashboard/?error=' + error_value)
    return HttpResponseRedirect('/dashboard/')


def delete_branch(request, bid):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Content-Type': 'application/json', 'Authorization': key}

    response = requests.delete(url + '/branch/api/' + bid + '/', headers=header)
    if response.status_code == 204:
        return HttpResponseRedirect('/dashboard/')
    else:
        error = "You have only one branch, you can not delete"
        return HttpResponseRedirect('/dashboard/?error=' + error)


def add_branch(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        # body
        name = request.POST['new_branch_name']
        address = request.POST['new_branch_address']
        phone = request.POST['new_branch_phone']
        email = request.POST['new_branch_email']
        title = request.POST['new_branch_title']
        # manager_email = request.POST['new_branch_mEmail']
        payload = {'name': name, 'address': address, 'phone': phone, 'email': email,
                   'title': title}
        payload = json.dumps(payload)
        response = requests.post(url + '/branch/api/', data=payload, headers=header)
        if response.status_code == 201:
            return HttpResponseRedirect('/dashboard/')
        else:
            error_obj = json.loads(response.text)
            try:
                test = error_obj['detail']
                error = "You have to chose subscription level 3 or up to create multiple branch"
            except:
                error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)
    return HttpResponseRedirect('/dashboard/')


def delete_item(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        item_list = request.POST.getlist('item_delete_button')
        payload = {"id": item_list}
        payload = json.dumps(payload)
        response = requests.post(url + '/item/api/delete_multiple/', data=payload, headers=header)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def delete_combo(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        # body
        combo_list = request.POST.getlist('combo_delete_button')
        payload = {"id": combo_list}
        payload = json.dumps(payload)
        response = requests.post(url + '/group/api/delete_multiple/', data=payload, headers=header)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def change_package(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        subscription_level = request.POST['selected-package']
        payload = {'subscription_level': subscription_level}
        payload = json.dumps(payload)
        response = requests.patch(url + '/subscription/update/', data=payload, headers=header)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = json.loads(response.text)
            error_value = error["detail"]
            return HttpResponseRedirect('/dashboard/?error=' + error_value)
    return HttpResponseRedirect('/dashboard/')


def set_date_format(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        bid = request.POST['branch_id']
        date_format = request.POST['date_format']
        currency_precision = request.POST['currency_precision']
        time_format = request.POST['time_format']
        number_format = request.POST['number_format']
        begin_week = request.POST['day_of_week']
        payload = {'date_format': date_format, 'currency_precision': currency_precision, 'time_format': time_format,
                   'number_format': number_format, 'begin_week': begin_week}
        payload = json.dumps(payload)
        response = requests.patch(url + '/branch/format/' + bid + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def update_localization(request):
    if request.method == "POST":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        bid = request.POST['branch_id']
        country_name = request.POST['country_name']
        set_time_zone = request.POST['time_zone']
        set_currency = request.POST['currency']
        payload = {'time_zone': set_time_zone, 'currency': set_currency, 'country': country_name}
        payload = json.dumps(payload)
        response = requests.patch(url + '/branch/zone/' + bid + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def system_update(request):
    if request.method == "GET":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        bid = str(request.GET.get('branch_id'))
        settings_system_update = request.GET.get('system_update')
        payload = {'system_update': settings_system_update}
        payload = json.dumps(payload)
        response = requests.patch(url + '/branch/n-settings/' + bid + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def change_log(request):
    if request.method == "GET":
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        bid = str(request.GET.get('branch_id'))
        settings_change_log = request.GET.get('change_log')
        payload = {'change_log': settings_change_log}
        payload = json.dumps(payload)
        response = requests.patch(url + '/branch/n-settings/' + bid + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            return HttpResponseRedirect('/dashboard/?error=' + error)


def delete_menu_item(request, menu_id, bid):
    if request.method == "POST":
        item_final_list = []
        combo_final_list = []
        session_key = request.session.get('key')
        key = "Token " + session_key
        header = {'Content-Type': 'application/json', 'Authorization': key}
        # Body
        item_combo_list = requests.get(url + '/menu/api/' + menu_id + '/', headers=header).json()

        item = request.POST.getlist('menu_item_delete_button_checkbox')
        combo = request.POST.getlist('menu_combo_delete_button_checkbox')

        item_list = item_combo_list["item"]
        combo_list = item_combo_list["group"]

        for data in item_list:
            if str(data["id"]) not in item:
                item_final_list.append(str(data["id"]))

        for data in combo_list:
            if str(data["id"]) not in combo:
                combo_final_list.append(str(data["id"]))

        payload = {'item': item_final_list, 'group': combo_final_list}
        payload = json.dumps(payload)
        response = requests.patch(url + '/menu/api/' + menu_id + '/', headers=header, data=payload)
        if response.status_code == 200:
            return HttpResponseRedirect('/menu-details/' + menu_id + '/' + bid + '/')
        else:
            error = response.text
            return HttpResponseRedirect('/menu-details/' + menu_id + '/' + bid + '/?error=' + error)
    return HttpResponseRedirect('/menu-details/' + menu_id + '/' + bid + '/')


def transfer_owner(request, email_id):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Content-Type': 'application/json', 'Authorization': key}
    payloads = {'email': email_id}
    response = requests.get(url + '/company/transfer-owner/', headers=header, params=payloads)
    if response.status_code == 200:
        return HttpResponseRedirect('/dashboard/')
    else:
        error = response.text
    return HttpResponseRedirect('/dashboard/?error=' + error)


# def delete_combo(request):
#     if request.method == "POST":
#         session_key = request.session.get('key')
#         key = "Token " + session_key
#         header = {'Content-Type': 'application/json', 'Authorization': key}
#         item_list = request.POST.getlist('item_delete_button')
#         payload = {'id': item_list}
#         payload = json.dumps(payload)
#         response = requests.post(url + '/item/api/delete_multiple/', data=payload, headers=header)
#         if response.status_code == 204:
#             return HttpResponseRedirect('/dashboard/')
#         else:
#             print(response.text)
#     return HttpResponseRedirect('/dashboard/')


def convert_to_aspect_ratio(image_path, aspect_ratio):
    # Open the image using Pillow
    im = Image.open(image_path)
    # Get the original dimensions of the image
    width, height = im.size
    # Calculate the new height and width based on the aspect ratio
    new_height = int(width / aspect_ratio)
    new_width = int(height * aspect_ratio)
    # Determine the area to crop based on the new dimensions
    if new_height > height:
        # Crop the sides of the image
        left = int((width - new_width) / 2)
        top = 0
        right = int(left + new_width)
        bottom = height
    else:
        # Crop the top and bottom of the image
        left = 0
        top = int((height - new_height) / 2)
        right = width
        bottom = int(top + new_height)
    # Crop the image to the specified area
    im = im.crop((left, top, right, bottom))
    # Resize the image to the specified aspect ratio
    im = im.resize((int(new_width), int(new_height)))
    # Create a BytesIO object to hold the image data
    buffer = BytesIO()
    # Save the image to the buffer in PNG format
    im.save(buffer, format="PNG")
    # Reset the buffer position to the beginning
    buffer.seek(0)
    # Return the buffer object
    return buffer


def convert_to_OneToOne_ratio(image_path, aspect_ratio):
    # Open the image using Pillow
    im = Image.open(image_path)
    # Get the original dimensions of the image
    width, height = im.size
    # Calculate the new height and width based on the aspect ratio
    new_width = int(min(width, height) * aspect_ratio)
    new_height = int(new_width / aspect_ratio)
    # Determine the area to crop based on the new dimensions
    left = int((width - new_width) / 2)
    top = int((height - new_height) / 2)
    right = int(left + new_width)
    bottom = int(top + new_height)
    # Crop the image to the specified area
    im = im.crop((left, top, right, bottom))
    # Resize the image to the specified aspect ratio
    im = im.resize((new_width, new_height))
    # Create a BytesIO object to hold the image data
    buffer = BytesIO()
    # Save the image to the buffer in PNG format
    im.save(buffer, format="PNG")
    # Reset the buffer position to the beginning
    buffer.seek(0)
    # Return the buffer object
    return buffer


# primary menu set
def set_primary_menu(request, bid, menu_id):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Content-Type': 'application/json', 'Authorization': key}
    payload = {'branch': bid, 'menu': menu_id}
    payload = json.dumps(payload)
    response = requests.post(url + '/menu/primary/', data=payload, headers=header)
    return HttpResponseRedirect('/dashboard/')


# additional signup
def user_sign_up(request):
    global email, branch_id, company_id
    header = {'Content-Type': 'application/json'}
    email = request.GET.get('email')
    branch_id = request.GET.get('branch_id')
    company_id = request.GET.get('company_id')
    try:
        token = request.GET.get('token')
    except:
        token = ""
    if request.method == 'POST':
        first_name = request.POST['additional_first_name']
        last_name = request.POST['additional_last_name']
        password = request.POST['additional_signUp_password']
        phone = request.POST['additional_phone']
        if branch_id is not None:
            payload = {'first_name': first_name, 'last_name': last_name, 'password': password, 'phone': phone,
                       'branch_id': branch_id, 'email': email}
            payload = json.dumps(payload)
            response = requests.post(url + '/user/create/', data=payload, headers=header)
        else:
            payload = {'first_name': first_name, 'last_name': last_name, 'password': password, 'phone': phone,
                       'company_id': company_id, 'email': email, 'token': token}
            payload = json.dumps(payload)
            response = requests.post(url + '/user/create/', data=payload, headers=header)
            print(payload)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            session_key = response_dict['token']
            request.session['key'] = session_key
            return HttpResponseRedirect('/dashboard/')
        else:
            error = response.text
            print(error)
            return HttpResponseRedirect('/user-sign-up/?error=' + error)
    return render(request, 'auth/additional_signup.html', {'email': email})


def log_out(request):
    session_key = request.session.get('key')
    if session_key:
        key = "Token " + session_key
        headers = {'Authorization': key}
        response = requests.get(
            url + '/user/logout/', headers=headers)
        if response.status_code == 200:
            request.session.flush()
    return HttpResponseRedirect('/sign-in/')


# from PIL import Image
# from io import BytesIO


# def image_to_excel(request):
#     if request.method == 'POST':
#         images = request.FILES.getlist('images')
#         combined_image = Image.new('RGB', (0, 0))
#         for img in images:
#             # Open the InMemoryUploadedFile object as a PIL Image object
#             buffer = BytesIO(img.read())
#             img = Image.open(buffer)
#
#             # Update the size of the combined image
#             combined_image = Image.new('RGB',
#                                        (max(combined_image.width, img.width), combined_image.height + img.height))
#
#             # Paste the current image into the combined image
#             combined_image.paste(img, (0, combined_image.height - img.height))
#
#         # Perform OCR on the combined image
#         text = pytesseract.image_to_string(combined_image)
#
#         # Convert the OCR output to a Pandas dataframe
#         data = [row.split('\t') for row in text.split('\n')]
#         df = pd.DataFrame(data[1:], columns=data[0])
#
#         # Create an Excel file from the Pandas dataframe and return it as a response
#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="output.xlsx"'
#         df.to_excel(response, index=False)
#         return response
#
#     return render(request, 'auth/imagetoexcell.html')


def image_to_excel(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        wb = openpyxl.Workbook()
        ws = wb.active
        row = 1
        for img in images:
            # Open the InMemoryUploadedFile object as a PIL Image object
            buffer = io.BytesIO(img.read())
            img = Image.open(buffer)

            # Perform OCR on the image
            text = pytesseract.image_to_string(img)

            # Convert the OCR output to a list of rows
            rows = [row.split('\t') for row in text.split('\n')]

            # Write the rows to the Excel worksheet
            for r in rows:
                ws.append(r)

            # Adjust the height of the current row based on the height of the image
            ws.row_dimensions[row].height = img.height / 2.5

            # Increment the row counter
            row += len(rows) + 1

        # Set the column widths to auto-fit
        for col in ws.columns:
            max_length = 0
            column = col[0].column
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            ws.column_dimensions[openpyxl.utils.get_column_letter(column)].width = adjusted_width

        # Save the Excel file and return it as a response
        response = io.BytesIO()
        wb.save(response)
        response.seek(0)
        filename = 'output.xlsx'
        content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response = HttpResponse(response.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    return render(request, 'auth/imagetoexcell.html')


def insert_items(request):
    session_key = request.session.get('key')
    key = "Token " + session_key
    header = {'Content-Type': 'application/json', 'Authorization': key}
    if request.method == 'POST':
        excel_file = request.FILES['user_excel_file']
        # Read the Excel file using pandas
        df = pd.read_excel(excel_file)
        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict('records')
        # data = json.dumps(data)
        item_obj = {}
        items = []
        for item in data:
            item = {key.lower(): value for key, value in item.items()}
            items.append(item)
        item_obj["items"] = items
        # Iterate through the list of items
        for i in item_obj["items"]:
            if isinstance(i["price"], float) and math.isnan(i["price"]):
                i["price"] = 0

            if isinstance(i["category"], float) and math.isnan(i["category"]):
                i["category"] = "Uncategorized"

            if isinstance(i["name"], float) and math.isnan(i["name"]):
                i["name"] = "Item"
        item_obj = json.dumps(item_obj)
        response = requests.post(url + '/item/api/create_multiple/', headers=header, data=item_obj)
        if response.status_code == 201:
            return HttpResponseRedirect('/dashboard/')
        else:
            error = "Please recheck the format"
            return HttpResponseRedirect('/dashboard/?error=' + error)


def phone_menu(request, menu_branch_id):
    header = {'Content-Type': 'application/json'}
    payload = {'branch_id': menu_branch_id}
    menu_info_id = requests.get(url + '/menu/get-primary/', params=payload, headers=header).json()
    menu_id = menu_info_id["menu"]
    payload = {'id': menu_id}
    menu_info = requests.get(url + '/menu/get-category-menu/', params=payload, headers=header).json()
    payload = {'menu_id': menu_id}
    payload = json.dumps(payload)
    set_counter = requests.post(url + '/menu/counter/', data=payload, headers=header)
    localization_info = requests.get(url + '/branch/zone/' + menu_branch_id + '/', headers=header).json()
    return render(request, 'user-view/mobile-menu-view/mobile-menu-view.html',
                  {'menu_info_id': menu_info_id, 'menu_details': menu_info, 'menu_id': menu_id,
                   'menu_branch_id': menu_branch_id, 'localization_info': localization_info})


def phone_item_details(request, item_id, menu_id, menu_branch_id):
    header = {'Content-Type': 'application/json'}
    item_details = requests.get(url + '/item/api/' + item_id + '/', headers=header).json()
    param = {'menu_id': menu_id, 'item_id': item_id}
    suggestions = requests.get(url + '/menu/item-ai/', params=param, headers=header).json()
    localization_info = requests.get(url + '/branch/zone/' + menu_branch_id + '/', headers=header).json()
    return render(request, 'user-view/mobile-menu-view/Item/item-description.html',
                  {'item_details': item_details, 'localization_info': localization_info, 'suggestions': suggestions})


def phone_combo_details(request, group_id, menu_branch_id):
    header = {'Content-Type': 'application/json'}
    group_details = requests.get(url + '/group/api/' + group_id + '/', headers=header).json()
    localization_info = requests.get(url + '/branch/zone/' + menu_branch_id + '/', headers=header).json()
    return render(request, 'user-view/mobile-menu-view/combo/combo-details.html',
                  {'group_details': group_details, 'localization_info': localization_info})


def country_list():
    list_of_country = ["Marshall Islands", "Finland", "Belarus", "Eritrea", "Malta", "Bolivia", "Uganda", "Philippines",
                       "Gibraltar", "British Virgin Islands", "Bosnia and Herzegovina", "Guinea", "Albania",
                       "Sierra Leone",
                       "Chad", "Antarctica", "Czechia", "Macau", "R 'e9union", "Saudi Arabia", "Germany", "Guernsey",
                       "Saint Kitts and Nevis", "Algeria", "Nauru", "Dominican Republic", "Palestine", "Micronesia",
                       "Nigeria", "Caribbean Netherlands", "Cocos (Keeling) Islands", "Libya", "Egypt", "Oman",
                       "Northern Mariana Islands", "Faroe Islands", "Costa Rica", "Sint Maarten", "Solomon Islands",
                       "Tuvalu", "North Macedonia", "Ethiopia", "Guyana", "France", "Azerbaijan", "Isle of Man",
                       "Malaysia",
                       "Iran", "Venezuela", "United Arab Emirates", "Suriname", "Saint Lucia", "Madagascar", "Slovenia",
                       "Ukraine", "Italy", "French Southern and Antarctic Lands", "Fiji", "United Kingdom", "Ghana",
                       "Singapore", "Mauritius", "Aruba", "Grenada", "Liberia", "Lithuania", "New Caledonia",
                       "Zimbabwe",
                       "Niue", "Kuwait", "Thailand", "Comoros", "Mauritania", "Tunisia", "United States", "Gambia",
                       "South Korea", "Syria", "Liechtenstein", "Romania", "Paraguay", "South Africa", "Qatar", "Iraq",
                       "Canada", "Austria", "Serbia", "Bermuda", "Portugal", "Norfolk Island", "Western Sahara",
                       "Bouvet Island", "North Korea", "Zambia", "Cambodia", "Cameroon", "Sudan", "Peru", "DR Congo",
                       "French Guiana", "Russia", "Tonga", "Hungary", "Turks and Caicos Islands", "Taiwan",
                       "Saint Pierre and Miquelon", "Falkland Islands", "Montserrat", "Malawi", "Guinea-Bissau",
                       "Botswana",
                       "Cape Verde", "Guadeloupe", "Monaco", "Kenya", "United States Minor Outlying Islands", "Vietnam",
                       "Saint Barth 'e9lemy", "British Indian Ocean Territory", "Bangladesh", "Papua New Guinea",
                       "Turkmenistan", "Chile", "Mayotte", "Cura 'e7ao", "Burkina Faso", "Ecuador", "American Samoa",
                       "Tanzania", "Belgium", "Mozambique", "Guatemala", "Montenegro", "Vanuatu", "Kosovo", "Lebanon",
                       "Greenland", "Tokelau", "Samoa", "Togo", "Panama", "Vatican City", "New Zealand", "Sweden",
                       "China",
                       "Latvia", "Switzerland", "Djibouti", "Bhutan", "Timor-Leste",
                       "Saint Helena, Ascension and Tristan da Cunha", "Denmark", "Martinique", "Iceland",
                       "Antigua and Barbuda", "Angola", "French Polynesia", "Japan", "Brazil", "Tajikistan",
                       "Christmas Island", "Mali", "Netherlands", "Namibia", "Lesotho", "San Marino", "Andorra",
                       "Colombia",
                       "Seychelles", "Brunei", "Barbados", "Pitcairn Islands", "Kyrgyzstan", "Puerto Rico", "Norway",
                       "Palau", "Somalia", "Hong Kong", "Kiribati", "Svalbard and Jan Mayen", "Cyprus", "Uruguay",
                       "Cayman Islands", "Anguilla", "Eswatini", "Morocco", "S 'e3o Tom 'e9 and Pr 'edncipe",
                       "Dominica",
                       "Poland", "Yemen", "Bulgaria", "Ireland", "Bahamas", "Laos", "Armenia", "Pakistan", "Nepal",
                       "Israel", "Nicaragua", "Croatia", "Maldives", "Burundi", "Central African Republic", "Bahrain",
                       "Argentina", "Sri Lanka", "Mexico", "Myanmar", "Rwanda", "Slovakia", "Moldova", "Spain", "Gabon",
                       "Senegal", "Cook Islands", "Belize", "Trinidad and Tobago", "Estonia", "Greece", "Guam",
                       "Georgia",
                       "Kazakhstan", "Luxembourg", "Turkey", "Benin", "Ivory Coast", " 'c5land Islands", "Australia",
                       "Equatorial Guinea", "Niger", "El Salvador", "Saint Vincent and the Grenadines", "Indonesia",
                       "Mongolia", "South Sudan", "Afghanistan", "Jamaica", "Heard Island and McDonald Islands",
                       "Republic of the Congo", "Saint Martin", "Wallis and Futuna", "India", "South Georgia",
                       "Honduras",
                       "Haiti", "Jersey", "Uzbekistan", "Cuba", "United States Virgin Islands", "Jordan"]
    return list_of_country


def time_zone():
    list_of_times = ["UTC+14:00", "UTC+13:00", "UTC+12:45", "UTC+12:00", "UTC+11:30", "UTC+11:00", "UTC+10:30",
                     "UTC+10:00", "UTC+09:30", "UTC+09:00", "UTC+08:00", "UTC+07:30", "UTC+07:00", "UTC+06:30",
                     "UTC+06:00", "UTC+05:45", "UTC+05:30", "UTC+05:00", "UTC+04:30", "UTC+04:00", "UTC+03:30",
                     "UTC+03:00", "UTC+02:00", "UTC+01:00", "UTC+00:00", "UTC-01:00", "UTC-02:00", "UTC-03:00",
                     "UTC-03:30", "UTC-04:00", "UTC-05:00", "UTC-06:00", "UTC-07:00", "UTC-08:00", "UTC-09:00",
                     "UTC-09:30", "UTC-10:00", "UTC-11:00", "UTC-12:00",
                     ]

    return list_of_times


def currency():
    list_of_currency = ['USD', 'EUR', 'BYN', 'ERN', 'BOB', 'UGX', 'PHP', 'GIP', 'BAM', 'GNF', 'ALL', 'SLL', 'XAF',
                        'CZK', 'MOP', 'SAR', 'GBP', 'GGP', 'XCD', 'DZD', 'AUD', 'DOP', 'EGP', 'ILS', 'JOD', 'NGN',
                        'LYD', 'OMR', 'DKK', 'FOK', 'CRC', 'ANG', 'SBD', 'TVD', 'MKD', 'ETB', 'GYD', 'AZN', 'IMP',
                        'MYR', 'IRR', 'VES', 'AED', 'SRD', 'MGA', 'UAH', 'FJD', 'GHS', 'SGD', 'MUR', 'AWG', 'LRD',
                        'XPF', 'ZWL', 'NZD', 'KWD', 'THB', 'KMF', 'MRU', 'TND', 'GMD', 'KRW', 'SYP', 'CHF', 'RON',
                        'PYG', 'ZAR', 'QAR', 'IQD', 'CAD', 'RSD', 'BMD', 'MAD', 'KPW', 'ZMW', 'KHR', 'SDG', 'PEN',
                        'CDF', 'RUB', 'TOP', 'HUF', 'TWD', 'FKP', 'MWK', 'XOF', 'BWP', 'CVE', 'KES', 'VND', 'BDT',
                        'PGK', 'TMT', 'CLP', 'TZS', 'MZN', 'GTQ', 'VUV', 'LBP', 'WST', 'PAB', 'SEK', 'CNY', 'DJF',
                        'BTN', 'INR', 'SHP', 'ISK', 'AOA', 'JPY', 'BRL', 'TJS', 'NAD', 'LSL', 'COP', 'SCR', 'BND',
                        'BBD', 'KGS', 'NOK', 'SOS', 'HKD', 'KID', 'UYU', 'KYD', 'SZL', 'STN', 'PLN', 'YER', 'BGN',
                        'BSD', 'LAK', 'AMD', 'PKR', 'NPR', 'NIO', 'MVR', 'BIF', 'BHD', 'ARS', 'LKR', 'MXN', 'MMK',
                        'RWF', 'MDL', 'CKD', 'BZD', 'TTD', 'GEL', 'KZT', 'TRY', 'IDR', 'MNT', 'SSP', 'AFN', 'JMD',
                        'HNL', 'HTG', 'JEP', 'UZS', 'CUC', 'CUP']
    return list_of_currency

from django.shortcuts import render, redirect
from forms import *
from query_handler import *
import json
import datetime
import os


SECURITY_SMS = '''curl -X POST  https://rest.nexmo.com/sms/json -d api_key=df746649 -d api_secret=1d240f5535b42132 -d to=972538303783 -d from="DORMS ACCESS MANAGER" -d text="BLACKLIST USER \nID: {}\nROOM: {}\nNAME: {}\nTRYING TO ACCESS DORMS!"'''

RSEIDENT_SMS = '''curl -X POST  https://rest.nexmo.com/sms/json -d api_key=df746649 -d api_secret=1d240f5535b42132 -d to=972523972339 -d from="DORMS ACCESS MANAGER" -d text="VISITOR ID: {}\nNAME: {}\n,ARRIVED TO VISIT YOU"'''

######################################### <WEB APP REQUESTS> #############################################################

def index(request):
    visitors_dict = {}
    residents_dict = {}
    message = ''
    visitor_access = []
    visitor_access_dict = {}
    if request.session.has_key('logged'):
        id = request.session['logged']
        if str(id).startswith('admin'):
            residents = get_all_residents()
            if request.method == "POST":
                ### DELETE RESIDENT
                modified_residents_list = dict(request.POST.iterlists())['residents_list']
                for v in residents:
                    if str(v[0]) not in modified_residents_list:
                        remove_resident(str(v[0]))
            residents = get_all_residents()
            for resident in residents:
                resident_id = resident[0]
                name = resident[1]
                room = resident[2]
                residents_dict[resident_id] = '{} , {}'.format(name, room)
            return render(request, 'admin.html', {"status": request.session['id'], "residents_list": residents_dict})
        else:
            room = get_room(request.session)
            if room == 'visitor':
                request.session['logged'] = id
                request.session['id'] = id
                valid_black_list = check_in_blacklist(id)
                if valid_black_list:
                    message = 'YOU ARE IN BLACKLIST!'
                visitor_access = get_visitor_access(id)
                for room in visitor_access:
                    resident_id = get_resident_id(str(room[0]))
                    valid_blacklist_resident = check_in_blacklist(resident_id)
                    if valid_blacklist_resident:
                        visitor_access_dict[room[0]] = room[0] + '\t--BLACKLIST--\t'
                    else:
                        visitor_access_dict[room[0]] = room[0]
                return render(request, 'visitor.html',
                              {"status": request.session['logged'], 'visitor_access': visitor_access_dict,
                               'message': message})
            visitors = get_visitors_id_access(room)
            if request.method == "POST":
                ### DELETE VISITOR ACCESS
                modified_visitors_list = dict(request.POST.iterlists())['visitors_list']
                for v in visitors:
                    if str(v[0]) not in modified_visitors_list:
                        remove_visitor_access_by_resident(str(v[0]), room)
                ### ADD NEW VISITOR ACCESS
                new_visitor_id = request.POST['visitor_id']
                if new_visitor_id:
                    valid = check_visitor_exist(new_visitor_id)
                    if valid:
                        add_new_visitor_access(new_visitor_id, room)
                    else:
                        message = 'Visitor Is Not Exist!!'
            visitors = get_visitors_id_access(room)
            for ele in visitors:
                visitor_name = get_visitor_name(ele[0])
                valid_black_list = check_in_blacklist(ele[0])
                if valid_black_list:
                    visitors_dict[str(ele[0])] = visitor_name[0] + '\t--BLACKLIST--\t'
                else:
                    visitors_dict[ele[0]] = visitor_name[0]
            welcome = '{} , {}'.format(get_resident_name(id)[0],room[0])
            return render(request, 'index.html',
                          {"status": request.session['id'], "visitors_list": visitors_dict, 'message': message,'welcome':welcome})
    else:
        return render(request, 'login.html')


def login(request):
    data = {}
    visitors_dict = {}
    residents_dict = {}
    message = ''
    visitor_access = []
    visitor_access_dict = {}
    MyLoginForm = LoginForm()
    context = {'formlogin': MyLoginForm, 'message': ''}
    if request.session.has_key('logged'):
        name = request.session['logged']
        return redirect('../', {"status": name})
    if request.method == "POST":
        # Get the posted form
        if str(request.POST['id']).startswith('admin'):
            MyadminLoginForm = adminLoginForm(request.POST)
            if MyadminLoginForm.is_valid():
                id = MyadminLoginForm.cleaned_data['id']
                password = MyadminLoginForm.cleaned_data['password']
                data['id'] = id
                data['password'] = password
                valid = validate_user(data)
            valid = validate_admin(data)
            if valid:
                request.session['logged'] = id
                request.session['id'] = id
                residents = get_all_residents()
                for resident in residents:
                    resident_id = resident[0]
                    name = resident[1]
                    room = resident[2]
                    residents_dict[resident_id] = '{} , {}'.format(name, room)
                return render(request, 'admin.html',
                              {"status": request.session['id'], "residents_list": residents_dict})
            else:
                context = {
                    'formlogin': MyadminLoginForm,
                    'message': 'Invalid Password Or Id!'}

        else:
            MyLoginForm = LoginForm(request.POST)
            if MyLoginForm.is_valid():
                id = MyLoginForm.cleaned_data['id']
                password = MyLoginForm.cleaned_data['password']
                data['id'] = id
                data['password'] = password
                valid = validate_user(data)
                if valid:
                    user_type = valid['result']
                    if user_type == 'resident':
                        request.session['logged'] = id
                        request.session['id'] = id
                        valid_black_list = check_in_blacklist(id)
                        if valid_black_list:
                            message = 'YOU ARE IN BLACKLIST!'
                        room = get_room(request.session)
                        visitors = get_visitors_id_access(room)
                        visitors_dict = {}
                        for ele in visitors:
                            visitor_name = get_visitor_name(ele[0])
                            valid_black_list = check_in_blacklist(ele[0])
                            if valid_black_list:
                                visitors_dict[str(ele[0])] = visitor_name[0] + '\t--BLACKLIST--\t'
                            else:
                                visitors_dict[ele[0]] = visitor_name[0]
                        return render(request, 'index.html',
                                      {"status": request.session['id'], "visitors_list": visitors_dict,
                                       'message': message})
                    else:
                        request.session['logged'] = id
                        request.session['id'] = id
                        valid_black_list = check_in_blacklist(id)
                        if valid_black_list:
                            message = 'YOU ARE IN BLACKLIST!'
                        visitor_access = get_visitor_access(id)
                        for room in visitor_access:
                            resident_id = get_resident_id(room[0])
                            valid_blacklist_resident = check_in_blacklist(resident_id)
                            if valid_blacklist_resident:
                                visitor_access_dict[room[0]] = room[0] + '\t--BLACKLIST--\t'
                            else:
                                visitor_access_dict[room[0]] = room[0]
                        return render(request, 'visitor.html',
                                      {"status": request.session['logged'], 'visitor_access': visitor_access_dict,
                                       'message': message})

                else:
                    MyLoginForm = LoginForm()
                    context = {
                        'formlogin': MyLoginForm,
                        'message': 'Invalid Password Or Id!'}
    return render(request, 'login.html', context)


def signup(request):
    if request.session.has_key('logged'):
        name = request.session['logged']
        return redirect('../', {"status": name})
    else:
        data = {}
        if request.method == "POST":
            # Get the posted form
            MyRegisterForm = signUpForm(request.POST)
            if MyRegisterForm.is_valid():
                data['id'] = MyRegisterForm.cleaned_data['id']
                data['name'] = MyRegisterForm.cleaned_data['name']
                data['password'] = MyRegisterForm.cleaned_data['password']
                if len(str(data['id'])) != 9:
                    return render(request, 'signup.html', {"status": "Invalid Id number!"})
                valid = validate_new_user(data)
                if valid:
                    sign_up_visitor(data)
                    request.session['logged'] = data['id']

                    return render(request, 'signup.html', {"status": "User SignUp Success!"})
                else:
                    return render(request, 'signup.html', {"status": "User already exists!"})
        return render(request, 'signup.html')


def admin_visitors(request):
    visitors_dict = {}
    if request.session.has_key('logged'):
        id = request.session['logged']
        if str(id).startswith('admin'):
            visitors = get_all_visitors()
            if request.method == "POST":
                ### DELETE VISITOR
                modified_visitors_list = dict(request.POST.iterlists())['visitors_list']
                for v in visitors:
                    if str(v[0]) not in modified_visitors_list:
                        remove_visitor(str(v[0]))
            visitors = get_all_visitors()
            for visitor in visitors:
                visitor_id = visitor[0]
                name = visitor[1]
                visitors_dict[visitor_id] = name
            return render(request, 'admin_visitors.html',
                          {"status": request.session['id'], "visitors_list": visitors_dict})
    return render(request, 'login.html')


def admin_visitors_access(request):
    visitors_access_dict = {}
    if request.session.has_key('logged'):
        id = request.session['logged']
        if str(id).startswith('admin'):
            visitors_access = get_all_visitors_access()
            if request.method == "POST":
                ### DELETE VISITOR
                modified_visitors_access_list = dict(request.POST.iterlists())['visitors_access_list']
                for v in visitors_access:
                    if str(v[3]) not in modified_visitors_access_list:
                        remove_visitor_access(str(v[3]))
            visitors_access = get_all_visitors_access()
            for visitor_access in visitors_access:
                visitor_id = visitor_access[0]
                name = visitor_access[1]
                room = visitor_access[2]
                ind = visitor_access[3]
                visitors_access_dict[ind] = "{} , {} , {}".format(visitor_id, name, room)
            return render(request, 'admin_visitors_access.html',
                          {"status": request.session['id'], "visitors_access_list": visitors_access_dict})
    return render(request, 'login.html')


def add_resident(request):
    if request.session.has_key('logged') and str(request.session['logged']).startswith('admin'):
        name = request.session['logged']
        if request.method == "POST":
            data = {'resident_id': request.POST['id'],
                    'room': request.POST['room'],
                    'name': request.POST['name'],
                    'password': request.POST['password']}
            valid = add_new_resident(data)
            if valid:
                msg = 'Succsees To Add New Resident with Id : ' + str(request.POST['id'])
            else:
                msg = "Resident With Id {} Is Exist!".format(request.POST['id'])
            return render(request, 'add_resident.html', {"status": request.session['id'],
                                                         "msg": msg})
        return render(request, 'add_resident.html', {"status": request.session['id']})

    return render(request, 'login.html')


def logout(request):
    try:
        del request.session['logged']
        del request.session['id']
    except:
        pass
    return redirect('../login', {"status": "Successfully logged out!"})


def blacklist(request):
    message = ''
    blacklist_dict = {}
    if request.session.has_key('logged') and str(request.session['logged']).startswith('admin'):
        users_blacklist = get_all_blacklist()
        if request.method == "POST":
            ### DELETE USERS FROM BLACKLIST
            modified_blacklist = dict(request.POST.iterlists())['blacklist_list']
            for user in users_blacklist:
                if str(user[0]) not in modified_blacklist:
                    remove_user_from_blacklist(user[0])
            ### ADD NEW USER TO BLACKLIST
            new_user_to_blacklist = request.POST['user_id']
            if new_user_to_blacklist:
                if (len(str(new_user_to_blacklist)) < 8 or len(str(new_user_to_blacklist)) > 9):
                    message = 'Invalid ID Number!'
                else:
                    add_to_blacklist(new_user_to_blacklist, request.session['id'])
            users_blacklist = get_all_blacklist()
            for user in users_blacklist:
                user_id = user[0]
                user_type = user[2]
                if user_type == 'resident':
                    user_name = get_resident_name(user_id)[0]
                elif user_type == 'visitor':
                    user_name = get_visitor_name(user_id)[0]
                blacklist_dict[user_id] = "{} , {}".format(user_name, user_type)
            return render(request, 'blacklist.html',
                          {"status": request.session['id'], "blacklist_list": blacklist_dict, 'message': message})
        else:
            for user in users_blacklist:
                user_id = user[0]
                user_type = user[2]
                if user_type == 'resident':
                    user_name = get_resident_name(user_id)[0]
                elif user_type == 'visitor':
                    user_name = get_visitor_name(user_id)[0]
                else:
                    user_name = "UNKNOWN"
                blacklist_dict[user_id] = "{} , {}".format(user_name, user_type)
            return render(request, 'blacklist.html',
                          {"status": request.session['id'], "blacklist_list": blacklist_dict, 'message': message})
    return render(request, 'login.html')


def display_all_logs(request):
    message = ''
    logs_dict = {}
    query_handler_dict = {'1':get_room_logs, '2':get_id_logs, '3':get_date_logs,'0': get_all_log}
    if request.session.has_key('logged') and str(request.session['logged']).startswith('admin'):
        if request.method == "POST" and request.POST['user_id'] != '':
            user_id = request.POST['user_id']
            if request.POST['search_type'] != '0':
                logs_query_handler = query_handler_dict[str(request.POST['search_type'])]
                all_logs = logs_query_handler(user_id)
            else :
                all_logs = get_all_log()
        else:
            all_logs = get_all_log()
        for log in all_logs:
            timestamp = str(log[0].strftime("%Y-%m-%d %H:%M:%S"))
            user_id = str(log[3])
            user_type = get_user_type(user_id)
            if user_type == 'resident':
                user_name = get_resident_name(user_id)
            else:
                user_name = get_visitor_name(user_id)
            room = str(log[2])
            logs_dict[timestamp] = "{0} | {1} | {2}".format(room, user_id, user_name[0])
        return render(request, 'display_all_logs.html',
                      {"status": request.session['logged'], 'logs_list': logs_dict,
                       'message': message})
    return render(request, 'login.html')


def display_resident_logs(request):
    message = ''
    logs_dict = {}
    if request.session.has_key('logged'):
        data = {'id': request.session['logged']}
        room = get_room(data)[0]
        room_logs = get_room_logs(room)
        for log in room_logs:
            timestamp = str(log[0].strftime("%Y-%m-%d %H:%M:%S-%H:%M"))
            user_id = str(log[3])
            user_type = get_user_type(user_id)
            if user_type == 'resident':
                user_name = get_resident_name(user_id)
            else:
                user_name = get_visitor_name(user_id)
            room = str(log[2])
            logs_dict[timestamp] = "{0} | {1} | {2}".format(room, user_id, user_name[0])
        return render(request, 'room_logs.html',
                      {"status": request.session['logged'], 'logs_list': logs_dict,
                       'message': message})
    return render(request, 'login.html')


def display_visitor_logs(request):
    message = ''
    logs_dict = {}
    if request.session.has_key('logged'):
        id = request.session['logged']
        visitor_logs = get_id_logs(id)
        for log in visitor_logs:
            timestamp = str(log[0].strftime("%Y-%m-%d %H:%M:%S-%H:%M"))
            user_id = str(log[3])
            user_name = get_visitor_name(user_id)
            room = str(log[2])
            logs_dict[timestamp] = "{0} | {1} | {2}".format(room, user_id, user_name[0])
        return render(request, 'visitor_logs.html',
                      {"status": request.session['logged'], 'logs_list': logs_dict,
                       'message': message})
    return render(request, 'login.html')


######################################### <MOBILE APP REQUESTS> #############################################################

def login_mobile(request):
    data = request.POST
    valid = validate_user(data)
    if valid:
        results = [valid]
    else:
        results = [{'response': 'failed'}]
    res = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(res, mimetype) 


def visitor_access(request):
    data = request.POST  # {room , id}
    results = [{'response': 'success', 'reason': ''}]
    valid = validate_visitor_access(data)
    resident_id = get_resident_id(data['room'])
    valid_blacklist_resident = check_in_blacklist(resident_id)
    valid_blacklist_visitor = check_in_blacklist(data['id'])
    id = data['id']
    room = data['room']
    if valid:
        if valid_blacklist_resident:
            results = [{'response': 'failed', 'reason': 'resident is in blacklist'}]
        elif valid_blacklist_visitor:
            results = [{'response': 'failed', 'reason': 'visitor is in blacklist'}]
            #os.system(SECURITY_SMS.format(id,room,get_visitor_name(id)[0]))
        if results[0]['response'] == 'success':
            timestamp = datetime.datetime.now()
            date = datetime.date.today()
            insert_new_log(timestamp, date, room, id)
            cmd = RSEIDENT_SMS.format(id,get_visitor_name(id)[0])
            #os.system(cmd)
        res = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(res, mimetype)
    return HttpResponse(status=404)



def resident_access(request):
    data = request.POST  # {id}
    results = [{'response': 'success', 'reason': ''}]
    valid = check_resident_access(data)
    if valid:
        timestamp = datetime.datetime.now()
        date = datetime.date.today()
        id = data['id']
        room = get_room(data)     
        insert_new_log(timestamp, date, room, id)
        res = json.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(res, mimetype)
    return HttpResponse(status=404)


def signup_mobile(request):
    print request.POST
    data = request.POST  # {id,name,password}
    results = [{'response': 'failed', 'reason': ''}]
    valid = validate_new_user(data)
    print data
    print valid
    if valid:
        sign_up_visitor(data)
        results = [{'response': 'success', 'reason': ''}]
    else:
        results = [{'response': 'failed', 'reason': 'User is exist!'}]
    res = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(res, mimetype)


def get_name_mobile(request):
     data = request.POST  # {id}
     user_id = data['id']
     user_name = ''
     user_type = get_user_type(user_id)
     if user_type == 'resident':
         user_name = get_resident_name(user_id)[0]
     else:
         user_name = get_visitor_name(user_id)[0]
     results = [{'name': user_name }]
     res = json.dumps(results)
     mimetype = 'application/json'
     return HttpResponse(res, mimetype)
     
     

################################### HELPER FUNCTIONS #########################################################################################
def add_new_visitor_access(visitor_id, room):
    data = {'id': visitor_id,
            'room': room}
    visitor_access = add_new_access(data)
    return True







from django.shortcuts import render
from forms import *
from query_handler import *


def Index(request):
    context={'name':'Audai Shmalih',
             'age':24,
             'jobs':['Software Developer'],
             }
    return render(request,'index.html',context)


def login(request):
    data = {}
    if request.method == "POST":
        # Get the posted form
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            id = MyLoginForm.cleaned_data['id']
            password = MyLoginForm.cleaned_data['password']
            data['id'] = id
            data['password'] = password
            valid = validate_resident(data)
            if valid:
                #srequest.session['logged'] = id
                return render(request, 'index.html', {"name": 'connected'})
    else:
        MyLoginForm = LoginForm()
    context = {
        'formlogin': MyLoginForm,
        'msg': ''
    }
    # TODO: fix when verification failed
    return render(request, 'login.html', context)



import json
def post_log(request):
    data = request.POST
    print request.POST['id']
    course = data.get("term")
    courses_list = {"hedva":"hedva" , 'linarit':'linarit', 'ddd': 'data struct'}
    autocomplete_results = []
    for course in courses_list.keys():
        course_json = {'id': course, 'label': courses_list[course] + ' (' + course + ')', 'value': courses_list[course]}
        autocomplete_results.append(course_json)
    autocomplete_results.sort(key=lambda course: course['label'])
    data = json.dumps(autocomplete_results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

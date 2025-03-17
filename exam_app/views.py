import bcrypt
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from exam_app.models import Pie, User

# Create your views here.
def index(request):

    return render(request, 'index.html')

def post_register(request):
    postData = request.POST
    errors = User.objects.registery_validator(postData)
    if errors:
        print(errors)
        bad_data = {
            "bad_first_name":postData['first_name'],
            "bad_last_name":postData['last_name'],
            "bad_email":postData['email']

        }
        request.session['bad_data'] = bad_data
        request.session['errors'] = errors
        messages.error(request, 'Registry Failed!')
        return redirect('/')
    first_name = postData['first_name']
    last_name = postData['last_name']
    email = postData['email']
    unhashed_pw = postData['password'].encode()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(unhashed_pw, salt).decode()
    User.objects.create(
        first_name  = first_name,
        last_name = last_name,
        email = email,
        password = hashed_pw,
    )
    request.session.clear()
    messages.success(request, 'Register Successfull! Please Login')
    return redirect('/')

def post_login(request):
    postData = request.POST
    errors = User.objects.login_validator(postData)
    if errors:
        messages.error(request, 'Login Failed!')
        return redirect('/')
    email = postData['email']
    if not User.objects.filter(email = email).exists():
        messages.error(request, 'Login Failed! Email does not exist in DB.')
        return redirect('/')
    user = User.objects.get(email = email)
    password_to_test = postData['password'].encode()
    hashed_pw = (user.password).encode()
    if bcrypt.checkpw(password_to_test, hashed_pw):
        messages.success(request, 'Succesfully Logged In!')
        request.session['current_user_id'] = user.id
        request.session['is_logged_in'] = True
        if request.session.get('errors'):
            request.session.get('errors').clear()
        return redirect('/dashboard')
    messages.error(request, 'Login failed!')
    return redirect('/')

def logout(request):
    request.session.clear()
    request.session['is_logged_in'] = False
    messages.success(request,"Successfully Logged Out!")
    return redirect('/')

def dashboard(request):
    if not request.session.get('is_logged_in'):
        messages.error(request, 'You must be logged in to view this page')
        return redirect('/')
    users = User.objects.all()
    current_user = User.objects.get(id = request.session['current_user_id'])
    pies = Pie.objects.filter(user = current_user)
    context = {
        "pies":pies,
        "users":users,
        "user":current_user
    }
    return render(request, 'dashboard.html', context)
def add_pie(request):
    postData = request.POST
    errors = Pie.objects.pie_validator(postData)
    if errors:
        print(errors)
        bad_data = {
            "bad_pie_name":postData['pie_name'],
            "bad_pie_filling":postData['pie_filling'],
            "bad_pie_crust":postData['pie_crust']
        }
        request.session['bad_data'] = bad_data
        request.session['errors'] = errors
        messages.error(request, 'Pie Creation Failed!')
        return redirect('/dashboard')
    pie_name = postData['pie_name']
    pie_crust = postData['pie_crust']
    pie_filling = postData['pie_filling']
    Pie.objects.create(
        name  = pie_name,
        filling = pie_filling,
        crust = pie_crust,
        user = User.objects.get(id = request.session['current_user_id'])
    )
    if request.session.get('bad_data'):
        del request.session['bad_data']
        del request.session['errors']
    messages.success(request, 'Pie Added Successfully!')
    return redirect('/dashboard')
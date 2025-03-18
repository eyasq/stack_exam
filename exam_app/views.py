import bcrypt
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from exam_app.models import Pie, User, Vote

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
    del request.session['bad_data'] 
    del request.session['errors'] 
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
    del request.session['current_user_id']
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

def all_pies(request):
    pies = Pie.objects.all().order_by('-votes')
    context = {
        "pies":pies
    }
    return render(request,'allpies.html',context)

def show_pie(request, pie_id):
    pie = Pie.objects.get(id = pie_id)
    current_user = User.objects.get(id = request.session['current_user_id'])
    context = {
        'pie' : pie,
        'user':current_user
    }
    
    return render(request, 'show_pie.html', context)

def vote_pie(request, pie_id):
    user = User.objects.get(id = request.session['current_user_id'])
    pie = Pie.objects.get(id = pie_id)
    vote, created = Vote.objects.get_or_create(user=user, pie=pie)
    if created:
        messages.success(request, 'Vote added successfully')
        new_vote_count = int(pie.votes) + 1
        pie.votes = new_vote_count
        pie.save()
        request.session['latest_vote_id'] = vote.id
    else:
        messages.info(request, 'You have already voted for this pie')
    return redirect('/pies')

def remove_vote(request):
    try:
        vote = Vote.objects.get(id = request.session.get('latest_vote_id'))
        pie = vote.pie
        pie.votes = max(0, int(pie.votes) - 1)
        pie.save()
        vote.delete()
        del request.session['latest_vote_id']
        messages.success(request, 'Vote Removed')
    except Vote.DoesNotExist:
        messages.error(request, 'No vote to remove')
    return redirect('/pies')

def edit_pie(request, pie_id):
    pie = Pie.objects.filter(id = pie_id).first()
    if not pie:
        messages.error(request, 'Pie Does Not Exist')
        return redirect('/dashboard')
    pie_owner = pie.user
    current_user = User.objects.get(id = request.session['current_user_id'])
    if not pie_owner == current_user:
        messages.error(request, 'You are not authorized to Edit this pie!!!')
        return redirect('/dashboard')
    context = {
        "pie":pie
    }
    return render(request,'edit_pie.html',context)

def post_edit_pie(request):
    postData = request.POST
    errors = Pie.objects.pie_edit_validator(postData)
    pie = Pie.objects.get(id = postData['pie_id'])
    if errors:
        print(errors)
        bad_data = {
            "bad_pie_name":postData['pie_name'],
            "bad_pie_filling":postData['pie_filling'],
            "bad_pie_crust":postData['pie_crust']
        }
        request.session['bad_data'] = bad_data
        request.session['errors'] = errors
        messages.error(request, 'Pie Editing failed!')
        return redirect(f'/pies/edit/{pie.id}')
    pie.name = postData['pie_name']
    pie.crust = postData['pie_crust']
    pie.filling = postData['pie_filling']
    pie.save()
    messages.success(request, 'Pie Edited Successfully!')
    return redirect('/dashboard')

def delete(request, pie_id):
    pie = Pie.objects.filter(id = pie_id).first()
    pie_owner = pie.user
    current_user = User.objects.get(id = request.session['current_user_id'])
    if not pie_owner == current_user:
        messages.error(request, 'You are not authorized to Delete this pie!!!')
        return redirect('/dashboard')
    pie.delete()
    messages.success(request, 'Succesfully Deleted Pie')
    return redirect('/dashboard')
    
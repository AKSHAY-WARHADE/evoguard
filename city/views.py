from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm , ComplaintForm ,UpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.db.models import Q
from .models import *
from .mail import *
import random

# Create your views here.
def home(request):
    total_complaints=Complaint.objects.count()
    pending=Complaint.objects.all().filter(status='Pending').count()
    solved=Complaint.objects.all().filter(status='Resolved').count()
    new=Complaint.objects.all().filter(status='Submitted').count()
    context={'total_complaints':total_complaints,'pending':pending,'solved':solved,'new':new}
    if request.method=='POST':
        name=request.POST['username']
        email=request.POST['email']
        message=request.POST['message']
        Queries.objects.create(name=name,email=email,message=message)
        
        return redirect('home')
    return render(request,'city/home.html',context=context)

def about(request):

    return render(request,'city/about.html')

def services(request):
    return render(request,'city/services.html')

def login_page(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_user==True:
            login(request,user)
            print(user.is_user)
            # return render(request,"city/login.html")
            return redirect('user_dashboard')
        else:
            messages.info(request,'username or password is incorrect')
        
    return render(request,"city/login.html")
 
def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email=form.cleaned_data['email']
            sub='Account Created Successfully'
            messages.success(request,'Account Created '+ user)
            body=f'Hello {user},\n\tYou have successfully created the user account in Evo Guard. Kindly login to raise the complaints. Hope you will help us to make the city clean and green\n\t\t Thank You\n\nRegards,\nEvo Guard\nPune'
            mail(email,sub,body)
            return redirect('login')
    context={
        'form':form
    }
    return render(request,"city/register.html",context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST,request.FILES)
        if form.is_valid():
            types=form.cleaned_data['complaint_type']
            area=form.cleaned_data['area']
            if request.user.is_authenticated:
                user_email = request.user.email
            else:
                user_email = 'ANON'
            tracking_id=(user_email[0:4]  
                +str(random.randint(100,999))
                +types[0:2]+str(random.randint(0,9))
                +types[-1:-3]+area[0:3]).upper()
            complaint = form.save(commit=False)
            complaint.user_name = request.user if request.user.is_authenticated else None
            complaint.tracking_id=tracking_id
            complaint.save()
            if request.user.is_authenticated:
                email_reciever=request.user.email
                sub='Complaint Registered'
                body=f'Hello {request.user}, \n\tYour complaint on {types} at {area}, It will be solved within two working days. You can track the complaint with this tracking {tracking_id}. \n\nEvo Guard\nPune'
                mail(email_reciever,sub,body,)
                return redirect('user_complaints')
            else:
                request.session['tracking_id'] = tracking_id
                return redirect('complaint_success')
    else:
        form = ComplaintForm()
    return render(request, 'city/complaint.html', {'form': form})

def complaint_success(request):
    tracking_id = request.session.get('tracking_id')  # Retrieve tracking_id from session
    if tracking_id:
        return render(request, 'city/complaint_success.html', {'tracking_id': tracking_id})
    else:
        return render(request, 'city/complaint_success.html')  # Render without tracking_id

@login_required(login_url='login')
def user_dashboard(request):
    return render(request,'city/user_dashboard.html')

@login_required(login_url='login')
def user_complaints(request):
    complaint=Complaint.objects.all().filter(user_name=request.user).order_by('-complaint_date')
    return render(request,'city/user_complaints.html',{'complaint':complaint})

@login_required(login_url='login')
def user_profile(request):
    return render(request,'city/user_profile.html')

@login_required(login_url='login')
def save_profile(request):
    if request.method == 'POST':
        # Process the form data and save the profile changes
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        

        # Update the user's profile information
        request.user.first_name = first_name
        request.user.last_name = last_name
        
        request.user.save()

        # Redirect to a success page or the user profile page
        return redirect('user_profile')  # Assuming you have a URL pattern named 'user_profile'

    # Handle GET requests or invalid form submissions
    # You may want to display an error message or handle the situation differently
    return redirect('user_profile')  # Redirect back to the user profile page

@login_required(login_url='login')
def user_settings(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            auth.logout(request)  # Logout the user
            messages.success(request, 'Your password was successfully updated. Please log in with your new password.')
            return JsonResponse({'success': True})
        else:
            errors = dict(form.errors.items())
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'city/user_settings.html', {'form': form})


def employee_login(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        
        if user is not None and user.is_employee==True:
            login(request,user)
            print(user.is_employee)
            # return render(request,"city/login.html")
            return redirect('emp_main')
        else:
            messages.info(request,'username or password is incorrect')
    
    return render (request,'city/employee_login.html')

@login_required(login_url='employee_login')
def emp_main(request):
    if request.user.is_employee==True:
        new=Complaint.objects.all().filter(status='Submitted').count()
        pending=Complaint.objects.all().filter(status='Pending').count()
        solved=Complaint.objects.all().filter(status='Resolved').count()
        query=Queries.objects.all().count()
        context={
            'new':new,
            'pending':pending,
            'solved':solved,
            'query':query
        }
        return render(request,'city/emp_main.html',context=context)
    else:
        return redirect('employee_login')


@login_required(login_url='employee_login')
def new_complaints(request):
    
    if request.user.is_employee==True:
        new=Complaint.objects.all().filter(status='Submitted')
        return render(request,'city/new_complaints.html',{'new':new})
    else:
        return redirect('employee_login')
    
@login_required(login_url='employee_login')
def pending_complaints(request):
    
    if request.user.is_employee==True:
        pending=Complaint.objects.all().filter(status='Pending')
        return render(request,'city/pending_complaints.html',{'pending':pending})
    else:
        return redirect('employee_login')

@login_required(login_url='employee_login')
def solved_complaints(request):
    
    if request.user.is_employee==True:
        solved=Complaint.objects.all().filter(status='Resolved')
        return render(request,'city/solved_complaints.html',{'solved':solved})
    else:
        return redirect('employee_login')



@login_required(login_url='employee_login')
def update_new_complaints(request,pk):
    
    if request.user.is_employee==True:
        complaints=Complaint.objects.get(id=pk)
        form =UpdateForm(instance=complaints)
        context={
            'form':form
        }
        if request.method=='POST':
            form=UpdateForm(request.POST,instance=complaints)
            if form.is_valid():
                form.save()
                return redirect('new_complaints')
        return render(request,'city/update_complaints.html',context=context)
    else:
        return redirect('employee_login')

@login_required(login_url='employee_login')
def update_pending_complaints(request,pk):
    
    if request.user.is_employee==True:
        complaints=Complaint.objects.get(id=pk)
        form =UpdateForm(instance=complaints)
        context={
            'form':form
        }
        if request.method=='POST':
            form=UpdateForm(request.POST,instance=complaints)
            if form.is_valid():
                email_reciever=complaints.user_name.email
                sub='Complaint Resolved'
                body=f'Hello {complaints.user_name}, \nYour complaint on {complaints.complaint_type} at {complaints.area} has been resolved. \n\t\tThank You\nEvo Guard'
                form.save()
                #mail(email_reciever,sub,body)
                return redirect('pending_complaints')
        return render(request,'city/update_complaints.html',context=context)
    else:
        return redirect('employee_login')


@login_required(login_url='employee_login')
def update_solved_complaints(request,pk):
    
    if request.user.is_employee==True:
        complaints=Complaint.objects.get(id=pk)
        form =UpdateForm(instance=complaints)
        context={
            'form':form
        }
        if request.method=='POST':
            form=UpdateForm(request.POST,instance=complaints)
            if form.is_valid():
                form.save()
                return redirect('solved_complaints')
        return render(request,'city/update_complaints.html',context=context)
    else:
        return redirect('employee_login')


@login_required(login_url='employee_login')
def queries(request):
    if request.user.is_employee==True:
        queries=Queries.objects.all()
        if request.method=='POST':
            queries.all().delete()
            return redirect('queries')
        return render (request,'city/queries.html',{'queries':queries})
    else:
        return redirect('employee_login')

def check_status(request):
    if request.method=='POST':
        tracking_id=request.POST['id']
        try:
            complaints=Complaint.objects.get(tracking_id=tracking_id)
            return render(request,'city/check_status.html',{'complaints':complaints})
        except:
            messages.warning(request,'Invalid Tracking ID')
    return render(request,'city/check_status.html')

@login_required(login_url='employee_login')
def search_complaints(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        if query:
            # Perform search operation based on the query
            complaints = Complaint.objects.filter(
                Q(area__icontains=query) |
                Q(city__icontains=query) |
                Q(pincode__icontains=query) |
                Q(complaint_type__icontains=query)
            )
        else:
            complaints = Complaint.objects.all()

        return render(request, 'city/complaint_search_results.html', {'complaints': complaints, 'query': query})

    return render(request, 'city/complaint_search_results.html', {'complaints': None, 'query': ''})

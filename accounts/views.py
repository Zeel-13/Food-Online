from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .utils import detectUser
# Create your views here.
def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in !")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.set_password(password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request,"Your account has been created successfully !")
            return redirect('registerUser')
        else:
            print('Form is invalid')
            print(form.errors)
    else:
        form=UserForm()
    context={
        'form':form
    }
    return render(request, 'accounts/registerUser.html',context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in !")
        return redirect('myAccount')
    elif request.method=="POST":
        form=UserForm(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.set_password(password)
            user.role=User.VENDOR
            user.save()
            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,"Your account has been created successfully ! Please Wait for the approval")
            return redirect('registerVendor')
        else:
            print('Form is invalid')
            print(form.errors)
    else:
        form=UserForm()
        v_form=VendorForm()
    context={
        'form':form,
        'v_form':v_form
    }
    return render(request, 'accounts/registerVendor.html',context)

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in !")
        return redirect('myAccount')
    elif request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are now Logged in....")
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"You are now Logged out....")
    return redirect('login')

@login_required(login_url='login')
def customerDashboard(request):
    if request.user.role!=User.CUSTOMER:
        messages.error(request,"You are not authorized to view this page")
        return redirect('myAccount')
    return render(request,'accounts/customerdashboard.html')

@login_required(login_url='login')
def vendorDashboard(request):
    if request.user.role!=User.VENDOR:
        messages.error(request,"You are not authorized to view this page")
        return redirect('myAccount')
    return render(request,'accounts/vendordashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

from django.shortcuts import render,HttpResponse,redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .utils import detectUser,send_verefication_email,send_password_reset_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
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
            send_verefication_email(request,user)
            messages.success(request,"Your account has been created successfully ! Please Wait for the approval")
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


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Congratulations! your account is activated')
        return redirect('myAccount')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('myAccount')


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
            send_verefication_email(request,user)
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


def forgot_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            send_password_reset_email(request,user)
            messages.success(request,'Password reset email has been sent to your email')
            return redirect('login')
        else:
            messages.error(request,'Email does not exists')
            return redirect('forgot_password')
    return render(request,'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,"Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request,"Thw link has been expired")
        return redirect('myAccount')

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,"Password reset successfully")
            return redirect('login')
        else:
            messages.error(request,"Passwords do not match")
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')
from django.shortcuts import render,get_object_or_404,redirect
from accounts.forms import UserProfileForm
from .forms import VendorForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
# Create your views here.

def get_vendor(request):
    vendor=Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='/accounts/login/')
def v_profile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor=get_object_or_404(Vendor,user=request.user)

    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,"Restaurant Details Updated Successfully")
            return redirect(v_profile)
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=UserProfileForm(instance=profile)
        vendor_form=VendorForm(instance=vendor)
    
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor':vendor,
    }
    return render(request,'vendor/v_profile.html',context)

@login_required(login_url='/accounts/login/')
def menu_builder(request):
    vendor=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor).order_by('created_at')
    context={
        'categories':categories
    }
    return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='/accounts/login/')
def food_items_by_category(request,pk=None):
    vendor=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    food_items=FoodItem.objects.filter(category=category,vendor=vendor)
    # print(food_items)
    context={
        'food_items':food_items,
        'category':category,
    }
    return render(request,'vendor/food_items_by_category.html',context)

@login_required(login_url='/accounts/login/')
def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            category.save()
            messages.success(request,"Category Added Successfully")
            return redirect('menu_builder')
    else:
        form=CategoryForm()
    context={
        'form':form,
    }
    return render(request,'vendor/add_category.html',context)

@login_required(login_url='/accounts/login/')
def edit_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            category.save()
            messages.success(request,"Category Updated Successfully")
            return redirect('menu_builder')
    else:
        form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category,
    }
    return render(request,'vendor/edit_category.html',context)

@login_required(login_url='/accounts/login/')
def delete_category(request,pk=None):
    category=get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,"Category Deleted Successfully")
    return redirect('menu_builder')

@login_required(login_url='/accounts/login/')
def add_food(request):
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title=form.cleaned_data['food_title']
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(food_title)
            form.save()
            messages.success(request,"Food Item Added Successfully")
            return redirect('food_items_by_category',food.category.id)
    else:
        form=FoodItemForm()
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
    context={'form':form}
    return render(request,'vendor/add_food.html',context)

@login_required(login_url='/accounts/login/')
def edit_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    if request.method=='POST':
        form=FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food_title=form.cleaned_data['food_title']
            food=form.save(commit=False)
            food.vendor=get_vendor(request)
            food.slug=slugify(food_title)
            food.save()
            messages.success(request,"Food Ttem Updated Successfully")
            return redirect('food_items_by_category',food.category.id)
    else:
        form=FoodItemForm(instance=food)
        form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))

    context={
        'form':form,
        'food':food, 
    }
    return render(request,'vendor/edit_food.html',context)


@login_required(login_url='/accounts/login/')
def delete_food(request,pk=None):
    food=get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,"Food Item Deleted Successfully")
    return redirect('food_items_by_category',food.category.id)

from django.urls import path
from .views import *

urlpatterns = [
    path('registerUser/',registerUser,name="registerUser"),
    path('registerVendor/',registerVendor,name="registerVendor"),
    path('myAccount/',myAccount,name="myAccount"),


    path('login/',login,name="login"),
    path('logout/',logout,name="logout"),
    path('customerDashboard/',customerDashboard,name="customerDashboard"),
    path('vendorDashboard/',vendorDashboard,name="vendorDashboard"),

]
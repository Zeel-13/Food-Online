
from django.urls import path,include
from .views import *
from accounts import views as AccountViews
urlpatterns = [
    path('profile/',v_profile,name="v_profile"),
    path('',AccountViews.vendorDashboard,name="vendor"),
]
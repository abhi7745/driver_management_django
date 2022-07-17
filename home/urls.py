from django.urls import path,include, re_path
from . import views


urlpatterns=[
    path("",views.index,name="index"),
    path("contact_form",views.contact_form,name="contact_form"),
    path("signup",views.signup,name="signup"),
    path("login",views.loginpage,name="login"),
    path("logout",views.logoutpage,name="logout"),
    # forgot_password
    path("forgot_password",views.forgot_password,name="forgot_password"),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('password_reset/',views.password_reset,name='password_reset'),

    # driver area
    path("add_trip",views.add_trip,name="add_trip"),

    # path("api_location",  views.api_location, name="api_location"),

    # path("add_route/<int:pk>",views.add_route,name="add_route"),
    path("recent_triplist",views.recent_triplist,name="recent_triplist"),
    path("recent_trip/<int:pk>",views.recent_trip,name="recent_trip"),

    # admin area
    path("dashboard",views.dashboard,name="dashboard"),
    path("driver_list",views.driver_list,name="driver_list"),
    path("trip_list",views.trip_list,name="trip_list"),
    path("dutyslip/<int:pk>",views.dutyslip,name="dutyslip"),
    ]
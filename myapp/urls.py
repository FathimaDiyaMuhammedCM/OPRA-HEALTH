
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('logout1/',views.logout1),

    path('adminhome/',views.adminhome),


    path('view_users/',views.view_users),

    path('view_complaints/',views.view_complaints),
    path('send_reply/<id>',views.send_reply),
    path('send_reply_post/',views.send_reply_post),
   
    path('view_feedback/',views.view_feedback),
    path('admin_change_password/',views.admin_change_password),
    path('admin_change_password_post/',views.admin_change_password_post),
    path('and_forget_password/',views.and_forget_password),
    path('and_forget_password_post/',views.and_forget_password_post),


    #Mentor

    path('user_login/', views.login_flut),
    path('user_viewprofile/', views.user_view_profile),
    path('android_forget_password_post/', views.android_forget_password_post),



   

    path('User_sendchat/', views.User_sendchat),
    path('User_viewchat/', views.User_viewchat),

    path('save_facial_emotion/', views.save_facial_emotion),

    #women

    path('user_register/', views.user_register),
    path('user_view_profile/', views.user_view_profile),
    path('user_edit_profile/', views.user_edit_profile),



    path('User_viewchat1/', views.User_viewchat1),
    path('User_sendchat1/', views.User_sendchat1),

    path('add_complaint/', views.add_complaint),
    path('woman_view_complaints/', views.user_view_complaints),
    path('add_feedback/', views.add_feedback),

  
    path('predict_emotion/', views.predict_emotion),


    path('user_view_symptoms/', views.user_view_symptoms),
    path('predictdiseasebysymptoms/', views.predictdiseasebysymptoms),


]

from django.urls import path
from .views import  PostDetail , Home , PostCreate ,Dashboard,PostUpdate,PostDelete ,PostComment
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'blog'

urlpatterns = [
    
    path('', login_required(Home.as_view(template_name = 'blog/home.html')) , name = 'home'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html') , name = 'login'),
    path('logout/', auth_views.LogoutView.as_view() , name = 'logout'),
    path('dashboard/', staff_member_required(Dashboard.as_view()) , name = 'dashboard'),
    path('post/<int:pk>/delete/', PostDelete.as_view() , name = 'post_delete'),
    path('post/<int:pk>/update/', PostUpdate.as_view() , name = 'post_update'),
    path('newpost/', PostCreate.as_view() , name = 'newpost'),
    path('post/<int:pk>/', PostDetail.as_view() ,  name='post_detail'),
   
]

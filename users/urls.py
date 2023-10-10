from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,AddView,ListView,UpdateView,DeleteView

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserView.as_view()),
    path('logout',LogoutView.as_view()),
    path('add',AddView.as_view()),
    path('list',ListView.as_view()),
    path('update',UpdateView.as_view()),
    path('delete',DeleteView.as_view()),

]
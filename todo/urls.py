from django.urls import path
from . import views

urlpatterns = [
    path('', views.ToDoListView.as_view(), name='home'),
    path('update/<str:pk>', views.ToDoDetailView.as_view(), name='detail'),
    path('create/', views.ToDoCreateView.as_view(), name='create'),
    path('<pk>/delete/', views.ToDoDeleteView.as_view(), name='delete'),
    path('<pk>/update/', views.ToDoUpdateView.as_view(), name='update'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('complete/<str:pk>/', views.update_task, name='complete')
]

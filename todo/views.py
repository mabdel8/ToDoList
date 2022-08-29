from http.client import HTTPResponse
from django.shortcuts import render, redirect
from .models import Task
from django.views.generic.list import ListView
from django.http import request
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegisterForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

# Create your views here.
class ToDoListView(ListView):
  model = Task
  context_object_name = 'task_list'

  def get_queryset(self):
    query = self.request.GET.get('q', default='')
    object_list = Task.objects.filter(
      Q(name__icontains=query) | Q(description__icontains=query)
    )
    return object_list



class ToDoDetailView(DetailView):
  model = Task
  context_object_name = 'task'


class ToDoCreateView(LoginRequiredMixin,CreateView):
  login_url = '/login'
  model = Task
  fields = ['name', 'description']
  
  #tell django that the user is the user from the request
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_success_url(self):
    return reverse('home')

class ToDoDeleteView(DeleteView):
  model = Task
  context_object_name = 'task'
  success_url = '/'

  template_name = 'todo/task_confirm_delete.html'

class ToDoUpdateView(UpdateView):
  model = Task
  fields = ['name', 'description', 'user']
  template_name_suffix = '_update_form'
  success_url = '/'

class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'todo/register.html'
  success_url = reverse_lazy('login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"

def login_request(request):
  if request.user.is_authenticated:
    return redirect('/')

  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}.")
        return redirect("/")
      else:
        messages.error(request,"Invalid username or password.")
    else:
      messages.error(request,"Invalid username or password.")
  form = AuthenticationForm()
  return render(request=request, template_name="todo/login.html", context={"login_form":form})

def logout_request(request):
  logout(request)
  messages.info(request, "You have successfully logged out.") 
  return redirect("/")


def update_task(request, pk):
  task = Task.objects.get(pk=pk)

  if task.completed:
    task.completed = False
    task.save()
  else:
    task.completed = True
    task.save()
  
  return redirect('/')

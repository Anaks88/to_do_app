from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from .models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import task
from .serializers import taskserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class customloginview(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True    #to prevent user from login again

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class Registratin(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(Registratin,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Registratin,self).get(*args,**kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model = task
    template_name = "task_list.html"
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search_area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input  # to add to template
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = task
    template_name = "detail.html"
    context_object_name = 'task'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = task
    fields = ['title','description','complete']
    template_name = "create.html"
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = task
    fields = ['title','description','complete']
    template_name = 'create.html'
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = task
    fields = '__all__'
    template_name = 'delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

@api_view(['GET'])
def getdata(request):
    tasks = task.objects.all()
    serializer = taskserializer(tasks,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addtask(request):
    serializer = taskserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def dlttask(request,pk):
    taskk = task.objects.get(id=pk)
    taskk.delete()
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','PUT','DELETE'])
def allop(request,id):
    try:
        taskk = task.objects.get(pk=id)
    except task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        serializer = taskserializer(taskk)
        return Response(serializer.data)
    elif request.method =='PUT':
        serializer = taskserializer(taskk,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method =='DELETE':
        taskk.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)












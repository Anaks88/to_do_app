from django.urls import path
from . import views
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,customloginview,Registratin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/',customloginview.as_view(),name='login'),
    path('register/',Registratin.as_view(),name='registration'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',TaskList.as_view(),name='tasks'),
    path('task/<int:pk>/',TaskDetail.as_view(),name='task_detail'),
    path('create_task/',TaskCreate.as_view(),name='task_create'),
    path('task_updt/<int:pk>/',TaskUpdate.as_view(),name='task_update'),
    path('task_dlt/<int:pk>/',TaskDelete.as_view(),name='task_delete'),
    path('rest/',views.getdata),
    path('add/',views.addtask),
    path('dlt/<int:pk>',views.dlttask),
    path('all/<int:id>',views.allop),
]
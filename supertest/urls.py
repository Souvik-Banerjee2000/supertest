"""supertest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from superapp.views import home, register, startupinfo, login, logout, search,cretaeGroup,viewallgroups,group_details,searchforagroup,searchgroup,joingroup,leavegroup,createpost,viewposts,ideasubmission
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('startupinfo/', startupinfo, name='startupinfo'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('search/', search, name='search'),
    path('creategroup/',cretaeGroup,name = 'creategroup'),
    path('viewallgroups/',viewallgroups,name= 'viewallgroups'),
    path('viewallgroups/details/<id>/',group_details,name = 'group_details'),
    path('searchforagroup/',searchforagroup,name = 'searchforagroup'),
    path('searchgroup/',searchgroup,name='searchgroup'),
    path('searchgroup/details/<id>',group_details,name = 'group_details'),
    path('searchgroup/details/join/<id>/',joingroup,name = 'joingroup'),
    path('viewallgroups/details/<id>/leave/', leavegroup, name='leavegroup'),
    path('viewallgroups/details/<id>/createpost/', createpost, name='createpost'),
    path('viewallgroups/details/<id>/viewposts/',viewposts, name='viewpostspost'),
    path('ideasubmission/',ideasubmission,name='ideasubmission')
]

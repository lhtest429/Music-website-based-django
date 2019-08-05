"""MyMusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from music import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    # 数据库已有数据
    path('get_data/', views.get_data, name='get_data'),
    # 首页
    path('', views.index, name="index"),
    # path('login/', views.Login.as_view(), name="login"),
    # 推荐
    # path('rec/', views.recommend, name="recommend"),
    # 歌单
    path('songlist/', views.songlist, name="songlist"),
    # 榜单
    path('list/', views.list, name="list"),
    # MV
    path('mv/', views.MV_view, name="mv"),
    # MV详情
    path('mv/<int:mv_id>', views.mv_detail, name="mv_detail"),
    # 搜索
    path('search/', views.search, name="search"),
    # 歌单详情
    path('detail/<int:songlist_id>/', views.song_list_detail, name="detail"),
    # rotate
    path('rotate/<int:rotate_id>/', views.rotate_view, name="rotate"),
    # 测试
    path('test/', views.test, name="test"),
    # 登陆
    path('login/', views.login, name="login"),
    # 注册
    path('register/', views.register, name="register"),

    # 管理员
    path('admin/', views.admin, name='admin'),
    path('admin_music/', views.admin_music, name='admin_music'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('admin_mv/', views.admin_mv, name='admin_mv'),
]

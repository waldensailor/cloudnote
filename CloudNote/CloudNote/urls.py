"""CloudNote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from main_view import views
from django.conf.urls import url, include
from django.contrib.auth import urls as auth_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include(auth_urls, namespace='accounts')),
    url(r'^login/', views.return_login),
    url(r'^logout/', views.return_logout),
    url(r'^regist/', views.return_regist),
    url(r'^regist_deal/', views.regist_deal),
    url(r'^index/', views.index),
    url(r'^red/', views.return_readmore),
    url(r'^editor/', views.return_editor),
    url(r'^aboutme/', views.return_aboutme),
    url(r'^test/', views.return_test),
    url(r'^editor_storage/', views.editor_storage),
    url(r'^article_update/', views.article_update),
    url(r'^read_article/', views.read_article),
    url(r'^delete_article/', views.delete_article),
    url(r'^search_article/', views.search_article),
    url(r'^tag_manage/', views.tag_manage),
    url(r'^about_me/', views.about_me),
    url(r'^me_update/', views.me_update),
    url(r'^change_password/', views.change_password),
    url(r'^delete_tag/', views.delete_tag),
    url(r'^update_tag/', views.update_tag),
    url(r'^search_from_tag/', views.search_from_tag),
    url(r'^search_from_content/', views.search_from_content),
    url(r'^img_update/', views.img_update),
]

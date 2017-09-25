# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/1.11/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.conf.urls import url,
# include
#     2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new, name='new'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^update/(?P<recipe_id>[0-9]+)/$', views.update, name='update'),
    url(r'^like/(?P<recipe_id>[0-9]+)/$', views.like, name='like'),
    url(r'^unlike/(?P<recipe_id>[0-9]+)/$', views.unlike, name='unlike'),
    url(r'^add_to_cookbook/(?P<recipe_id>[0-9]+)/$', views.add_to_cookbook,
        name='add_to_cookbook'),
    url(r'^remove_from_cookbook/(?P<recipe_id>[0-9]+)/$',
        views.remove_from_cookbook, name='remove_from_cookbook'),
    url(r'^mycookbook$', views.mycookbook, name='mycookbook'),
    url(r'results$', views.search, name='results'),
]

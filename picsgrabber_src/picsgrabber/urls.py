from django.conf.urls import patterns, include, url
from django.contrib import admin
from webapp import views


urlpatterns = patterns('',
            url(r'^$', include('webapp.urls')),
            url(r'^accounts/', include(admin.site.urls)),
            url(r'^admin/', include(admin.site.urls)),
            url(r'^reddit/$', views.reddit, name='reddit'),
            url(r'^reddit/(?P<sort>\w+)/$', views.reddit, name='reddit'),
            url(r'^imgur/$', views.imgur, name='imgur'),
            url(r'^imgur/(?P<section>\w+)/(?P<sort>\w+)/(?P<page>\d+)/$', views.imgur, name='imgur'),

            url(r'^post/$', views.post_list, name='post_list'),
            url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
            url(r'^post/new/$', views.post_new, name='post_new'),
            # url(r'^post/create_post/$', views.create_post, name='create_post'),
            url(r'^create_post/$', views.create_post, name='create_post'),
)

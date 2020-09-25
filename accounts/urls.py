from django.conf.urls import url
from accounts.views import RegisterView, LoginView, AuthenticatedView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^$', RegisterView.as_view(), name='register'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^authenticated/$', AuthenticatedView.as_view(), name='authenticated'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]

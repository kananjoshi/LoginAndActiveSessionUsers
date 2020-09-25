from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic.edit import FormView
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from accounts.forms import UserRegisterForm
from accounts.models import UserProfile


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        user = form.save(True)
        description = form.cleaned_data.get('description')
        phne_no = form.cleaned_data.get('phone_no')
        UserProfile.objects.create(user=user, description=description, phone_no=phne_no)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/authenticated/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


# Method to get currently active login session users

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


class AuthenticatedView(TemplateView):
    template_name = 'auth.html'
    context_object_name = 'user'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                active_users = get_all_logged_in_users()
                return render_to_response('auth.html', {'users': active_users,'is_admin':True})

            else:
                return render_to_response('auth.html', {'user': request.user})

        # return super(ProtectedView, self).dispatch(*args, **kwargs)

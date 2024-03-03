from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

def is_admin(user):
    newuser =User.objects.get(username=user.username)
    if newuser.groups.filter(name='Admin').exists():
        print('exists')
        return True
    else:
        print('admin doesnt exist')
        return False

def admin_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped_view



def is_student(user):
    newuser =User.objects.get(username=user.username)
    if newuser.groups.filter(name='Student').exists():
        return True
    else: 
        return False

def student_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not is_student(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped_view
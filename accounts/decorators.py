from django.http import HttpResponseForbidden
from functools import wraps


def pharmacist_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'pharmacist':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")

    return _wrapped_view


def supplier_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'supplier':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")

    return _wrapped_view
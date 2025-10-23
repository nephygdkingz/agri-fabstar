from django.shortcuts import redirect
from functools import wraps

def redirect_authenticated(to='dashboard'):
    """Redirect authenticated users to a given URL name."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(to)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

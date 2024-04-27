from django.contrib.auth.decorators import user_passes_test

# Decorator to restrict access to superusers only
def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser,
        login_url='login_' 
    )(view_func)
    return decorated_view_func

# from functools import wraps
# from django.shortcuts import redirect
#
#
# def custom_login_required(view_func):
#     @wraps(view_func)
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return view_func(request, *args, **kwargs)
#         else:
#
#             return redirect('Orders:HomePage')
#
#     return wrapper

import functools
from django.shortcuts import redirect
from django.contrib import messages

def check_is_seller(view_func, reirect_url = 'becomeSeller'):
    """ 
        This decorator checks if the user is seller or not
    """
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_seller:
            return view_func(request, *args, **kwargs)
        messages.info("You Are Not A Seller")
        return redirect(reirect_url)
    return wrapper
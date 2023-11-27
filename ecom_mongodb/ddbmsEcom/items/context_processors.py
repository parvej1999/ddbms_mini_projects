from . import views
def cart_count(request):
    cart_list = views.get_cart_item(request.user)
    return {
        "cart_items":cart_list
    }
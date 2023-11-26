from django.urls import path
from . import views as itemViews

urlpatterns = [
    path("", itemViews.home, name = 'home'),
    path("createNewItem", itemViews.createItem, name="createNewItem"),
    path("addItem/", itemViews.add_to_cart, name = "addToCart"),
    path("cart/", itemViews.show_cart, name='showCart'),
    path('remove/', itemViews.remove_cart_item, name='remove_cart')
]
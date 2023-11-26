from django.shortcuts import render, redirect
from .models import item, cart
from django.contrib.auth.decorators import login_required
from accounts.decorators import check_is_seller
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def home(request):
    items = item.objects.all()
    
    context = {
        'items': items,
    }
    if request.user.is_authenticated:
        pass
    return render(request, "items/items.html", context)

@login_required
@check_is_seller
def createItem(request):
    if request.method == "POST":
        title = request.POST.get("title")
        discription = request.POST.get("discription")
        price = request.POST.get("price")
        category = request.POST.get("category")
        prodImage = request.FILES.get("prodImage")
        
        createdBy = request.user
        print(request.POST)
        instance = item(
            title = title,
            discription = discription,
            price = price,
            category = category,
            prodImage = prodImage,
            addedBY = createdBy,
        )
        instance.save()
        print('image=',instance.prodImage)
        return redirect('home')
    return render(request, "items/createItems.html")

def add_to_cart(request):
    if request.method == 'POST':
        prodId = request.POST.get('prod_id')
        prod = item.objects.get(pk = prodId)
        try:
            cart_item = cart.objects.get(item=prod)
        except:
            cart_item = None
        if  cart_item:
            cart_item.quantity += 1
            cart_item.save()    
            print('quantity added')
            return redirect('home')
        print('product id=',prodId,cart_item)

        user = request.user
        price = prod.price
        instance = cart(
            item = prod,
            user = user,
            price = price,
        )
        print('--------add item------------')
        instance.total_price += price
        instance.save()
        # print(instance)
        return redirect("home")
    return redirect("home")

def remove_cart_item(request):
    if request.method == "POST":
        item_id =  request.POST.get("prod_id")
        cart_item = cart.objects.get(id=item_id )
        cart_item.delete()
    return redirect('showCart')

def show_cart(request):
    cart_items = cart.objects.filter(user = request.user)
    context = {
        'cart_list':cart_items,
    }
    return render(request, 'items/cartList.html', context)
from django.shortcuts import render, redirect
from .models import item, cart
from django.contrib.auth.decorators import login_required
from accounts.decorators import check_is_seller
from django.contrib.auth import get_user_model
from pymongo import MongoClient
from bson.objectid import ObjectId
from ddbmsEcom import settings
import datetime
import base64
import os

User = get_user_model()

def connect():
    client = MongoClient(
        settings.mongodb['host'],
        settings.mongodb['port'],
        
    )
    return client

def get_cart_item(cart_user):
    client = connect()
    item_db = client[settings.mongodb.get('db-name')]
    cart_collection = item_db[settings.mongodb.get('cart_collection')]
    # cart_user_id = ObjectId(str(cart_user.pk))
    # user_id = ObjectId(cart_user.pk)
    user_cart = cart_collection.find_one({"user_id":cart_user.pk})
    if user_cart:
        cart_items = user_cart.get("items", [])
        print(cart_items)
        return cart_items
    return None

# Create your views here.
def home(request):
    client = connect()
    items_db = client[settings.mongodb['db-name']]
    item_collection = items_db['product']
    items = item_collection.find()
    # items = item.objects.all()
    # print(items)
    context = {
        'items': items,
    }
    # if request.user.is_authenticated:
    #     pass
    return render(request, "items/items.html", context)



@login_required
@check_is_seller
def createItem(request):
    client = connect()
    items_db = client[settings.mongodb['db-name']]
    item_collection = items_db[settings.mongodb['item_collection']]
    if request.method == "POST":
        title = request.POST.get("title")
        discription = request.POST.get("discription")
        price = request.POST.get("price")
        category = request.POST.get("category")
        prodImage = request.FILES.get("prodImage")

        encoded_image = base64.b64encode(prodImage.read()).decode("utf-8")
        
        createdBy = request.user
        instance = {
            'title': title,
            'discription' : discription,
            'price' : price,
            'category' : category,
            'prodImage' : encoded_image,
            'user' : {
                'pk':createdBy.pk,
                'user_name':createdBy.username,
                },
            'createdAt':datetime.datetime.now()
        }
        item_collection.insert_one(instance)
        return redirect('home')
    return render(request, "items/createItems.html")

@login_required
def add_to_cart(request):
    client = connect()
    item_db = client[settings.mongodb['db-name']]
    item_collection = item_db[settings.mongodb['item_collection']]
    cart_collection = item_db[settings.mongodb['cart_collection']]
    if request.method == 'POST':
        prodId = request.POST.get('prod_id')
        user = request.user
        user_id = user.pk
        user_cart = cart_collection.find_one({'user_id':user_id})
        objInstance = ObjectId(prodId)
        new_item = item_collection.find_one({'_id':objInstance})
        if user_cart:
            updated_items = user_cart.get("items", [])+[new_item]
            cart_collection.update_one(
                {'user_id':user_id},
                {'$set':{"items":updated_items}}
            )
        else:
            new_cart = {
                'user_id':user_id,
                'items':[new_item]
            }
            cart_collection.insert_one(new_cart)

        
    return redirect("home")

@login_required
def remove_cart_item(request):
    
    if request.method == "POST":
        client = connect()
        item_db = client[settings.mongodb.get('db-name')]
        item_collection = item_db[settings.mongodb.get('item_collection')]
        cart_collection = item_db[settings.mongodb.get('cart_collection')]

        item_id =  request.POST.get("prod_id")
        item_id = ObjectId(item_id)
        user_id = request.user.pk
        item = item_collection.find_one({
            "_id":item_id
        })
        user_cart = cart_collection.find_one({
            "user_id":user_id
        })
        cart_items = user_cart.get('items',[])
        if item in cart_items:
            cart_items.remove(item)
            cart_collection.update_one(
                {'user_id':user_id},
                {'$set':{'items':cart_items}}
            )

    return redirect('showCart')

@login_required
def show_cart(request):
    
    cart_items = get_cart_item(request.user)

    # cart_items = cart.objects.filter(user = request.user)
    context = {
        'cart_list':cart_items,
    }
    return render(request, 'items/cartList.html', context)
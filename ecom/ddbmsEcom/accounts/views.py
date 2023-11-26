from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from . import models 

User = get_user_model()

# Create your views here.
def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            print(request.method)
            user_id = request.POST.get('user_id')
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            password = request.POST.get('pass')
            email = request.POST.get('email')
            instance = User.objects.create_user(username = user_id, email=email, password=password)
            instance.first_name=fname
            instance.last_name=lname
            instance.save()
            user = authenticate(request, username=user_id, password = password)
            login(request, user)
            return redirect('home')
    # else:
        return render(request, "accounts/sign_up.html")
    return redirect("home")

def auth(request):
    print('login')
    if not request.user.is_authenticated:
        if request.method == 'POST':
            userId = request.POST.get('user_id')
            password = request.POST.get('pass')
            user = authenticate(request, username = userId, password=password)
            # user.has_perm(accounts.add_seller)
            if user is not None:
                login(request, user)
                print("=================")
                print("is he seller =" ,user.is_seller)
                print("=================")

            else:
                print("not a user")
                return render(request, "accounts/login.html")
                

            return redirect('home')

        return render(request, "accounts/login.html")
    return redirect('home')

@login_required
def signOut(request):
    logout(request)
    return redirect('home')

@login_required
def becomeSeller(request):
    if request.user.is_seller == False:
        if request.method == 'POST':
            print('become seller')
            user = User.objects.get(id=request.POST.get('currentUserId'))
            fullname = user.first_name +" "+ user.last_name
            email = user.email
            user.is_seller = True
            user.save()
            address = request.POST.get('phnumber')
            phnum = request.POST.get('address')
            idprooftype = request.POST.get('idtype')
            idproofnum = request.POST.get('idnumber')
            accnum = request.POST.get('accnumber')
            instance=models.seller(
                name = fullname,
                email = email,
                address = address,
                phoneNumber = phnum,
                IdProofType = idprooftype,
                uniqueIdProof = idproofnum,
                bankAccNum = accnum,
                createdBy = user
            )
            instance.save()
            print(fullname)
            print("=================")
            print("is he seller =" ,user.is_seller)
            print("=================")
            
            return redirect('home')
        return render(request, 'accounts/becomeseller.html')
    return redirect('home')
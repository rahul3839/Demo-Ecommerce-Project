import email
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import UserForm,LoginForm,UserUpdatForm
from .models import Contacts, CustomUser,Product,Main_Product_Cate,Cart,Order
from django.contrib.auth.forms import PasswordChangeForm ,SetPasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.
   

def Index(request):
   
    main_product_cate = Main_Product_Cate.objects.all()
    product = Product.objects.all().order_by('-id')
    maincategoryID = request.GET.get('detail')  
    Category_ID = request.GET.get('category') 

    if 'search' in request.GET:
        Search = request.GET['search']
        product = Product.objects.filter(name__icontains=Search) 
        print(product,"------------------------")
        return render(request,'app/shop.html',{'product':product})

    elif Category_ID:
        product=Product.objects.filter(id=Category_ID)
        return render(request,'app/shop.html',{'product':product})

    elif maincategoryID:
        product=Product.objects.filter(id=maincategoryID)
        return render(request,'app/shopingdetail.html',{'product':product})

    else:
        product = Product.objects.all().order_by('-id')
    return render(request,'app/index.html',{'product': product ,'main_product_cate':main_product_cate})
    
   
def Shop(request):
    maincategoryID = request.GET.get('detail')
    if  maincategoryID:
        product=Product.objects.filter(id=maincategoryID)
        return render(request,'app/shopingdetail.html',{'product':product})
    product = Product.objects.all()
    return render(request,'app/shop.html',{'product':product})


def Detail(request):
    return render(request,'app/shopingdetail.html')

def add_to_card(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user ,product=product).save()
    return HttpResponseRedirect('/showcart')

def show_cart(request): 
    if request.user.is_authenticated:
        user = request.user
        product =  Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount =70.0 
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price) 
                amount += tempamount
                totalamount  =  amount +  shipping_amount
        return render(request,'app/shopingcart.html',
        {'product':product,'amount':amount,'totalamount':totalamount})
    else:
        return HttpResponseRedirect('/')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount =70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
        for p in cart_product:         
            tempamount = (p.quantity * p.product.price)
            amount += tempamount
            totalamount =  amount + shipping_amount

        data = {
            'quantity': c.quantity,
            'amount' : amount,
            'totalamount' : totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount =70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user] 
        for p in cart_product:         
            tempamount = (p.quantity * p.product.price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount' : amount,
            'totalamount' : amount + shipping_amount
        }
        return JsonResponse(data)

    
def cart_delete(request,id):
     if request.method == 'POST':
        pi = Cart.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/showcart')

def Checkout(request):
    if request.user.is_authenticated:
        user = request.user
        product =  Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount =70.0 
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price) 
                amount += tempamount
                totalamount  =  amount +  shipping_amount
        return render(request,'app/checkout.html',
        {'product':product,'amount':amount,'totalamount':totalamount,'tempamount':tempamount})
    else:
        return HttpResponseRedirect('/')

#======================Contact==============================
def Contact(request):

    if request.method == 'POST':
        Contacts.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            subject = request.POST['subject'],
            message = request.POST['message']
        )
        messages.success(request, 'Your request has been sent it.....')
    return render(request,"app/contact.html")

def placeorder(request): 
    if request.user.is_authenticated:
        amount = 0.0
        shipping_amount =70.0 
        total_price = 0.0 
        user = request.user 
            
        product = Cart.objects.filter(user=request.user).first() 
        if request.method == 'POST':
            fname = request.POST.get('fname'),
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            phone= request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            pincode = request.POST.get('pincode') 

            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    tempamount = (p.quantity * p.product.price) 
                    amount += tempamount
                    total_price  =  amount +  shipping_amount
            data = Order(user=user,product=product,fname=fname,lname=lname,email=email,phone=phone,
            address=address,city=city,state=state,country=country,pincode=pincode,total_price=total_price)
            messages.success(request, 'Your request has been sent it.....')
            data.save()
                            
        return render(request,'app/checkout.html')
    else:
        return HttpResponseRedirect('/')          

#========================USER REGISTRATION-=================================
def RegistrationView(request):

    if request.method == 'POST':                                
        fm = UserForm(request.POST) 

        if fm.is_valid():
            fm.save()
            print(fm,"===========")
            subject = 'about Registration'
            message = f'hi {{user}},you has been registrtion successfully '
            email_from = 'rhp.globaliasoft@gmail.com'
            rec_list = [email,]
            send_mail(subject,message,email_from,rec_list)
            messages.success(request,'Your Account has been Created Please Login Now.!!!!!!')
            return HttpResponseRedirect('userlogin/')
    else:
        fm =UserForm()
    return render(request,'app/registrationForm.html',{'form':fm}) 

#=======================USER LOGIN===============================
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user =  authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'logged Successfully!!!!')
                    return HttpResponseRedirect('/')
        else:
            form = LoginForm()
        return render(request,'app/userlogin.html',{"form":form})
    else:
        return HttpResponseRedirect('/')

#====================CHANGE PASSWORD===============================
def ChangePassword(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password has been update.......')
            return HttpResponseRedirect('/userlogin')
        else:
            messages.error(request,"please corrent the error below")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/changepassword.html', {'form': form})

#====================LOGOUT=============================== 
def UserLogout(request):
    logout(request)   
    return render(request,'app/index.html')
    
#====================FORGETPASSWORD===============================   
# def FogetPassword(request):
#     return render(request,'app/registration/password_reset_form.html')
    

def About(request):
    return render(request,'app/about.html')
    

#--------------------------USER PROFILE UPDATE------------------------------------------
def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = UserForm(request.POST,instance = request.user)
            if fm.is_valid():   
                messages.success(request,"your profilr wes updated!!!")
                fm.save()
        else:
            fm = UserUpdatForm(instance = request.user)
        return render(request,'app/userprofile.html',{'name':request.user,'form':fm})
    else:
        return HttpResponseRedirect('/userlogin/')



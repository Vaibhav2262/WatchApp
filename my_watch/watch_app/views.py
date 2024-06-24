from django.shortcuts import render , HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay

# Create your views here.


def about(request):
    return HttpResponse("This is About Page !")

def home(request):
    #print('result is :',request.user.is_authenticated)
     context={}
     p=Product.objects.filter(is_active=True)
     print(p)
     context['products']=p
     return render(request,'index.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']

        # Error conform all deteils are fill or not
        context={}  # empty dectionary
        if uname=="" or upass=="" or ucpass=="" :  # check the those thick
            context['errmsg']="Fields cannot be Empty"    # pass key and value to dectonary
        elif upass != ucpass:
            context['errmsg']="Password & confirm password didn't match"
        # pass value in database
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)  # pass word is not visible in database
                u.save()
                context['success']="User Created Successfully, Please Login"
            except Exception:
                context['errmsg']='user with same username already exists!!!!!!!'
        #return HttpResponse("User created successfully!!")
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')


def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print (uname, '-,upass')

        context={}
        if uname=="" or upass=="":  # check the those thick
            context['errmsg']="Fields cannot be Empty"    # pass key and value to dectonary
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/')
            else:
                context['errmsg']="Invallid user and password"
                return render(request,'login.html',context)

            #print(u) #object  ==>> sell the record on terminal 
            #print(u.password)
            #print(u.is_superuser)  #0- false
            return HttpResponse("Data is fetched")
    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')


def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1&q2)
    print(p)     
    context={}
    context['products']=p    
    return render(request,'index.html',context)

def sort(request,sv):
    if sv == '0':
        #accending order
        col='price'
    else:
        #Deccending order
        col='-price'  
    p = Product.objects.order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    #print(min)
    #print(max)
    q1 = Q(price__gte=min)
    q2 = Q (price__lte=max)
    q3= Q(is_active=True)
    p = Product.objects.filter(q1&q2&q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def product_details(request,pid):
    p = Product.objects.filter(id=pid)
    context = {}
    context['products']=p
    return render(request,'product_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        # print(pid)
        # print(userid)(
        u=User.objects.filter(id=userid)
        #print(u[0])
        p=Product.objects.filter(id=pid)
        #print(p[0])
        # check the product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        #print(c)
        n=len(c)
        context={}
        if n==1:
            context['msg']="Product Already Exist in cart !!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added Succefully in Cart"
        context['products']=p
        return render(request,'product_details.html',context)
        #return HttpResponse('product added')
    else:
         return redirect('/login')

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    np=len(c)
    s=0
    for x in c:
        s=s + x.pid.price * x.qty
        print(s)
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

# remove product from order table
def remove_order(request,oid):
    c=Order.objects.filter(id=oid)
    c.delete()
    return redirect('/placeorder')



def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        #Increase quantity
        t=c[0].qty + 1
        c.update(qty=t)
    else:
        #decrease quantity
        if c[0].qty>1:
            t=c[0].qty - 1
            c.update(qty=t)
    return redirect('/viewcart')


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    #print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid, pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    context = {}
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders)
    context['data']=orders
    context['n']=np
    s=0
    for x in orders:
        s= s + x.pid.price * x.qty
    context['total']=s
    return render(request,'placeorder.html',context)
    #return HttpResponse("")

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s= s + x.pid.price * x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_d7e82DgLM34rbi", "THAMAN1zfURcOOXvZwatM6Qm"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)
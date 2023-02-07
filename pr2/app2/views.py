from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='loginpage')
@admin_only
def home(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    orders_count=orders.count
    pending=orders.filter(status='Pending').count
    delieverd=orders.filter(status='Delieverd').count

    context={'orders':orders,'customers':customers,'orders_count':orders_count,'pending':pending,'delieverd':delieverd}
    return render(request,'app2/dashboard.html',context)


@unauthencticated_user
def loginpage(request):
    if request.method=='POST':
        name=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=authenticate(request,username=name,password=password)
            login(request,user)
            return redirect('home')

        except:
            messages.error(request,'Username or Password is invalid!!!')


    context={'page':'login'}
    return render(request,'app2/login_register.html',context)    


def logoutuser(request):
    logout(request)
    return redirect('home')    


@unauthencticated_user
def register(request):
    form=UserForm()
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request,f'Account with {user.username} has been created successfully!!!')
            return redirect('home')    

    context={'form':form,'page':'register'}
    return render(request,'app2/login_register.html',context)    


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin'])
def productpage(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'app2/products.html',context)    


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin','Customer'])
def customerpage(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()
    my_filter=OrderFilter(request.GET,queryset=orders)
    orders=my_filter.qs

    context={'customer':customer,'orders':orders,'my_filter':my_filter}
    return render(request,'app2/customer.html',context)    


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin','Customer'])
def createorder(request,pk):
    orderformset=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk)
    formset=orderformset(queryset=Order.objects.none(),instance=customer)
    # form=OrderForm(initial={'customer':customer})

    if request.method=='POST':
        formset=orderformset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context={'formset':formset,'page':'order'}
    return render(request,'app2/form.html',context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin','Customer'])
def updateorder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)

    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'app2/form.html',context)    


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Admin','Customer'])
def deleteorder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('home') 

    context={'obj':order}
    return render(request,'app2/delete.html',context)        


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Customer','Admin'])
def userpage(request):
    orders=request.user.customer.order_set.all()
    orders_count=orders.count
    pending=orders.filter(status='Pending').count
    delieverd=orders.filter(status='Delieverd').count
    print(f'Orders : {orders}')
    context={'orders':orders,'orders_count':orders_count,'pending':pending,'delieverd':delieverd}

    return render(request,'app2/user.html',context)    


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['Customer'])
def accountsettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid:
            form.save()
            return redirect('userpage')

    context={'form':form}    
    return render(request,'app2/account_settings.html',context)
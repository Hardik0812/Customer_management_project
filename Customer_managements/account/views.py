
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.

from .forms import orderform, CreateUserForm,CustomerForm
from django.contrib.auth.models import User
from .models import Customer,Order,Product
from .decorators import unauthenticated_user, allowed_user, admin_only
# Create your views here.

@unauthenticated_user
def registerpage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customers')
            user.groups.add(group)
            Customer.objects.create(user=user)


            messages.success(request, 'Account was created successfully' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginpage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
        

    context = {}
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customers'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    total_order = request.user.customer.order_set.count()
    delivered = request.user.customer.order_set.filter(status='delivered').count()
    pending = request.user.customer.order_set.filter(status='pending').count()
    print('ORDERS',orders)
    context = {'orders':orders,'total_order': total_order,'delivered':delivered,'pending':pending}
    return render(request, 'accounts/user.html', context)


def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    order = Order.objects.all()
    Customers = Customer.objects.all()

    total_customers = Customer.objects.count()
    total_order = Order.objects.count()

    delivered = Order.objects.filter(status='delivered').count()
    pending = Order.objects.filter(status='pending').count()

    context = {'order': order, 'Customers': Customers, 'total_order': total_order,
               'total_customers': total_customers, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/Dashbord.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def Products(request):
    Products = Product.objects.all()
    return render(request, 'accounts/products.html', {'Products': Products})

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def Customers(request, pk):
    Customers = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customers_id=pk)
    order_count = Order.objects.filter(customers_id=pk).count()
    context = {'Customers': Customers,
               'orders': orders, 'order_count': order_count}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customers'])
def accountSettings(request):
	customer = request.user.customer        
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormset = inlineformset_factory(Customer, Order, fields=('products', 'status'), extra=10)
    Customers = Customer.objects.get(id=pk)
    formset = OrderFormset(queryset=Order.objects.none(), instance=Customers)   
    if request.method == 'POST':

        formset = OrderFormset(request.POST, instance=Customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/update_order.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def update_order(request, pk):
    orders = Order.objects.get(id=pk)
    form = orderform(instance=orders)
    if request.method == 'POST':
        form = orderform(request.POST, instance=orders)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/update_order.html', context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def delete_order(request, pk):
    orders = Order.objects.get(id=pk)
    if request.method == 'POST':
        orders.delete()
        return redirect('/')
    context = {'item': orders}
    return render(request, 'accounts/delete.html', context)




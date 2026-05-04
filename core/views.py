from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt     # commant for csrf origin stattus from setting.py


def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {
        'products': products
    })


def product_details(request, id):
    data = get_object_or_404(Product, id=id)
    return render(request, 'core/product_detail.html', {
        'data': data
    })


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Already registered...')
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Registered successfully!')
        return redirect('index')

    return render(request, 'core/register.html', {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})

    return render(request, 'core/login.html', {})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def add_to_cart(request, id):
    product = Product.objects.get(id=id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('index')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for data in cart_items:
        total += data.product.price * data.quantity

    return render(request, 'core/cart.html', {'cart_items': cart_items, 'total': total})


def remove(request, id):
    data = Cart.objects.get(id=id)
    data.delete()
    return redirect('cart')


def qty_increase(request, id):
    data = Cart.objects.get(id=id)
    data.quantity += 1
    data.save()
    return redirect('cart')


def qty_decrease(request, id):
    data = Cart.objects.get(id=id)

    if data.quantity > 1:
        data.quantity -= 1
        data.save()
    else:
        data.delete()

    return redirect('cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for data in cart_items:
        total += data.product.price * data.quantity

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total=total
        )

        for data in cart_items:
            OrderItem.objects.create(
                order=order,
                product=data.product,
                quantity=data.quantity,
            )

        # FIX: loop ke bahar
        cart_items.delete()
        return redirect('success')

    return render(request, 'core/checkout.html', {'cart_items': cart_items, 'total': total})


def success(request):
    return render(request, 'core/success.html', {})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'core/my_orders.html', {'orders': orders})


@login_required
def order_details(request, id):
    order = Order.objects.get(id=id, user=request.user)
    data = OrderItem.objects.filter(order=order)

    return render(request, 'core/order_details.html', {
        'order': order,
        'data': data
    })

@login_required
def payment(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for data in cart_items:
        total += data.product.price * data.quantity

    order = Order.objects.create(
        user=request.user,
        total=total,
        status='Pending'
    )

    amount = int(total * 100)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": amount,
        "currency": "INR"
    })

    order.razorpay_order_id = payment['id']
    order.save()

    return render(request,'core/payment.html',{
        'payment':payment,
        'total':total,
        'key':settings.RAZORPAY_KEY_ID
    })



@csrf_exempt
def payment_success(request):

    razorpay_order_id = request.POST.get('razorpay_order_id')

    order = Order.objects.get(razorpay_order_id=razorpay_order_id)

    order.status = "Paid"
    order.save()

    return redirect('success')
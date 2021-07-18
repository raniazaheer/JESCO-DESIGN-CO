from django.shortcuts import render, HttpResponse
from django.views import View
# Create your views here.
from django.forms.forms import Form
from django.shortcuts import redirect, render
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib import auth
from .forms import ContactForm, CustomerRegistrationForm
from django.conf import settings
# Create your views here.
from django.template.response import TemplateResponse
from django.http import JsonResponse, request
from .forms import CustomUserCreationForm
import json
from django.contrib import sessions
import datetime
from django .http import FileResponse
import io
from reportlab.pdfgen import canvas, textobject
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.views.generic import View
# from django.utils import render_to_pdf
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(
                user=user, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0,
                     'get_cart_items': 0, 'shipping': True}
            cartItems = order['get_cart_items']

        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            'items': items,
            'order': order,
            'cartItems': cartItems
        }

        pdf = render_to_pdf('invoice_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    # def order_pdf(request):
    #     # create Bytestream buffer
    #     buf = io.BytesIO()
    #     # create canvas
    #     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #     # create a text object
    #     textob = c.beginText()
    #     textob.setTextOrigin(inch, inch)
    #     textob.setFont("Helvetica", 14)
    #     c.drawImage(r"C:\Users\ladoo\OneDrive\Desktop\arrow.png",
    #                 0, 0, width=50, height=30)
    #     # add some lines of text
    #     lines = [
    #         "line 1",
    #         "line2",
    #     ]

    #     for line in lines:
    #         textob.textLine(line)
    #         # finish up

    #     c.drawText(textob)
    #     c.showPage()
    #     c.save()
    #     buf.seek(0)

    #     # return something
    #     return FileResponse(buf, as_attachment=True, filename='invoice.pdf')


class ProductView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(user=user,
                                                         complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0,
                     'get_cart_items': 0, 'shipping': True}
            cartItems = order['get_cart_items']

        prods = Product.objects.all()
        sketches = Product.objects.filter(category='sketching')
        frame = Product.objects.filter(category='Frames')
        paintings = Product.objects.filter(category='oil_paintings')
        drawings = Product.objects.filter(category='drawing')
        prods = Product.objects.all()

        return render(request, 'index.html', {'sketches': sketches, 'frame': frame,
                                              'paintings': paintings, 'drawing': drawings, 'prods': prods, 'items': items, 'cartItems': cartItems})


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)

        return render(request, 'product_detail.html', {'product': product})


def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('index')

        else:
            messages.error(request, 'Error wrong username/password')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')


def store(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']

    products = Product.objects.all()

    return render(request, 'store.html', {'items': items, 'products': products, 'cartItems': cartItems})


def contact(request):
    # if request.method == 'POST':
    #     message = request.POST['message']
    #     name = request.POST['name']
    #     email = request.POST['email']

    return render(request, "contact.html")


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user,
                                                     complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    return render(request, 'dashboard.html', {'items': items, 'products': products, 'cartItems': cartItems})


def cart(request):

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']

    return render(request, 'cart.html', {'items': items, 'order': order, 'cartItems': cartItems})


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']

    return render(request, 'checkout.html', {'items': items, 'order': order, 'cartItems': cartItems})


def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': True}
        cartItems = order['get_cart_items']

    return render(request, 'wishlist.html', {'items': items, 'order': order, 'cartItems': cartItems})


def register(request):
    form = CustomUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Congratulations! Account for ' + user +
                             ' has been created successfully ^_^ ')

    return render(request, 'register.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)
    user = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity = - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def blogs(request):
    return render(request, 'blogs.html')


def about(request):
    return render(request, 'about.html')


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, complete=True)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAdddress.objects.create(
            user=user,
            order=order,
            address=data['form']['address'],
            city=data['form']['city'],
            state=data['form']['state'],
            zipcode=data['form']['zipcode'],

        )
    else:
        print('User is not logged in')

    return JsonResponse('payment was submitted', safe=False)

from catalog.models import Product, Contact
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}): {message}")
    return render(request, 'contacts.html')


def home_view(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    # latest_products = Product.objects.all()

    for product in latest_products:
        print(product.name, product.created_at, product.image.url if product.image else "No image")
    return render(request, "home.html", {'latest_products': latest_products})


def contacts_view(request):
    contacts_info = Contact.objects.all()

    for contact in contacts_info:
        print(contact.name, contact.phone)
    return render(request, "contacts.html", {'contacts': contacts_info})


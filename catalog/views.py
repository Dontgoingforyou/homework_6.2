from catalog.models import Product, Contact
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import ProductForm


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"{name} ({phone}): {message}")
    return render(request, 'contacts.html')


def contacts_view(request):
    contacts_info = Contact.objects.all()

    for contact in contacts_info:
        print(contact.name, contact.phone)
    return render(request, "contacts.html", {'contacts': contacts_info})


def home_view(request):
    latest_products = Product.objects.order_by('-created_at')[:6]

    for product in latest_products:
        print(product.name, product.created_at, product.image.url if product.image else "No image")
    return render(request, "latest_products.html", {'latest_products': latest_products})


def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "product_list.html", {"page_obj": page_obj})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def create_product(request):
    request.method = 'POST'
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('catalog:product_list')

    return render(request, 'create_product.html', {'form': form})

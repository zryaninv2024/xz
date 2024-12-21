from django.shortcuts import render
from django.db.models import Q
from .forms import UserRegisterForm, ProductForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    return render(request, 'store/home.html', {'latest_products': latest_products})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'avatar' in request.FILES:
                user.profile.avatar = request.FILES['avatar']
                user.profile.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form})

def service_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'store/service_list.html', {'products': products, 'query': query})

def service_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/service_detail.html', {'product': product})

def search_result(request):
    query = request.GET.get('q')
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/search_result.html', {'products': products, 'query': query})

@login_required
def profile(request):
    orders = request.user.orders.select_related('product')  # Оптимизация запроса
    return render(request, 'store/profile.html', {'orders': orders})

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Order.objects.create(user=request.user, product=product)
    return redirect('profile')

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'store/create_product.html', {'form': form})

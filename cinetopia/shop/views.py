import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from shop.cart import Cart
from shop.models import Product


class ProductsListView(ListView):
    model = Product
    queryset = Product.objects.filter(is_active=True)
    context_object_name = 'products'
    template_name = 'shop/shop.html'
    paginate_by = 30

    def get_queryset(self):
        category = self.request.GET.get('category', '')
        sort = self.request.GET.get('sort', '-created_at')
        products = Product.objects.filter(is_active=True)

        if category:
            products = products.filter(category=category)

        products = products.order_by(sort)
        return products

    def get_context_data(self, **kwargs):
        category = self.request.GET.get('category', '')
        sort = self.request.GET.get('sort', '-created_at')

        context = super().get_context_data(**kwargs)
        context.update({
            'categories': dict(Product.CATEGORY_CHOICES),
            'selected_category': category,
            'sort_options': {
                '-created_at': 'Новинки',
                'price': 'Цена по возрастанию',
                '-price': 'Цена по убыванию',
                'name': 'По названию (А-Я)',
                '-name': 'По названию (Я-А)',
            },
            'selected_sort': sort,
        })
        return context


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    data = json.loads(request.body)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(data.get('quantity', 1))
    update_quantity = data.get('update', False)

    cart.add(product=product, quantity=quantity, update_quantity=update_quantity)

    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'cart_total_price': str(cart.get_total_price()),
        'product_total_price': str(product.get_price() * quantity)
    })


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return JsonResponse({
        'success': True,
        'cart_total_items': len(cart),
        'cart_total_price': str(cart.get_total_price())
    })

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})
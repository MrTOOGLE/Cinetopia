from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


class OrderCreateView(LoginRequiredMixin, TemplateView):
	template_name = 'orders/order_create.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = OrderCreateForm()
		return context

	def post(self, request, *args, **kwargs):
		cart = Cart(request)
		form = OrderCreateForm(request.POST)

		if form.is_valid() and cart:
			order = form.save(commit=False)
			order.user = request.user
			order.save()

			for item in cart:
				OrderItem.objects.create(
					order=order,
					product=item['product'],
					price=item['price'],
					quantity=item['quantity'],
					discount=item['product'].discount
				)

			cart.clear()
			return redirect('order_created', order_id=order.id)

		return self.render_to_response({'form': form})


class OrderCreatedView(LoginRequiredMixin, TemplateView):
	template_name = 'orders/order_created.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		order_id = self.kwargs.get('order_id')
		context['order'] = Order.objects.get(id=order_id)
		return context


class OrderDetailView(LoginRequiredMixin, DetailView):
	model = Order
	template_name = 'orders/order_detail.html'
	context_object_name = 'order'

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user)


class UserOrdersView(LoginRequiredMixin, ListView):
	model = Order
	template_name = 'orders/user_orders.html'
	context_object_name = 'orders'

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user).order_by('-created')

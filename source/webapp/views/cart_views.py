from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DeleteView, CreateView
from django.shortcuts import redirect, get_object_or_404

from webapp.models import Product, Order, OrderProduct
from webapp.forms import OrderForm


class AddItemToCart(View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        qty = int(request.POST.get('qty'))

        cart = Order.objects.get_or_create(status='new', session=request.session._session_key)
        cart_item = OrderProduct.objects.get_or_create(order=cart, product=product)

        if product.balance >= cart_item.product + qty:
            cart_item.qty += qty
            cart_item.save()

        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        next = self.request.GET.get('next')
        if next:
            return next
        return reverse('webapp:index')


class CartList(ListView):
    model = Order
    template_name = 'cart/index.html'
    context_object_name = "carts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['total'] = Order.get_total()
        context['form'] = OrderForm
        return context


class CartDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('webapp:cart_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeleteOne(DeleteView):
    model = Order
    success_url = reverse_lazy('webapp:cart_index')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.qty -= 1
        if self.object.qty < 1:
            self.object.delete()
        else:
            self.object.save()
        return redirect(success_url)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        order = form.save()

        for item in Order.objects.all():
            OrderProduct.objects.create(product=item.product, qty=item.qty, order=order)
            item.product.balance -= item.qty
            item.product.save()
            item.delete()

        return redirect(self.success_url)

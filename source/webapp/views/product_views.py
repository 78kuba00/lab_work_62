from webapp.forms import SearchForm, ProductForm
from webapp.models import Product
from webapp.views.base_views import SearchView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect


class ProductList(SearchView):
    model = Product
    template_name = 'product/index.html'
    context_object_name = 'products'
    search_form_class = SearchForm
    search_fields = ['name__icontains']
    paginate_by = 5
    ordering = ['category', 'name']
    search_fields = ['name__icontains', 'description__icontains']

    def post(self, request, *args, **kwargs):
        for product_pk in request.POST.getlist('products', []):
            print(self.request.POST.getlist('products', []))
            request.session['key'] = 'value'
        return redirect("webapp:product_view")

    def get_queryset(self):
        return self.model.objects.filter(balance__gt=0)

    def get_success_url(self):
        return reverse('webapp:index', kwargs={'pk': self.object.product.pk})


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_view.html'

    def get_context_data(self, **kwargs):
        my_dict = self.request.session.get('key', {})
        my_dict['test'] = 1
        self.request.session['key'] = my_dict
        # self.request.session['key']['test'] = 1
        context = super().get_context_data(**kwargs)
        product = self.object
        # order = product.order.order_by('-name')
        # context['order'] = order
        return context


class ProductCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    context_object_name = 'products'
    permission_required = 'webapp.add_product'

    def form_valid(self, form):
        print(self.kwargs.get('pk'))
        form.instance.project = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.pk })


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'
    context_object_name = 'products'
    permission_required = 'webapp.change_product'

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().products.users.all()


    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.products.pk })


class ProductDelete(PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "product/product_delete.html"
    redirect_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_product'

    def has_permission(self):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in self.get_object().product.users.all()

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_product') or self.get_object().users == self.request.user

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:product_view', kwargs={'pk': self.object.product.pk})

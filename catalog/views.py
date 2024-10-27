from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Blog, Version


# Create your views here.


# def home(request):
#     return render(request, "home.html")


# def contacts(request):
#     return render(request, "contacts.html")

class ContactsView(TemplateView):
    """Контроллер просмотра контактов"""
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    model = Product


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    # fields = ["name", "description", "category", "photo", "price"]
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # fields = ["name", "description", "category", "photo", "price"]
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    # Добавлено переопределение функции
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset()
        return context_data

    def form_valid(self, form):
            context_data = self.get_context_data()
            formset = context_data["formset"]
            if form.is_valid() and formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.edit_category') and user.has_perm('catalog.edit_description') and user.has_perm(
                'catalog.can_edit_is_published'):
            return ProductModeratorForm
        raise PermissionDenied()


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogCreateView(CreateView):
    model = Blog
    slug_field = 'slug'
    fields = ['title', 'description', 'photo']
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_counter += 1
        obj.save()
        return obj


class BlogUpdateView(UpdateView):
    model = Blog
    slug_field = 'slug'
    fields = ['title', 'description', 'photo']

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_detail', kwargs={'slug': self.object.slug})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')

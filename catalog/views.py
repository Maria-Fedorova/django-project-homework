# from django.shortcuts import render, get_object_or_404
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from catalog.forms import ProductForm, VersionForm
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




class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    # fields = ["name", "description", "category", "photo", "price"]
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_context_data(self, **kwargs):
        taboo_world = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        context_data = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        cleaned_data = form.cleaned_data['name'].lower()
        taboo_world = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in taboo_world:
            if word in cleaned_data:
                form.add_error('name', 'Данное название не подходит.')
                return self.form_invalid(form)

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
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
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super.form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
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

# def publishing_action(slug):
#     blog_item = get_object_or_404(Blog, slug=slug)
#     if blog_item.is_published:
#         blog_item.is_published = False
#     else:
#         blog_item.is_published = True
#
#         blog_item.save()
#
#         return redirect(reverse_lazy('catalog:blog_list'))

# def is_published_filter(request):
#     context = {
#         'object_list': Blog.objects.filter(is_published=True),
#     }
#     return render(request, 'blog/blog_list.html', context)

# if request.method == 'POST':
#     blog.is_published = not blog.is_published
#     blog.save()
#     return redirect('catalog:blog_detail', slug=blog.slug)
# else:
#     return redirect('catalog:blog_detail', slug=blog.slug)

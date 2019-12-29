from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView

from ..article.models import Article
from .forms import CategoryForm
from .models import ArticleCategory

per_page = settings.PER_PAGE


class CategoryListView(ListView):
    """Get all categories"""
    model = ArticleCategory
    template_name = 'category/all_categories.html'
    context_object_name = 'categories'

    def get(self, request, *args, **kwargs):
        return super(CategoryListView, self).get(request, *args, **kwargs)


class CategorizeArticleListView(ListView):
    """Get all articles based on category name"""
    model = Article
    context_object_name = 'articles'
    paginate_by = per_page
    template_name = 'category/article_categorized.html'

    def get_queryset(self):
        queryset = super(CategorizeArticleListView, self).get_queryset()
        category = ArticleCategory.objects.get(
            name=self.kwargs.get('name', 'uncategorized'))
        return queryset.filter(category=category)

    def get_context_data(self, **kwargs):
        context = dict()
        context['category'] = ArticleCategory.objects.get(
            name=self.kwargs.get('name', 'uncategorized'))
        return super(CategorizeArticleListView, self).get_context_data(
            **context)


@login_required
@permission_required(
    [
        "category.add_articlecategory", "category.view_articlecategory",
        "category.change_articlecategory", "category.delete_articlecategory"
    ],
    raise_exception=True)
def manage_category(request):
    """Cagetory dashboard View
    response category dashboard, provide form, template
        args:
            :type request: HttpRequest
            :rtype: HttpResponse
    """
    category_form = CategoryForm()
    return render(
        request, 'category/category_backend.html', {
            'form': category_form,
            'action_name': "添加",
            'action': reverse('category:add'),
            'error_msg': ''
        })


@login_required
@permission_required(
    ("category.add_articlecategory", "category.view_articlecategory"),
    raise_exception=True)
def add_category(request):
    """Add category view
    the desination of the datafrom submitted form, process form data
        args:
            :request: HttpRequest, its object include submitted form data
            :rtype: HttpResponse
    """
    if request.method == 'POST':
        # 使用request post 的数据初始化表单字段
        form = CategoryForm(request.POST)
        if request.user.is_superuser and form.is_valid():
            name = request.POST.get('name')
            try:
                category = ArticleCategory(name=name)
                category.save()
            except IntegrityError:
                error_message = "Duplicated %s category" % repr(name)
                category_form = CategoryForm()
                return render(request, 'category/category_backend.html', {
                    'form': category_form,
                    'error_msg': error_message
                })
            else:
                return HttpResponseRedirect(reverse('category:manage'))
        else:
            return render(
                request, 'category/category_backend.html', {
                    'form': form,
                    'action_name': "添加",
                    'action': reverse("category:add")
                })
    return HttpResponseRedirect(reverse('category:manage'))


@login_required
@permission_required(
    ("category.add_articlecategory", "category.view_articlecategory"),
    raise_exception=True)
def edit_category(request, name):
    """
    view function for changing category's name
        args:
            :request: HttpRequest
            :name: str, category's name
            :rtype: HttpResponse
    """
    category = get_object_or_404(ArticleCategory, name=name)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        name = request.POST.get('name')
        if request.user.is_superuser and form.is_valid():
            category.name = name
            try:
                category.save()
            except IntegrityError:
                error_message = "Duplicated %s category" % repr(name)
                category_form = CategoryForm()
                return render(request, 'category/category_backend.html', {
                    'form': category_form,
                    'error_msg': error_message
                })
            else:
                return HttpResponseRedirect(reverse('category:manage'))
    else:
        initial = {'name': category.name}
        # 在前端编辑表单中显示要编辑的类名
        category_form = CategoryForm(initial=initial)
        return render(
            request, 'category/category_backend.html', {
                'form': category_form,
                'action_name': "编辑",
                'action': reverse('category:edit', args=(name, ))
            })


@login_required
@permission_required(
    ("category.delete_articlecategory", "category.view_articlecategory"),
    raise_exception=True)
def delete_category(request, name):
    if request.method == 'POST':
        if request.user.is_superuser:
            get_object_or_404(ArticleCategory, name=name).delete()
        return HttpResponseRedirect(reverse('category:manage'))
    category = get_object_or_404(ArticleCategory, name=name)
    return render(request, 'category/delete_confirm.html',
                  {'category': category})

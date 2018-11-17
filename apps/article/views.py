from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseCreateView, DeleteView, UpdateView
from django.db.models import F
from django.conf import settings

from ipware.ip import get_real_ip

from .forms import CreateArticleForm, EditArticleForm
from .models import Article
from apps.comment.forms import CommentForm
from utils.cache import cache_decorator, cache

PER_PAGE = getattr(settings, 'PER_PAGE')


class IndexView(ListView):
    """Index homepage
    """
    template_name = "article/index.html"
    model = Article
    paginate_by = PER_PAGE
    context_object_name = 'articles'

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)


class CreateArticleView(LoginRequiredMixin, SingleObjectTemplateResponseMixin,
                        BaseCreateView):
    """Class-based view function used to write an article
    """
    template_name = 'article/editor.html'
    form_class = CreateArticleForm
    login_url = '/accounts/login/'

    def dispatch(self, request, *args, **kwargs):
        return super(CreateArticleView, self).dispatch(request, *args,
                                                       **kwargs)

    def form_valid(self, form):
        """
        :param form: instantiate an form with request.POST
        :return: HttpResponseRedirect
        """
        # update article instance,
        # fix article'author is null when article posted.
        form.instance.author = self.request.user
        return super(CreateArticleView, self).form_valid(form)


class UpdateArticleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View function for editing a posted article
    """
    model = Article
    login_url = '/accounts/login/'
    template_name = 'article/editor.html'
    context_object_name = 'article'
    form_class = EditArticleForm
    permission_denied_message = "Permission Denied."
    raise_exception = True

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or \
            self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return super(UpdateArticleView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        super(UpdateArticleView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect(reverse("articles:manage"))


class ArticleDetailView(DetailView, BaseCreateView):
    """The detail of each article
    """
    model = Article
    form_class = CommentForm
    template_name = 'article/article_detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        Day = 24 * 60 * 60 # A day
        self.object = super(ArticleDetailView, self).get_object()
        ip = get_real_ip(request)
        visited_ips = cache.get(self.object.slug, set())

        if not visited_ips:
            visited_ips.add(ip)
            cache.set(self.object.slug, visited_ips, Day)
            self.model.objects.filter(id=self.object.id).update(
                view_times=F('view_times') + 1)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    login_url = 'account/login/'
    template_name = 'article/article_confirm.html'
    success_url = reverse_lazy('articles:manage')
    context_object_name = 'article'
    permission_denied_message = "Permission Denied."
    raise_exception = True

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or \
            self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return super(DeleteArticleView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(DeleteArticleView, self).post(request, *args, **kwargs)


class ArticleListView(ListView):
    template_name = 'article/all_articles.html'
    model = Article
    paginate_by = 15
    context_object_name = 'articles'

    def get(self, request, *args, **kwargs):
        return super(ArticleListView, self).get(request, *args, **kwargs)


class TaggedArticleListView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    paginate_by = PER_PAGE
    context_object_name = 'articles'

    def get_queryset(self, **kwargs):
        queryset = Article.objects.filter(
            tags__icontains=self.kwargs.get('tag'))
        return queryset

    def get(self, request, *args, **kwargs):
        return super(TaggedArticleListView, self).get(request, *args, **kwargs)


class ArticleManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'article/article_backend.html'

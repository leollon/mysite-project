from django.shortcuts import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Article


class ArticleBaseForm(forms.ModelForm):
    """Article base form for writing or editting an article
    """

    def __init__(self, *args, **kwargs):
        super(ArticleBaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "save"))

    class Meta:
        model = Article
        fields = ["title", "article_body", "category", "tags"]


class CreateArticleForm(ArticleBaseForm):
    """
    generate an form from models for writing an article
    """

    def __init__(self, *args, **kwargs):
        super(CreateArticleForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse("article:write")


class EditArticleForm(ArticleBaseForm):
    """
    generate an form from models for edit an article
    """

    def __init__(self, *args, **kwargs):
        super(EditArticleForm, self).__init__(*args, **kwargs)

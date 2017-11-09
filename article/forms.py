from django import forms
from article.models import Article
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CreateArticleForm(forms.ModelForm):
    """
    generate an form from models for writing an article
    """
    class Meta:
        model = Article
        fields = ('title', 'article_body', 'category',)

    def __init__(self, *args, **kwargs):
        super(CreateArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = 'article:write'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'publish'))


class EditAriticleForm(forms.ModelForm):
    """
    generate an form from models for edit an article
    """
    class Meta:
        model = Article
        fields = ('title', 'article_body', 'category')

    def __init__(self, *args, **kwargs):
        super(EditAriticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'save'))

from django import forms
from django.utils.translation import ugettext_lazy as _


class CategoryForm(forms.Form):
    """
    form for category's operations
    """
    error_messages = {'required': _("category name is required.")}
    name = forms.CharField(max_length=64,
                           label='Name',
                           widget=forms.TextInput(
                           attrs={"class": 'form-control',
                                  "placeholder": 'Category name'}),
                           error_messages={'required': _('category name is '
                                                         'required.')}
                           )

    def __int__(self, data=None, *args, **kwargs):
        super(CategoryForm, self).__int__(data, args, kwargs)

    def clean(self):
        name = self.cleaned_data.get('name')
        if name == '' or name is None:
            raise forms.ValidationError(message=self.error_messages['required'])
        return name

from django import forms
from django.utils.translation import ugettext as _

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_text", "username", "email", "link", "post")

    def __init__(self, label_suffix="", *args, **kwargs):
        super(CommentForm, self).__init__(
            label_suffix=label_suffix, *args, **kwargs
        )
        self.fields["username"].widget.attrs["placeholder"] = _(
            "Username(required)"
        )
        self.fields["email"].widget.attrs["placeholder"] = _("Email(optional)")
        self.fields["link"].widget.attrs["placeholder"] = _("Link(optional)")
        self.fields["comment_text"].widget.attrs["placeholder"] = _(
            "Comment(required)"
        )
        self.fields["username"].widget.attrs["required"] = True
        self.fields["comment_text"].widget.attrs["required"] = True

from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment_text", "username", "email", "link", "post")

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Username(needed)"
        self.fields["email"].widget.attrs["placeholder"] = "Email(optional)"
        self.fields["link"].widget.attrs["placeholder"] = "Link(optional)"
        self.fields["comment_text"].widget.attrs["placeholder"] = (
            "Comment(" "needed)"
        )
        self.fields["username"].widget.attrs["required"] = True
        self.fields["comment_text"].widget.attrs["required"] = True

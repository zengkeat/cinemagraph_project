from django import forms

# CREATING COMMENT FORM CONDINGENTREPRENEUR ADVANCING BLOG:15
# https://www.youtube.com/watch?v=zgF-KtQPqxQ&list=PLEsfXFp6DpzQB82YbmKKBy2jKdzpZKczn&index=15
class CommentForm(forms.Form):
    content_type = forms.CharField(widget = forms.HiddenInput)
    object_id = forms.IntegerField(widget = forms.HiddenInput)
    # parent_id = forms.IntegerField(widget = forms.HiddenInput, require = False)
    content = forms.CharField(label = '',widget = forms.Textarea)

from django import forms


class NewEntryForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    image = forms.CharField(widget=forms.URLInput())
    category = forms.CharField()
    # Chose to make the step $1 instead of 0.1c so biddings go faster :p
    bid = forms.CharField(widget=forms.NumberInput(attrs={"min": "0", "step": "1.00"}))


class NewCommentForm(forms.Form):
    comment = forms.Textarea()
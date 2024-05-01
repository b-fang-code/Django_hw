from django import forms


class ClientForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=100)
    address = forms.CharField(max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=100)
    price = forms.IntegerField()
    quantity = forms.IntegerField()
    image = forms.ImageField()


class ChoiceForm(forms.Form):
    client_id = forms.IntegerField(min_value=1)
    choice_period = forms.ChoiceField(choices=[('week', 'За неделю'), ('month', 'За месяц'), ('year', 'За год')])


class DeleteByIdForm(forms.Form):
    id = forms.IntegerField(min_value=1)

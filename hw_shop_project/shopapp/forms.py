from django import forms


class ChoiceForm(forms.Form):
    client_id = forms.IntegerField(min_value=1)
    choice_period = forms.ChoiceField(choices=[('week', 'За неделю'), ('month', 'За месяц'), ('year', 'За год')])

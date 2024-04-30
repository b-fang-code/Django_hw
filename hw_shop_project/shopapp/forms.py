from django import forms


class ChoiceForm(forms.Form):
    client_id = forms.IntegerField(min_value=1, max_value=8)
    choice_period = forms.ChoiceField(choices=[('week', 'За неделю'), ('month', 'За месяц'), ('year', 'За год')])

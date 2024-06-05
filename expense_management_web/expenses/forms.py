from django import forms

class categoryExpenseForm(forms.Form):
    name = forms.CharField(label='Name Category', max_length=255)

class ExpenseForm(forms.Form):
    category = forms.ChoiceField(label='Category', choices=[])
    amount = forms.IntegerField(label='Amount')
    note = forms.CharField(label='Note', max_length=255, required=False)
    
    date = forms.DateField(label='Date', widget=forms.SelectDateWidget)

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories')
        super(ExpenseForm, self).__init__(*args, **kwargs)
        # category của từng user

        self.fields['category'].choices = [(category.id, category.name) for category in categories]
        self.fields['category'].choices.append(('other', 'Other'))  # Add 'Other' option

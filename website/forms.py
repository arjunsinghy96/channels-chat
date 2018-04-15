from django import forms

class LeagueForm(forms.Form):
    
    name = forms.CharField(label='Leaguename', max_length=50)
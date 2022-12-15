from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from django import forms
from .models import newUser, Poll, Choice, Vote

class CreateNewUserForm(UserCreationForm):
    class Meta:
        model = newUser
        fields = ['username', 'name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-field--input'}),
            'name':forms.TextInput(attrs={'class':'form-field--input'}),
            'email':forms.EmailInput(attrs={'class':'form-field--input'})
        }
    pass

class DateInput(forms.DateInput):
    input_type = 'date'
    

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'detail', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

class ChoiceFormD(ModelForm):
    class Meta:
        model = Choice
        fields = []

class ChoiceFormA(ModelForm):
    class Meta:
        model = Choice
        fields = []

class VoteForm(ModelForm):
    class Meta:
        model = Vote
        fields = ['choice']
        
        
    def __init__(self, poll_pk = None, **kwargs):
        super(VoteForm, self).__init__(**kwargs)
        if True:
            self.fields['choice'].queryset = Choice.objects.filter(poll = poll_pk)
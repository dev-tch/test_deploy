from django import forms
from .models import Office, CustomUser
from django.core.exceptions import ValidationError

class OfficeCreationForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['ref', 'name', 'country', 'state', 'region', 'address' , 'number_of_windows']

class OfficeUpdateForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['name', 'country', 'state', 'region', 'address' , 'number_of_windows', 'counter']

class AgentUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'national_id']
     # form block  update existing user due to  uniqueness of  data 
    # override clean for fields that blocks the update
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise ValidationError("username exists")
        return username
    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if CustomUser.objects.exclude(id=self.instance.id).filter(national_id=national_id).exists():
            raise ValidationError("national_id exists ")
        return national_id

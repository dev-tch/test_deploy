from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Office
from django.urls import reverse, NoReverseMatch

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'national_id', 'office')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        try:
            signup_url = reverse('tcn:signup')
        except NoReverseMatch:
            signup_url = '/tcn/signup/'  # Fallback URL path
       
        # Set role choices and configure widgets based on signup_url condition
        if self.request and self.request.path == signup_url:
            self.fields['role'].choices = CustomUser.USER_ROLES[:2]
            self.fields['national_id'].widget = forms.HiddenInput()
            self.fields['office'].widget = forms.HiddenInput()
            self.fields['national_id'].required = False
            self.fields['office'].required = False
        else:
            self.fields['role'].choices = [('agent', 'Agent')]
            self.fields['national_id'].widget = forms.TextInput(attrs={'placeholder': 'Enter National ID'})
            self.fields['office'].widget = forms.Select(attrs={'class': 'form-control'})
            self.fields['national_id'].required = True
            self.fields['office'].required = True
        
        # Set queryset for office field
        if self.request.user.is_authenticated:
            self.fields['office'].queryset = Office.objects.filter(users=self.request.user).exclude(ref='guest')
        else:
            self.fields['office'].queryset = Office.objects.filter(ref='guest')
        # self.fields['office'].queryset = Office.objects.all()

    def clean_office(self):
        role = self.cleaned_data.get('role')
        office = self.cleaned_data.get('office')
        if role in ['client', 'manager']:
            try:
                return Office.objects.get(pk='guest')
            except Office.DoesNotExist:
                # Create the office object with primary key 'guest' if it doesn't exist
                return Office.objects.create(pk='guest', name='Guest Office',
                                             country='Country', state='State',
                                             region='Region',
                                             address='Address',
                                             number_of_windows=1)
        elif role == 'agent':
            request = self.request
            if not request.user.is_authenticated:
                raise forms.ValidationError("User must be signed in to use Role agent")
            if request.user.role != 'manager':
                raise forms.ValidationError("User must be a manager  to use Role agent")

            user_office = Office.objects.filter(users=request.user).exclude(pk='guest').first()
            if not user_office:
                raise forms.ValidationError("No offices associated with the authenticated manager user")
            return user_office

        return office

    def save(self, commit=True):
        user = super().save(commit=False)
        user.office = self.cleaned_data.get('office')

        if commit:
            user.save()

        return user

from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class MyCustomSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={'placeholder': 'First Name'}),
            label='First Name',
        )
        self.fields['last_name'] = forms.CharField(
            required=True,
            widget=forms.TextInput(
                attrs={'placeholder': 'Last Name'}),
            label='Last Name',
        )

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        default_group, created = Group.objects.get_or_create(name='Users')
        user.groups.add(default_group)

        # You must return the original result.
        return user



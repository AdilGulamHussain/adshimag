from django import forms
from .models import MagUser, Comment


class NewUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    password1 = forms.CharField(widget=forms.PasswordInput(), help_text="Re-enter your password",
                                label="Confirm Password")
    phone_number = forms.RegexField(regex=r'^0\d{10}$', help_text="Optional. UK Phone number",
                                    error_messages={'invalid': "Phone number must be entered. 11 Digits."})

    class Meta:
        model = MagUser
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password', 'password1')

    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password1')

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("The two password fields must match.")
        return cleaned_data


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = MagUser
        fields = ('email', 'password',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(
                attrs={'id': 'com-body', 'required': True, 'placeholder': 'Enter your comment...'}),
        }

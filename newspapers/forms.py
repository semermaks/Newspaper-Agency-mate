from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from newspapers.models import Newspaper, Redactor


class NewspaperForm(forms.ModelForm):

    class Meta:
        model = Newspaper
        fields = "__all__"


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )
    )


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )

    def clean_years_of_experience(self):
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        ),
    )


class RedactorLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["years_of_experience"]

    def clean_years_of_experience(self):
        return validate_years_of_experience(self.cleaned_data["years_of_experience"])


def validate_years_of_experience(
    years_of_experience,
):
    if len(years_of_experience) != 8:
        raise ValidationError("License number should consist of 8 characters")
    elif not years_of_experience[:3].isupper() or not years_of_experience[:3].isalpha():
        raise ValidationError("First 3 characters should be uppercase letters")
    elif not years_of_experience[3:].isdigit():
        raise ValidationError("Last 5 characters should be digits")

    return years_of_experience


class TopicSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )
    )


class RegisterForm(UserCreationForm):
    agree_terms = forms.BooleanField(
        required=True,
        label='I agree all statements in Terms of service',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Redactor
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'years_of_experience']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'agree_terms':
                field.widget.attrs.update({'class': 'form-check-input me-2'})
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Redactor

        fields = ('username', 'email', 'first_name', 'last_name', 'years_of_experience')

        labels = {
            'years_of_experience': 'Years of experience',
            'first_name': 'First name',
            'last_name': 'Last name'
        }

        placeholders = {
            'years_of_experience': 'Write years of your experience'
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg',
                'placeholder': self.Meta.placeholders.get(field_name)
            })
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'

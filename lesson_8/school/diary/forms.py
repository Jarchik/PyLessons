from django import forms
from django.core.exceptions import ValidationError


class NoteForm(forms.Form):
    title = forms.CharField(min_length=5, max_length=10)
    msg = forms.CharField(min_length=10, max_length=200)
    assignee = forms.CharField(max_length=100, empty_value="")
    email = forms.CharField(max_length=100, empty_value="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].required = False
        self.fields['email'].required = False

    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data.split(' ')) < 2:
            raise ValidationError("Please create Title with at least two words")
        return data

    @staticmethod
    def check_isalpha_and_capitalized(str_to_check: str):
        if not all((str_to_check.isalpha(), str_to_check.istitle())):
            raise ValidationError("Should contain at least two words started with capitalized letter")

    def clean_assignee(self):
        data = self.cleaned_data['assignee']
        if data:
            assignee_name_and_surname = data.split(' ')
            if len(assignee_name_and_surname) < 2:
                raise ValidationError("Please create Assignee with Firstname and Surname at least")

            NoteForm.check_isalpha_and_capitalized(assignee_name_and_surname[0])
            NoteForm.check_isalpha_and_capitalized(assignee_name_and_surname[1])

        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            super().clean()

            if not data.endswith('@ithillel.ua'):
                raise ValidationError("Email domain should belong to ithillel.ua")

        return data

    def clean(self):
        super().clean()
        # NOTE: Everything work with the exchange of the cleaned_data[key] to cleaned_data.get(key)
        assignee = self.cleaned_data.get('assignee')
        email = self.cleaned_data.get('email')

        if (assignee and not email) or (email and not assignee):
            raise ValidationError("Both fields must be either specified or left empty")

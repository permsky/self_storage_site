from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2'
        )

    def clean(self):
        super().clean()
        errors = dict()
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            errors['email'] = ValidationError(
                'E-mail адрес уже используется'
            )
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password1) < 8:
            errors['password1'] = ValidationError(
                'Слишком короткий пароль'
            )
        elif password1 and password2 and password1 != password2:
            errors['password1'] = ValidationError(
                'Пароли не совпадают'
            )
        if errors:
            raise ValidationError(errors)
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        if not User.objects.filter(email=email).exists() \
                or User.objects.filter(username=email).exists():
            user.username = email
            user.email = email
            user.set_password(password1)
            user.save()

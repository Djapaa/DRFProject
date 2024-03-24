from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserCreateForm(forms.ModelForm):
    """
    Кастомная форма для создани пользователя
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Enter Password Again', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Убедимся, что две записи пароля совпадают

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Сохраним предоставленный пароль в хэшированном формате
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'avatar', 'is_active', 'is_superuser',
                  'descriptions', 'sex', 'balance')

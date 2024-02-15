from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from students.models import Group, Student



class AddStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].empty_label = 'Не выбрана'


    last_name = forms.CharField(label='Фамилия', max_length=50)
    first_name = forms.CharField(label='Имя', max_length=50)
    middle_name = forms.CharField(label='Очество', max_length=50)
    email = forms.EmailField(label='e-mail')
    birth_date = forms.DateField(label='Дата рождения')
    is_study = forms.BooleanField(label='Учится', required=False, initial=True)
    group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), empty_label='Не выбрана')
    slug = forms.SlugField(label='URL', max_length=255)

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'middle_name', 'email', 'birth_date', 'is_study', 'photo', 'group', 'slug']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise ValidationError('Недопустимые символы')
        return first_name


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class FilterStudentForm(forms.Form):
    last_name = forms.CharField(label='Фамилия', max_length=50, required=False)
    first_name = forms.CharField(label='Имя', max_length=50, required=False)
    group = forms.ModelChoiceField(label='Группа', queryset=Group.objects.all(), empty_label='', required=False)

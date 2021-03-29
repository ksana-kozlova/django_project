from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    email = forms.EmailField(label='E-Mail', max_length=128)
    password = forms.CharField(label='Password', min_length=3, max_length=128, widget=forms.PasswordInput)
    password_again = forms.CharField(label='Password, again', min_length=3, max_length=128, widget=forms.PasswordInput)


StarChoices = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]


class ReviewForm(forms.Form):

    subject = forms.CharField(label='Subject', max_length=80, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Very nice place'}))
    stars = forms.IntegerField(label='Amount of stars', widget=forms.RadioSelect(choices=StarChoices))
    text = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 80, 'rows': 10,'placeholder': 'Write something about this place'}))
    image = forms.ImageField(label='Photo of restaurant', required=False)

        
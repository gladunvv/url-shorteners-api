from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class UserCreationFormCustom(UserCreationForm):
    
    class Meta:
        model = User
    
        fields = ('username', 'password1', 'password2', 'role')

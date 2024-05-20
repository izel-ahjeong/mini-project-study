from django import forms
from .models import Users_info

class Users_infoForm(forms.ModelForm):

    class Meta:
        model=Users_info
        exclude=('user_id','user_custom_keywords', 'user_age_keywords')
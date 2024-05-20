from django import forms 
from home.models import Comment, Rating

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]
        widgets = {
            'content' : forms.TextInput(
                attrs={
                    'placeholder' : '댓글 달기...', 
                }
            )
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["ratings", ]
        widgets = {
            'ratings' : forms.Select(choices = Rating.ratings_choices)
        }
from django import forms
from SAM2018.models import Review


class AssignForm(forms.Form):
    class Meta:
        model = Review
        fields = (
            'paper_id','pcm_id'
        )


from django import forms
from .models import Timeline


class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['title', 'color']


    def __init__(self, *args, **kwargs):
        super(TimelineForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})
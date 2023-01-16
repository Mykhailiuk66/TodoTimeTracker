from django.forms import ModelForm, Form, CharField
from .models import Task, Tag

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'note', 'tags', 'priority']
        
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})
        
        
class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name',]
        
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs.update({'class': 'form-control form-control-lg'})
        
        
class UpdateTagForm(Form):
    tag_name = CharField(max_length=50)
    new_tag_name = CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(UpdateTagForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})
        
        
class DeleteTagForm(Form):
    tag_name = CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(DeleteTagForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})
        
        
        
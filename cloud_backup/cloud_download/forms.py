from django import forms
from .models import aws_data
from . import platforms

class AWS_AuthForm(forms.ModelForm):
    aws_key_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'AWS Key ID'}), label='Key Id', max_length=100)
    aws_key = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'AWS Key'}), label='Key', max_length=100)
    class Meta:
        model = aws_data
        managed = False
        fields = ('aws_key_id', 'aws_key',)

    def clean_message(self):
            aws_key_id = self.cleaned_data.get('aws_key_id')
            aws_key = self.cleaned_data.get('aws_key')
            try:
                platforms.aws.aws(aws_key_id, aws_key).get_image_list()
            except:
                forms.ValidationError("Incorrect username or password")
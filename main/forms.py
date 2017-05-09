from django import forms
from .models import Question
# from .widgets import WYMEditor
# from tinymce import models as tinymce_models
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
class CreateQuestionForm(forms.Form):
	title=forms.CharField()
	content=forms.CharField(widget=forms.Textarea,required=False)	

	def clean(self,*args,**kwargs):
		title=self.cleaned_data.get("title")
		content=self.cleaned_data.get('content')
		user_id=self.cleaned_data.get('user_id')
		return super(CreateQuestionForm,self).clean(*args,**kwargs)	

class CreateAnswerForm(forms.Form):
	content=forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

	class Meta:
		model = FlatPage
	
		
	

	

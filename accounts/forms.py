from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)
from django.contrib.auth.models import User
from .models import UserProfile

class UserLoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
	

	def clean(self,*args,**kwargs):
		username=self.cleaned_data.get("username")
		password=self.cleaned_data.get('password')
		if username and password:
			try:
				user=User.objects.get(username=username)
				if not user.check_password(password):
					raise forms.ValidationError("Incorrect Password.")					
				if not user.is_active:
					raise forms.ValidationError("This user is no longer active.")
			except User.DoesNotExist:
				raise forms.ValidationError("This user does not exists.")		

		return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegisterForm(forms.ModelForm):
	rusername=forms.RegexField(regex=r'^\w+$',widget=forms.TextInput(attrs=dict(required=True, max_length=30,placeholder="Username")),error_messages={ 'invalid':("This value must contain only letters, numbers and underscores.")})
	password1=forms.CharField(widget=forms.PasswordInput(dict(placeholder="Password")),label="Password")
	password2=forms.CharField(widget=forms.PasswordInput(dict(placeholder="Confirm Password")),label="Confirm Password")	
	email=forms.EmailField(required=True,widget=forms.EmailInput(dict(placeholder="Email")))
	class Meta:
		model=User
		fields=("rusername","email","password1","password2")
	def clean_rusername(self):
		try:
			user=User.objects.get(username=self.cleaned_data["rusername"])
		except User.DoesNotExist:
			return self.cleaned_data["rusername"]
		raise forms.ValidationError("This username has already been taken.Please try another one")		

	def clean_password2(self):
		if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
			if self.cleaned_data["password1"]!=self.cleaned_data["password2"]:
				raise forms.ValidationError("The two password fields doesn't match.")
		return self.cleaned_data["password2"]
	def clean_email(self):
		try:
			user=User.objects.get(email=self.cleaned_data["email"])
		except User.DoesNotExist:
			return self.cleaned_data["email"]
		raise forms.ValidationError("This email is already registered.Please try another one.")	
							 
	def save(self,commit=True):
		user=super(UserRegisterForm,self).save(commit=False)
		user.username=self.cleaned_data["rusername"]
		user.set_password(self.cleaned_data["password1"])
		user.email=self.cleaned_data["email"]

		if commit:
			user.save()
		return user

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model=User
		fields=["first_name","last_name","email"]
	def save(self,commit=True):
		user=super(UserUpdateForm,self).save(commit=False)
		user.first_name=self.cleaned_data["first_name"]
		user.last_name=self.cleaned_data["last_name"]
		user.email=self.cleaned_data["email"]

		if commit:
			user.save()

class ProfileUpdateForm(forms.ModelForm):
	location=forms.CharField(required=False)
	description=forms.CharField(required=False)
	city=forms.CharField(required=False)
	website=forms.URLField(required=False)
	phone=forms.RegexField(regex=r'^\+?1?\d{9,15}$')
	class Meta:
		model=UserProfile
		fields=["location","description","city","website","phone","image"]
	def save(self,user,commit=True):
		profile=super(ProfileUpdateForm,self).save(commit=False)
		if user:
			profile.user=user
			profile.location=self.cleaned_data["location"]
			profile.description=self.cleaned_data["description"]
			profile.city=self.cleaned_data["city"]
			profile.website=self.cleaned_data["website"]
			profile.phone=self.cleaned_data["phone"]	
			profile.image=self.cleaned_data["image"]	
		profile.save()		


from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)
from django.views.generic import TemplateView,UpdateView
from django.shortcuts import render,redirect
from .forms import UserLoginForm,UserRegisterForm,ProfileUpdateForm,UserUpdateForm
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Question,Answer
from django.http import HttpResponse
from .models import Relationship
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


class LoginRegisterView(TemplateView):
	template_name="accounts/loginregister.html"
	def get(self,request):
		login_form=UserLoginForm(None)
		register_form=UserRegisterForm(None)
		return render(request,self.template_name,{"login":login_form,"register":register_form})

	def post(self,request,*args,**kwargs):
		if "login" in request.POST:
			login_form=UserLoginForm(request.POST)
		else:
			login_form=UserLoginForm()		
		if "register" in request.POST:
			register_form=UserRegisterForm(request.POST)
		else:
			register_form=UserRegisterForm()	
		

		if login_form.is_valid():
			username=login_form.cleaned_data.get("username")
			password=login_form.cleaned_data.get("password")
			user=authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				return redirect(reverse("main:latest_answers"))
				
		if register_form.is_valid():
			login(request,register_form.save())
			return redirect(reverse("main:latest_answers"))

		return render(request,self.template_name,{"login":login_form,"register":register_form})					
		

class LogoutView(TemplateView):
	template_name="accounts/logout.html"
	def get(self,request):
		logout(request)
		return redirect("accounts:login")

# class RegisterView(TemplateView):
# 	template_name="accounts/register.html"
# 	def get(self,request):
# 		form=UserRegisterForm()
# 		return render(request,self.template_name,{"form":form,"title":"Register"})
# 	def post(self,request,*args,**kwargs):
# 		form=UserRegisterForm(request.POST)
# 		if form.is_valid():
# 			login(request,form.save())
# 			return redirect(reverse("posts:list"))	

class ProfileAnswerView(TemplateView):
	def get(self,request,username):
		if request.user.username == username:
			answers=Answer.objects.filter(user_id=request.user)
			count={
				"answers":answers.count(),
				"followers":Relationship.objects.filter(user_to=request.user.userprofile).count(),
				"questions":Question.objects.filter(user=request.user).count()
			}
			return render(request,"accounts/user/profile-answers.html",{"answers":answers,"count":count})									
		else:
			result=User.objects.get(username=username)
			answers=Answer.objects.filter(user_id=result)
			count={
				"answers":answers.count(),
				"followers":Relationship.objects.filter(user_to=result.userprofile).count(),
				"questions":Question.objects.filter(user=result).count()
			}	
			return render(request,"accounts/others/profile-answers.html",{"result":result,"answers":answers,"count":count})	

class ProfileQuestionView(TemplateView):
	def get(self,request,username):
		if request.user.username==username:
			questions=Question.objects.filter(user=request.user)
			count={
				"answers":Answer.objects.filter(user_id=request.user).count(),
				"followers":Relationship.objects.filter(user_to=request.user.userprofile).count(),
				"questions":questions.count()
			}
			return render(request,"accounts/user/profile-questions.html",{"questions":questions,"count":count})
		else:
			result=User.objects.get(username=username)
			questions=Question.objects.filter(user_id=result)
			count={
				"answers":Answer.objects.filter(user_id=result).count(),
				"followers":Relationship.objects.filter(user_to=result.userprofile).count(),
				"questions":questions.count()
			}		
			return render(request,"accounts/others/profile-questions.html",{"result":result,"questions":questions,"count":count})

class ProfileFollowersView(TemplateView):
	def get(self,request,username):
		if request.user.username==username:
			followers=Relationship.objects.filter(user_to=request.user.userprofile)
			count={
				"answers":Answer.objects.filter(user_id=request.user).count(),
				"followers":followers.count(),
				"questions":Question.objects.filter(user_id=request.user).count()
			}
			return render(request,"accounts/user/profile-followers.html",{"followers":followers,"count":count})
		else:	
			result=User.objects.get(username=username)
			followers=Relationship.objects.filter(user_to=result.userprofile)
			count={
				"answers":Answer.objects.filter(user_id=result).count(),
				"followers":followers.count(),
				"questions":Question.objects.filter(user_id=result).count()
			}
			return render(request,"accounts/others/profile-followers.html",{"result":result,"followers":followers,"count":count})				

class ProfileFollowingView(TemplateView):
	def get(self,request,username):
		if request.user.username==username:
			count={
				"answers":Answer.objects.filter(user_id=request.user).count(),
				"followers":Relationship.objects.filter(user_to=request.user.userprofile).count(),
				"questions":Question.objects.filter(user_id=request.user).count()
			}
			return render(request,"accounts/user/profile-following.html",{"count":count})
		else:
			result=User.objects.get(username=username)
			count={
				"answers":Answer.objects.filter(user_id=result).count(),
				"followers":Relationship.objects.filter(user_to=result.userprofile).count(),
				"questions":Question.objects.filter(user_id=result).count()
			}
			return render(request,"accounts/others/profile-following.html",{"result":result,"count":count})


class ProfileUpdateView(TemplateView):
	template_name="accounts/profile_update.html"
	def get(self,request):
		user_form=UserUpdateForm(instance=request.user)
		profile=ProfileUpdateForm(instance=request.user.userprofile)
		return render(request,self.template_name,{"user_form":user_form,"profile":profile,"title":"Profile Update"})

	def post(self,request,*args,**kwargs):
		if request.method=="POST" and "user_submit" in request.POST:
			user_form=UserUpdateForm(request.POST,instance=request.user)
			if user_form.is_valid():
				user_form.save()
				return redirect("accounts:profile_edit")

		if request.method=="POST" and "profile_submit" in request.POST:
			profile=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
			if profile.is_valid():
				profile.save(request.user)
				return redirect("accounts:profile_edit")

def follow_user(request):
	user_id=request.GET.get("id")
	action=request.GET.get("action")
	if user_id and action:
		try:
			user=User.objects.get(id=user_id).userprofile
			if action=="follow":
				Relationship.objects.get_or_create(user_from=request.user.userprofile,user_to=user)
			else:
				Relationship.objects.filter(user_from=request.user.userprofile,user_to=user).delete()
			count=Relationship.objects.filter(user_to=user).count()	

			return JsonResponse({'status':'ok',"followers":count})
		except User.DoesNotExist:
			return JsonResponse({'status':'ko'})
	return JsonResponse({'status':'ko'})		

def change_password(request):
	if request.method=="POST":
		form=PasswordChangeForm(data=request.POST,user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request,form.user)
			return redirect("/main/")
		else:
			return redirect("/account/change-password")	
	else:
		form=PasswordChangeForm(user=request.user)
		return render(request,"accounts/change-password.html",{"form":form})


def profile_update(request,username):
	if request.user.username==username:
		if ("first_name","last_name") in request.GET:
			print("true")
		else:
			print("false")	


	
	return JsonResponse({"status":"ko"})	











# def login_view(request):
# 	title="login"
# 	form=UserLoginForm(request.POST or None)
# 	if form.is_valid():
# 		username=form.cleaned_data.get("username")
# 		password=form.cleaned_data.get("password")
# 		user=authenticate(username=username,password=password)
# 		login(request,user)
		
# 	if request.user.is_authenticated():
# 		return redirect('posts:list')	
# 	return render(request,"accounts/index.html",{"form":form,"title":title})

# def register_view(request):
# 	return render(request,"form.html",{})

# def logout_view(request):
# 	logout(request)
# 	return redirect('login')	

# def about_view(request):
# 	template_name='accounts/about.html'	
# 	return render(request,template_name)
# def show_view(request,id):
# 	template_name='accounts/show.html'
# 	return render(request,template_name,{'user':request.user})	




		
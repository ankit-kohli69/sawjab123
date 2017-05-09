from django.contrib import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post
from .forms import PostForm
def post_create(request):
	form=PostForm(request.POST or None)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,'Successfully Created.')
		return redirect('posts:list')
	context={
		"form":form,
		'title':'Create'
	}
	return render(request,'posts/form.html',context)

def post_detail(request,id):
	post_object=get_object_or_404(Post,pk=id)
	context={
		'title':"Detail",
		'object':post_object,
	}
	return render(request,'posts/detail.html',context)

def post_update(request,id):
	instance=get_object_or_404(Post,pk=id)
	form=PostForm(request.POST or None,instance=instance)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,'Saved')
		return redirect(instance.get_absolute_url())
	context={
		'title':"Update",
		#'instance':instance,
		'form':form,
	}
	return render(request,'posts/form.html',context)

def post_list(request):
	if request.user.is_authenticated():
		queryset=Post.objects.all()
		context={
			'title':"List",
			'posts':queryset,
		}
		return render(request,'posts/index.html',context)
	return redirect('login')	
def post_delete(request,id=None):
	instance=get_object_or_404(Post,id=id);
	instance.delete()
	messages.success(request,'Post Deleted')
	return redirect('posts:list')

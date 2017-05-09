from django.shortcuts import render,get_object_or_404,redirect,reverse
from .forms import CreateQuestionForm,CreateAnswerForm
from django.contrib import messages
from .models import Question,Answer,Comment
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from django.http import JsonResponse,HttpResponseRedirect

def question_create(request):
	title=request.POST.get('question_content')
	if title:
		q=Question(title=title,content="",user_id=request.user.id)
		q.save()	
		return redirect("main:answer_all",id=q.id)
	return HttpResponseRedirect(request.META.get("HTTP_REFERER"))		

def question_list(request):
	results=Question.objects.filter(user_id=request.user.id)
	count_ans=list()
	for result in results:
		count_ans.append(Answer.objects.filter(question_id=result.id).count)	
	context={
		'results':results,
		"count":count_ans,
		'title':'Questions asked by you'
	}
	return render(request,'main/list.html',context)	

def question_list_all(request):
	results=Question.objects.all().order_by("-timestamp")
	context={
		'results':results
	}
	return render(request,'main/listall.html',context);	

def answer_all(request,id):
	question=get_object_or_404(Question,pk=id);
	results=question.answer_set.all()
	context={
		'results':results,
		'title':'Answer',
		'question':question
	}
	return render(request,'main/answerall.html',context)

def answer_create(request,id):
	form=CreateAnswerForm(request.POST or None)
	question=Question.objects.get(pk=id)
	if form.is_valid():
		content=request.POST.get('content','')
		user_id=request.POST.get('user_id','')
		answer=Answer(question=question,content=content,user_id=request.user.id)
		answer.save()	
		messages.success(request,'Answer Successfully Submitted')
		return redirect('main:answer_all',id=id)
	context={
		'title':'Add Answer',
		'form':form,
		'question':question
	}
	return render(request,'main/form.html',context)

def answer_show(request,id):
	answer=get_object_or_404(Answer,pk=id)
	return render(request,'main/showanswer.html',{"answer":answer})

def latest_answers(request):
	lans=Answer.objects.raw("SELECT a.id from main_answer a join (select max(id) as id from main_answer group by question_id) b on a.id=b.id join main_question q on  q.id=a.question_id order by a.id desc")	
	# lques=Question.objects.all().order_by("-timestamp")[:20]
	# latest_answers=Answer.objects.all().order_by("-timestamp")[:20]
	# latest_qa=list(latest_answers)+list(latest_questions)
	# latest_qa.sort(key=lambda x:x.timestamp,reverse=True)
	# print(latest_qa)
	return render(request,"main/main.html",{"lans":lans})

def answer_like(request):
	answer_id=request.GET.get("id")
	action=request.GET.get("action")
	if answer_id and action:
		try:
			answer=Answer.objects.get(id=answer_id)
			if action=="like":
				answer.likes.add(request.user)
			else:
				answer.likes.remove(request.user)
			return JsonResponse({"status":"ok","count":answer.likes.count()})
		except Answer.DoesNotExist:
			return JsonResponse({"status":"ko"})
	return JsonResponse({"status":"ko"})	

def answer_comment(request):
	answer_id=request.GET.get("id")
	content=request.GET.get("content")
	if answer_id and content:
		try:
			answer=Answer.objects.get(id=answer_id)
			Comment.objects.get_or_create(user=request.user,answer=answer,content=content)
			return JsonResponse({"status":"ok","count":answer.comments.count(),"current":[{"username":request.user.username,"content":content}]})
		except Answer.DoesNotExist:
			return JsonResponse({"status":"ko"})
	return JsonResponse({"status":"ko"})

def get_answer_comment(request):
	answer_id=request.GET.get("id")
	if answer_id:
		try:
			comments=list()
			answer=Answer.objects.get(id=answer_id)
			if answer.comments.count():
				for comment in Comment.objects.filter(answer=answer).order_by("-id"):
					comments.append({"username":comment.user.username,"content":comment.content})
				
			# comments.append({"username":"taylor","content":"I lOve TS"})
			# comments.append({"username":"ankit","content":"I lOve AK"})
			return JsonResponse({"status":"ok","comments":comments})
		except Answer.DoesNotExist:
			return JsonResponse({"status":"ko"})
	return JsonResponse({"status":"ko"})

def question_followers(request):
	qid=request.GET.get("id")
	action=request.GET.get("action")
	if qid and action:
		try:
			q=Question.objects.get(id=qid)
			if action=="follow":
				q.followers.add(request.user)
			else:
				q.followers.remove(request.user)
			return JsonResponse({"status":"ok","count":q.followers.count()})
		except Question.DoesNotExist:
			return JsonResponse({'status':'ko'})
	return JsonResponse({'status':'ko'})













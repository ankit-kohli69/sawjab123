from django.contrib.auth.models import User
from main.models import Question
from django.views.generic import ListView
import operator
from django.db.models import Q
from functools import reduce
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
class SearchView(ListView):
	template_name="main/search_results.html"
	context_object_name="results"
	def get_queryset(self):
		results=Question.objects.all()
		users=User.objects.all()
		query=self.request.GET.get("q")
		print(query)
		if query:
			query_list=query.split()
			print(query_list)
			results=results.filter(
				reduce(operator.and_,(Q(title__icontains=q) for q in query_list))
				)
			users=users.filter(
				reduce(operator.and_,(Q(username__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q) for q in query_list))
				)
		return {"results":results,"users":users}

def autocomplete(request):
    if request.is_ajax():
        queryset = User.objects.filter(username__startswith=request.GET.get('search', None))
        results=Question.objects.all()
        query=request.GET.get('search', None)
        query_list=query.split()
        results=results.filter(
				reduce(operator.and_,(Q(title__icontains=q) for q in query_list))
				)
        users = []
        users_urls=[]  
        questions=[]
        questions_urls=[]      
        for i in queryset:
            users.append(i.username)
            users_urls.append(reverse("accounts:profile",kwargs={"username":i.username}))
        for j in results:
        	questions.append(j.title) 
        	questions_urls.append(reverse("main:answer_all",kwargs={"id":j.id}))  			   
        data = {
            'users': users,
            'users_urls':users_urls,
            'questions':questions,
            'questions_urls':questions_urls

        }
        return JsonResponse(data)			

def index_redirect(request):
    if request.user.is_authenticated():
        return redirect("main:latest_answers")
    else:    
        return redirect("accounts:login")	
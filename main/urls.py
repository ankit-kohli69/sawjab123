from django.conf.urls import url
from . import views
app_name='main'
urlpatterns = [
	url(r'^question/create',views.question_create,name='question_create'),
	url(r'^question/list',views.question_list,name='question_list'),
	url(r'^question/$',views.question_list_all,name='question_list_all'),
	url(r'^question/(?P<id>\d+)/$',views.answer_all,name='answer_all'),
	url(r'^question/(?P<id>\d+)/answer/create/$',views.answer_create,name='answer_create'),
	url(r'^question/followers/$',views.question_followers,name="question_followers"),
	url(r'^answer/(?P<id>\d+)/$',views.answer_show,name='answer_show'),
	url(r'^$',views.latest_answers,name="latest_answers"),
	url(r'^like/$',views.answer_like,name="answer_like"),
	url(r'^comment/$',views.answer_comment,name="answer_comment"),
	url(r'^comment/get$',views.get_answer_comment,name="get_answer_comment")
]

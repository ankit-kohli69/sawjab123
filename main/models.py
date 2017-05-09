from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
	name = models.CharField(max_length=50)
	followers = models.ManyToManyField(User, related_name='topic_followers')	

class Question(models.Model):
	title=models.CharField(max_length=150)
	content=models.TextField(blank=True,null=True)
	user=models.ForeignKey(User)
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	followers = models.ManyToManyField(User, related_name='question_followers')
	topics = models.ManyToManyField(Topic, related_name='topic_questions')

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title	

class Answer(models.Model):
	question=models.ForeignKey(Question,on_delete=models.CASCADE)
	content=models.TextField()
	user=models.ForeignKey(User)
	likes=models.ManyToManyField(User,blank=True,related_name="answer_likes")
	comments=models.ManyToManyField(User,blank=True,related_name="answer_comments",through="Comment")
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	# def __unicode__(self):
	# 	return self.title

	def __str__(self):
		return str(self.user)

class Comment(models.Model):
	user=models.ForeignKey(User)
	answer=models.ForeignKey(Answer)
	content=models.TextField()
	created=models.DateTimeField(auto_now_add=True,db_index=True)





"""class Like(models.Model):
		user=models.ForeignKey(User)
		answer=models.ForeignKey(Answer)
		created=models.DateTimeField(auto_now_add=True,db_index=True)
	
	class Comment(models.Model):
		user=models.ForeignKey(User)
		answer=models.ForeignKey(Answer)
		content=models.TextField()
		created=models.DateTimeField(auto_now_add=True,db_index=True)"""	




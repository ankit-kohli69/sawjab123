from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
class UserProfile(models.Model):
	user=models.OneToOneField(User)
	location=models.CharField(max_length=255,blank=True,null=True)
	description=models.TextField(blank=True,null=True)
	city=models.CharField(max_length=100,default='',blank=True,null=True)
	website=models.URLField(default='',blank=True,null=True)
	phone=models.CharField(max_length=15,blank=True,null=True,unique=True)
	image=models.ImageField(upload_to="profile_image",blank=True)
	follow=models.ManyToManyField("self",symmetrical=False,through="Relationship")
	 
	def __str__(self):
		return self.user.username

class Relationship(models.Model):
	user_from=models.ForeignKey(UserProfile,related_name="who")
	user_to=models.ForeignKey(UserProfile,related_name="whom")
	created=models.DateTimeField(auto_now_add=True,db_index=True)

	def __str__(self):
		return "{} follows {}".format(self.user_from,self.user_to)
#Add following Field Dynamically
#User.add_to_class('following',models.ManyToManyField('self',through=Relationship,related_name="followers",symmetrical=False))			

def create_profile(sender,**kwargs):	
	if kwargs["created"]:
		user_profile=UserProfile.objects.create(user=kwargs["instance"])

post_save.connect(create_profile,sender=User)		
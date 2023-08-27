from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Session(models.Model):
    group=models.IntegerField(default=0,blank=True)

    def __str__(self):
        return str(self.group)

class Main_user(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    my_session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True,blank=True)
    roll_no=models.TextField()
    is_gr=models.BooleanField(default=False)
    is_cr=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Slides(models.Model):
    my_session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    sub_name=models.TextField()
    code=models.TextField()
    link=models.TextField()

    def __str__(self):
        return str(self.sub_name) + ' - ' + str(self.code)
    
class Notification(models.Model):
    my_session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    information=models.TextField()
    created_on=models.DateTimeField(default=datetime.datetime.now())
    
    # def save(self,*args,**kwars):

    def __str__(self):
        return str(self.created_on)
    
class Deadline(models.Model):
    my_session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    my_slide=models.ForeignKey(Slides,on_delete=models.CASCADE,null=True)
    sub_name=models.TextField()
    code=models.TextField()
    information=models.TextField()
    created_on=models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return str(self.sub_name) + '-'+ str(self.created_on)
    
class Evaluation(models.Model):
    my_session=models.ForeignKey(Session,on_delete=models.CASCADE,null=True)
    my_slide=models.ForeignKey(Slides,on_delete=models.CASCADE,null=True)
    sub_name=models.TextField()
    code=models.TextField()
    eval_type=models.TextField()
    eval_room=models.TextField()
    eval_information=models.TextField()
    created_on=models.DateTimeField(default=datetime.datetime.now())
    
    def __str__(self):
        return str(self.sub_name) + '-' + str(self.eval_type) + '-' + str(self.created_on)
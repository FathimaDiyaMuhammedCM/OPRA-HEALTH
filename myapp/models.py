from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class Users(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    phone= models.BigIntegerField()
    image= models.CharField(max_length=400)
    pin= models.IntegerField()
    post= models.CharField(max_length=100)
    place= models.CharField(max_length=100)
    gender= models.CharField(max_length=100)
    dob= models.DateField()
   
    USER=models.OneToOneField(User,on_delete=models.CASCADE)





class Complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=200)
    reply=models.CharField(max_length=200)
    status=models.CharField(max_length=50)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)



class Feedback(models.Model):
    date=models.DateField()
    feedback=models.CharField(max_length=200)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)




class Workouts(models.Model):
    date=models.DateField()
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    file=models.CharField(max_length=400)
    video=models.CharField(max_length=400)
    is_cardiac = models.CharField(max_length=50)
    body_type = models.CharField(max_length=50)
    bmi = models.CharField(max_length=50)
    bp = models.CharField(max_length=50)
    cholestrol = models.CharField(max_length=50)
    sugar_level = models.CharField(max_length=50)
    thyroid_status = models.CharField(max_length=50)
    vitamin_d_level = models.CharField(max_length=50)
    smoking = models.CharField(max_length=50)
    alcohol_consumption = models.CharField(max_length=50)
    physical_activity_level = models.CharField(max_length=50)



class Facial_emotion(models.Model):
    date=models.DateField()
    time=models.TimeField()
    emotion=models.CharField(max_length=200)
    photo=models.CharField(max_length=400)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)


class Chat(models.Model):
    date=models.DateField()
    time=models.TimeField()
    message=models.CharField(max_length=200)
    FROM=models.ForeignKey(User,on_delete=models.CASCADE,related_name="from_id")


class Posts(models.Model):
    date=models.DateField()
    time=models.TimeField()
    content=models.CharField(max_length=500)
    photo=models.CharField(max_length=400)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)

class Comments(models.Model):
    date=models.DateField()
    time=models.TimeField()
    content=models.CharField(max_length=500)
    POSTS=models.ForeignKey(Posts,on_delete=models.CASCADE)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)


   
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class studentuser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=19,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=44,null=True)
    type=models.CharField(max_length=44,null=True)
    def __str__(self):
        return self.user.username
class recruiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=19,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=44,null=True)
    company=models.CharField(max_length=100,null=True)
    type=models.CharField(max_length=44,null=True)
    status=models.CharField(max_length=40,null=True)
    

    def __str__(self):
        return self.user.username
class job(models.Model):
    recruiter=models.ForeignKey(recruiter,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    title=models.CharField(max_length=100)
    salary=models.FloatField(max_length=100)
    image=models.FileField()
    description=models.CharField(max_length=300)
    experience=models.CharField(max_length=40)
    location=models.CharField(max_length=400)
    skills=models.CharField(max_length=100)
    creationdate=models.DateField(max_length=40,null=True)
    def __str__(self):
        return self.title
class apply(models.Model):
    Job=models.ForeignKey(job,on_delete=models.CASCADE)
    student=models.ForeignKey(studentuser,on_delete=models.CASCADE)
    resume=models.FileField(null=True)
    applydate=models.DateField()
    title = models.CharField(max_length=100, default='Job Application')
    def __str__(self):
        return self.title


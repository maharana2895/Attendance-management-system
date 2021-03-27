from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class UserType(models.Model):
    # User Type Table Field: User Type
    caption = models.CharField(max_length=10)

    def __str__(self):
        return self.caption


class ClassInfo(models.Model):
    # Class Information Table Field: Class Name
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class MajorInfo(models.Model):
    # Professional Information Form Field: Professional Name
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    #reate user model, student number, password, class, name, nickname, professional, user type, phone, name, motto, mail
    studentNum = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=64)
    username = models.CharField(max_length=15)
    cid = models.ForeignKey('ClassInfo', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, null=True)
    major = models.ForeignKey('MajorInfo', on_delete=models.CASCADE,)
    hobby = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    user_type = models.ForeignKey(to='UserType',on_delete=models.CASCADE)
    gender = models.IntegerField(default=1)
    phone = models.CharField(max_length=11)
    motto = models.TextField(null=True)
    email = models.EmailField(null=False)

    def __str__(self):
        return self.username

# Sign-in form design
class Attendence(models.Model):
    #Check-in table Field: User, check-in time, check-out time, description Others are for convenience of operation.
    stu = models.ForeignKey('UserInfo',on_delete=models.CASCADE,)
    # cur_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now)
    # state=models.BooleanField(default=False)
    is_leave = models.BooleanField(default=False)
    detail = models.TextField(default='no')
    leave_count = models.IntegerField(default=0)

    def __str__(self):
        return self.stu.username



# Bulletin design
class Notice(models.Model):
    # Announcement Form Field: Publisher, Release Date, Release Title, Post Content, Release Level
    author = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now=True)
    head = models.TextField(max_length=200)
    content = models.TextField(max_length=500)
    level = models.IntegerField(default=0)



# Leave design
class Leave(models.Model):
    # Leave form Field: User, start time, end time, leave reason
    user = models.ForeignKey(to='UserInfo',on_delete=models.CASCADE)
    start_time = models.DateField(null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    explain = models.TextField(default='no', max_length=500)




# Examination content
# Assessment content table: title, name, review status
class ExamContent(models.Model):
    title = models.TextField(max_length=200)
    date = models.DateField(auto_now=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.title


# Assessment transcript design
class Exam(models.Model):
    # Assessment transcript field: user, assessment content, score, remarks
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,)
    content = models.ForeignKey(to='ExamContent',on_delete=models.CASCADE)
    point = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    detail = models.TextField(max_length=200, default="no")
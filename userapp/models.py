from django.db import models
from instructorapp.models import *
# Create your models here.
class StudentRegModel(models.Model):
    student_id = models.AutoField(primary_key=True)
    full_name = models.CharField(help_text='Enter full Name', max_length=100,null=True)
    email = models.EmailField(max_length=100, help_text='Enter Email Address',null=True)
    phone_number = models.BigIntegerField()
    # gender = models.CharField(max_length=100,default='gender',null=True)
    photo =models.ImageField(upload_to='images/',default='image',null=True)
    password = models.CharField(max_length=10, help_text='Enter Password',null=True)
    # status = models.CharField(default='Pending',max_length=100, null=True)
    reg_date = models.DateField(auto_now_add=True, null=True)
    address = models.CharField(max_length=255)
    otp = models.CharField(max_length=6,default=0) 
    otp_status = models.CharField(max_length=15, default='Not Verified')

    class Meta:
        db_table= 'Student_Details'




class CartModel(models.Model):
    cart_user=models.ForeignKey(StudentRegModel,on_delete=models.CASCADE)
    cart_booking=models.ForeignKey(Addcourse,on_delete=models.CASCADE)

    class Meta:
        db_table='cart_details'



class StudentCourses(models.Model):
    student = models.ForeignKey(StudentRegModel,on_delete=models.SET_NULL,null=True,related_name='student_courses')
    course = models.ForeignKey(Addcourse,on_delete=models.SET_NULL,null=True)
    amount = models.IntegerField(help_text='Enter fee',default=0)
    payment_status= models.CharField(max_length=100,default="pending")
    purchase_date = models.DateField(auto_now_add=True, null=True)
    # payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    certificate_downloaded = models.BooleanField(default=False)
    class Meta:
        db_table = 'student_courses_details'




class UserTestModel(models.Model):
    test_user = models.ForeignKey(StudentRegModel,on_delete=models.CASCADE,null=True,related_name='user_results')
    test_name = models.CharField(max_length=155,unique=True)
    test_date = models.DateField(auto_now_add=True)
    test_marks = models.IntegerField(default=0)

    class Meta:
        db_table = 'User_tests_details'


class ResultModel(models.Model):
    result_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    test_id = models.IntegerField(null=True)
    test_name = models.CharField(max_length=155)
    question = models.CharField(max_length=155)
    useranswer = models.CharField(max_length=55)
    correctanswer = models.CharField(max_length=55)
    marks=models.IntegerField()
    result_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'Student_Result_Details'






class StudentFeedback(models.Model):
    student = models.ForeignKey(StudentRegModel, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    rating = models.IntegerField()
    additional_comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student_feedback'



class Conversation(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message[:50]}..."





class Conversation(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"User: {self.user_message[:50]}..."
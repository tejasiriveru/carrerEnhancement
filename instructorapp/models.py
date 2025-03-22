from django.db import models

# Create your models here.
class InstructorRegModel(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=100,help_text="Enter Email")
    phone_number = models.BigIntegerField(null=True)
    gender =models.CharField(max_length=50,default=False)
    # experience = models.CharField(max_length=100)
    # category = models.CharField(help_text='Select Category',max_length=50,default='category')   
    password = models.CharField(max_length=100,help_text="Enter Password")
    photo = models.ImageField(default=False)
    status = models.CharField(default='Pending',max_length=100, null=True)
    reg_date = models.DateField(auto_now_add=True, null=True)
    address = models.CharField(max_length=255)
    otp = models.CharField(max_length=6,default=0) 
    otp_status = models.CharField(max_length=15, default='Not Verified')
    

    class Meta:
        db_table = 'Instructor_Details'




class Addcourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    course_image = models.ImageField(upload_to='course_images/')
    course_category = models.CharField(max_length=100)
    course_language = models.CharField(max_length=100)
    course_description = models.TextField()
    video_url = models.URLField()
    duration_weeks = models.IntegerField()
    price = models.IntegerField(default=0,help_text='Enter fee ')
    added_date = models.DateField(auto_now_add=True, null=True)



    class Meta:
        db_table = 'Courses_details'

from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    publication_date = models.DateTimeField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    candidate_required_location = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    cover_letter = models.TextField()
    resume = models.FileField(upload_to="resumes/")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"

class Question(models.Model):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    QUESTION_TYPES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    instructor = models.ForeignKey(InstructorRegModel, on_delete=models.CASCADE)
    course = models.ForeignKey(Addcourse, on_delete=models.CASCADE)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, null=True)

    class Meta:
        db_table = 'Questions'
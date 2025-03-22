from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
import os
from userapp.models import *
from instructorapp.models import *
from django.utils.datastructures import MultiValueDictKeyError
import random
import urllib.request
import urllib.parse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Create your views here.

def ins_logout(request):
    logout(request)
    messages.info(request,"Logout Successfully ")
    return redirect('instructor_login')




def ins_dashboard(request):
    current_logined_ins = request.session.get('ins_id_after_login')
    total_courses = Addcourse.objects.filter(instructor=current_logined_ins).count()
    total_questions = Question.objects.filter(instructor=current_logined_ins).count()
    total_students = StudentRegModel.objects.count()
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_questions': total_questions,
    }
    return render(request, 'instructor/index.html', context)



def add_courses(request):
    current_logined_ins = request.session.get('ins_id_after_login')
    if request.method == 'POST':
        instructor_id = current_logined_ins
        course_name = request.POST.get('courseName')
        if Addcourse.objects.filter(instructor_id=instructor_id, course_name=course_name).exists():
            messages.error(request, 'Course with the same name already exists')
            return redirect('add_courses')
        else:
            course_image = request.FILES.get('courseImage')
            course_category = request.POST.get('courseCategory')
            course_language = request.POST.get('courseLanguage')
            course_description = request.POST.get('courseDescription')
            video_url = request.POST.get('videourl')
            duration_weeks = request.POST.get('courseDuration')
            price = request.POST.get('coursePrice')
            course = Addcourse.objects.create(
                instructor_id=instructor_id,
                course_name=course_name,
                course_image=course_image,
                course_category=course_category,
                course_language=course_language,
                course_description=course_description,
                video_url=video_url,
                duration_weeks=duration_weeks,
                price=price
            )
            messages.success(request,"Course Added Successfully")
            return redirect('add_courses')
    return render(request, "instructor/add-courses.html")


def view_courses(request):
    current_logined_ins = request.session.get('ins_id_after_login')
    courses = Addcourse.objects.filter(instructor_id=current_logined_ins)
    paginator = Paginator(courses, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, "instructor/view-courses.html", context)



def add_question(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    if request.method == 'POST':
        course_id = request.POST.get('courseSelect')
        course = Addcourse.objects.get(pk=course_id)
        question_text = request.POST.get('questionText')
        option_a = request.POST.get('optionA')
        option_b = request.POST.get('optionB')
        option_c = request.POST.get('optionC')
        option_d = request.POST.get('optionD')
        correct_answer = request.POST.get('correctAnswer')
        question_type = request.POST.get('questionType')
        Question.objects.create(
            instructor_id=current_instructor_id,
            course=course,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            question_type=question_type,
        )
        messages.success(request, "Question Added Successfully")
        return redirect('add_question')  
    return render(request, "instructor/add-questions.html", {'instructor_courses': instructor_courses})



def all_questions(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_questions = Question.objects.filter(instructor_id=current_instructor_id).order_by('-id')
    paginator = Paginator(instructor_questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "instructor/all-questions.html", {'page_obj': page_obj})


def remove_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    messages.info(request,"Deleted Successfully !")
    return redirect('all_questions') 


def view_students(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    if current_instructor_id is None:
        return HttpResponse("Instructor ID not found in session")
    course_students = StudentCourses.objects.filter(course__instructor=current_instructor_id).values('course__course_name').annotate(num_students=Count('student'))
    return render(request, "instructor/view-students.html", {'course_students': course_students})



def view_student_feedbacks(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    course_names = courses.values_list('course_name', flat=True)
    feedbacks = StudentFeedback.objects.filter(course_name__in=course_names)
    paginator = Paginator(feedbacks, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, "instructor/view-feedbacks.html", context)



def feedbacks_graph(request):
    current_instructor_id = request.session.get('ins_id_after_login')
    instructor_courses = Addcourse.objects.filter(instructor_id=current_instructor_id)
    course_names = [course.course_name for course in instructor_courses]
    feedbacks = StudentFeedback.objects.filter(course_name__in=course_names)
    rating_counts = {
        'rating1': feedbacks.filter(rating=1).count(),
        'rating2': feedbacks.filter(rating=2).count(),
        'rating3': feedbacks.filter(rating=3).count(),
        'rating4': feedbacks.filter(rating=4).count(),
        'rating5': feedbacks.filter(rating=5).count(),
    }
    return render(request, "instructor/feedback-graph.html", {'rating_counts': rating_counts})





def edit_course(request, course_id):
    course_details = Addcourse.objects.get(pk=course_id)
    if request.method == 'POST':
        course_details.course_name = request.POST.get('courseName') if request.POST.get('courseName') else course_details.course_name
        course_details.course_image = request.FILES['courseImage'] if 'courseImage' in request.FILES else course_details.course_image
        course_details.course_category = request.POST.get('courseCategory') if request.POST.get('courseCategory') else course_details.course_category
        course_details.course_language = request.POST.get('courseLanguage') if request.POST.get('courseLanguage') else course_details.course_language
        course_details.course_description = request.POST.get('courseDescription') if request.POST.get('courseDescription') else course_details.course_description
        course_details.video_url = request.POST.get('videourl') if request.POST.get('videourl') else course_details.video_url
        course_details.duration_weeks = request.POST.get('courseDuration') if request.POST.get('courseDuration') else course_details.duration_weeks
        course_details.price = request.POST.get('coursePrice') if request.POST.get('coursePrice') else course_details.price
        course_details.save()
        messages.success(request,"Updated successfully !")
        return redirect('view_courses')
    return render(request, "instructor/edit-courses.html", {'course_details': course_details})




def remove_course(request, course_id):
    course = get_object_or_404(Addcourse, pk=course_id)
    course.delete()
    messages.error(request,"Deleted Successfully !")
    return redirect('view_courses')






def rating_view(request, rating, feedback_id):
    try:
        feedback = StudentFeedback.objects.get(pk=feedback_id)
        user = feedback.student
        if rating == 1 or rating == 2:
            subject = 'Improvement Feedback'
            message = 'Hello,\n\nThank you for your feedback. We have taken note of your suggestions and will work towards improving our services. Your input is valuable to us.'
        elif rating == 3:
            subject = 'Appreciation for Feedback'
            message = 'Hello,\n\nThank you for your feedback. We appreciate your suggestions and will strive to make improvements based on your input.'
        elif rating == 4 or rating == 5:
            subject = 'Appreciation for Feedback'
            message = 'Hello,\n\nThank you for your feedback. We are delighted to hear about your positive experience. Your satisfaction is our priority.'
        else:
            messages.error(request, 'Invalid rating provided.')
            return redirect('admin_view_feedbacks')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, 'Email sent successfully!')
    except StudentFeedback.DoesNotExist:
        messages.error(request, 'Feedback does not exist.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    return redirect('view_student_feedbacks')




def remove_feedback_ins(request, feedback_id):
    feedback = get_object_or_404(StudentFeedback, pk=feedback_id)
    feedback.delete()
    messages.info(request,"Feedback deleted Successfully ")
    return redirect('view_student_feedbacks') 

from django.shortcuts import render, redirect
from instructorapp.models import Job, JobApplication
from django.utils.timezone import now
def create_job(request):
    if request.method == "POST":
        Job.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            candidate_required_location=request.POST.get("candidate_required_location"),
            salary=request.POST.get("salary"),
            company_name=request.POST.get("company_name"),
            job_type=request.POST.get("job_type"),
            category=request.POST.get("category"),
            url=request.POST.get("url"),
            publication_date=now()
        )
        return redirect("create_job")
    return render(request, "instructor/add.html")

def view_jobs(request):
    applications = JobApplication.objects.all().select_related('job')
    return render(request, "instructor/viewjobs.html", {"applications": applications})
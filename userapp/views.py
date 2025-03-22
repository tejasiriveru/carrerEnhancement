from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re
import pandas as pd
from django.contrib import messages
import urllib.request
import urllib.parse
import random
from django.conf import settings
import os
from django.core.mail import send_mail
from django.utils.datastructures import MultiValueDictKeyError
from userapp.models import *
from instructorapp.models import *
from django.utils.datastructures import MultiValueDictKeyError
import random
import urllib.request
import urllib.parse
from onlinecourses.RazorPayApi import RazorpayClient
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
from random import sample

from django.utils.text import slugify
from django.utils import timezone

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

from django.shortcuts import render
from .models import Job

def job_listssss(request):
    jobs = Job.objects.all()
    return render(request, "user/all_jobs.html", {"jobs": jobs})

def generate_otp(length=4):
    otp = ''.join(random.choices('0123456789', k=length))
    return otp

import re
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Conversation
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_chatbot(request):
    conversations = Conversation.objects.all().order_by('created_at')
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            # Call Perplexity API
            headers = {
                "Authorization": f"Bearer {settings.PERPLEXITY_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "Be precise and concise."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers=headers
            )
            
            bot_response = "Error: Could not get response from AI"
            if response.status_code == 200:
                try:
                    bot_response = response.json()['choices'][0]['message']['content']
                    
                    # Remove markdown bold () and any references (e.g., [1], [2], etc.)
                    bot_response = re.sub(r'\\([^]+)\\*', r'\1', bot_response)  # Remove bold
                    bot_response = re.sub(r'\[\d+\]', '', bot_response)  # Remove reference numbers
                except:
                    pass
                
            Conversation.objects.create(
                user_message=user_message,
                bot_response=bot_response
            )
            
            return redirect('chatbot')
    
    return render(request, 'user/chatbot.html', {'conversations': conversations})


from django.shortcuts import render, redirect
from .models import Job
from django.contrib import messages

def apply_job(request):
    if request.method == "POST":
        job_id = request.POST.get("job_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        cover_letter = request.POST.get("cover_letter")
        resume = request.FILES.get("resume")

        # Store application data in session (simulating database storage)
        applied_jobs = request.session.get("applied_jobs", [])
        applied_jobs.append(job_id)
        request.session["applied_jobs"] = applied_jobs

        messages.success(request, "Your application has been submitted successfully!")
        return redirect("job_list")  # Redirect back to job listings

    return redirect("job_list")





def student_logout(request):
    logout(request)
    messages.info(request,"Logout Successfully ")
    return redirect('student_login')

# Create your views here.

def index(requrest):
    return render(requrest,"user/index.html")



def about(request):
    return render(request,"user/about.html")


def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            student = StudentRegModel.objects.get(email=email)   
            if student.password == password:
                if student.otp_status == 'Verified':
                    messages.success(request, 'Login successful!')
                    request.session['student_id_after_login'] = student.student_id
                    return redirect('student_dashboard')
                else:
                    otp = generate_otp()
                    student.otp = otp
                    student.save()
                    subject = 'OTP Verification for Account Activation'
                    otp = f'Your OTP for verification is: {student.otp}'
                    message = f'Hello {student.full_name},\n\nYou are attempting to log in to your query account. Your OTP for login verification is: {otp}\n\nIf you did not request this OTP, please ignore this email.'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [student.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    messages.success(request, 'Otp sent to mail and phone number !')
                    return redirect('otp')
            else:
                messages.error(request, 'Incorrect Password')
                return redirect('student_login')
        except StudentRegModel.DoesNotExist:
            messages.error(request, 'No User Found')
            return redirect('student_register')
    return render(request,"user/student-login.html")


def instructor_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('Password')
        try:
            ins = InstructorRegModel.objects.get(email=email)
            if ins.password == password:
                if ins.otp_status == 'Verified':
                    if ins.status == 'Accepted':
                        messages.success(request, 'Login successful!')
                        request.session['ins_id_after_login'] = ins.pk
                        return redirect('ins_dashboard')
                    else:
                        messages.error(request, 'Account not yet accepted')
                        return redirect('instructor_login')
                else:
                    otp = generate_otp()
                    ins.otp = otp
                    ins.save()
                    subject = 'OTP Verification for Account Activation'
                    otp_message = f'Your OTP for verification is: {ins.otp}'
                    message = f'Hello {ins.full_name},\n\nYou are attempting to log in to your account. {otp_message}\n\nIf you did not request this OTP, please ignore this message.'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [ins.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    messages.success(request, 'Otp sent to mail and phone number!')
                    return redirect('instructorotp')
            else:
                messages.error(request, 'Incorrect Password')
                return redirect('instructor_login')
        except InstructorRegModel.DoesNotExist:
            messages.error(request, 'No User Found')
            return redirect('instructor_register')
    return render(request, "user/instructor-login.html")




def student_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        try:
            StudentRegModel.objects.get(email=email)
            messages.info(request, 'Email Already Exists!')
            return redirect('student_register')
        except StudentRegModel.DoesNotExist:
            otp = generate_otp()
            user = StudentRegModel.objects.create(full_name=name, email=email, phone_number=phone, photo=profile, password=password, address=location, otp=otp)
            print(user)
            subject = 'OTP Verification for Account Activation'
            otp_message = f'Your OTP for verification is: {user.otp}'
            message = f'Hello {user.full_name},\n\nYou are attempting to Register an Account. {otp_message}\n\nIf you did not request this OTP, please ignore this message.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            request.session['student_id'] = user.student_id
            print(request.session['student_id'])
            messages.info(request, 'OTP Sent To Email and Phone!')
            return redirect('otp')
    return render(request, "user/student-register.html")


def instructor_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        location = request.POST.get('address')
        profile = request.FILES.get('profile')
        gender = request.POST.get('gender')
        try:
            InstructorRegModel.objects.get(email=email)
            messages.info(request, 'Email Already Exists!')
            return redirect('instructor_login')
        except InstructorRegModel.DoesNotExist:
            otp = generate_otp()
            ins = InstructorRegModel.objects.create(full_name=name, email=email, phone_number=phone, photo=profile, password=password, address=location, otp=otp)
            print(ins)
            subject = 'OTP Verification for Account Activation'
            otp_message = f'Your OTP for verification is: {ins.otp}'
            message = f'Hello {ins.full_name},\n\nYou are attempting to Register an Account. {otp_message}\n\nIf you did not request this OTP, please ignore this message.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ins.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            request.session['ins_id'] = ins.instructor_id
            messages.info(request, 'OTP Sent To Email and Phone!')
            return redirect('instructorotp')
    return render(request,"user/instructor-register.html")



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        if username == "admin"  and password == "admin":
            messages.success(request, 'Login Successfully.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request,"user/admin-login.html")



def contact(request):
    return render(request,"user/contact.html")




def ins_otp(request):
    ins_id = request.session.get('ins_id')
    if request.method == "POST":
        otp_entered = request.POST.get('ins_otp')
        if not otp_entered:
            messages.error(request, 'Please enter the OTP')
            print("OTP not entered")
            return redirect('instructorotp')
        try:
            instructor = InstructorRegModel.objects.get(pk=ins_id)
            if str(instructor.otp) == otp_entered:
                instructor.otp_status = 'Verified'
                instructor.save()
                # user_id = request.session['user_id']
                messages.success(request, 'OTP verification successful!')
                return redirect('instructor_login')
            else:
                messages.error(request, 'Invalid OTP entered')
                print("Invalid OTP entered")
                return redirect('instructorotp')
        except instructor.DoesNotExist:
            messages.error(request, 'Invalid Instructor')
            print("Invalid Instructor")
            return redirect('instructor_register')
    return render(request,"user/ins-otp.html")




def otp(request):
    student_id = request.session.get('student_id')
    student = StudentRegModel.objects.get(student_id=student_id)
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        print(otp_entered,"otp enterd")
        print(student)
        if not otp_entered:
            messages.error(request, 'Please enter the OTP')
            print("OTP not entered")
            return redirect('otp')
        try:
            student = StudentRegModel.objects.get(student_id=student_id)
            if str(student.otp) == otp_entered:
                student.otp_status = 'Verified'
                student.save()
                # user_id = request.session['user_id']
                messages.success(request, 'OTP verification successful!')
                return redirect('student_login')
            else:
                messages.error(request, 'Invalid OTP entered')
                print("Invalid OTP entered")
                return redirect('otp')
        except student.DoesNotExist:
            messages.error(request, 'Invalid Student')
            print("Invalid Student")
            return redirect('student_register')
    return render(request,"user/otp.html")



# student views after login

from django.shortcuts import render, redirect
from instructorapp.models import Job as jobbbssss   # Make sure Addcourse is imported
from instructorapp.models import JobApplication as aappplisjaj   # Make sure Addcourse is imported
from instructorapp.models import  Addcourse  # Make sure Addcourse is imported
from django.http import HttpResponseBadRequest
def student_dashboard(request):
    all_courses = Addcourse.objects.all()
    jobs = Job.objects.all().order_by('-publication_date')  # Corrected model name
    
    print(f"Number of jobs found: {jobs.count()}")
    for job in jobs:
        print(f"Job ID: {job.id} | Title: {job.title}")
        
    return render(request, "user/student-dashboard.html", {
        'all_courses': all_courses,
        'jobs': jobs
    })

def apply_job(request, job_id):
    if request.method == "POST":
        try:
            # Correct model name from aappplisjaj to Job
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return HttpResponseBadRequest("Invalid job ID")

        name = request.POST.get('name')
        email = request.POST.get('email')
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')

        if not all([name, email, cover_letter, resume]):
            return HttpResponseBadRequest("All fields are required")

        JobApplication.objects.create(
            job=job,
            name=name,
            email=email,
            cover_letter=cover_letter,
            resume=resume
        )
        return redirect('student_dashboard')
    return redirect('student_dashboard')


def student_courses(request):
    all_courses = Addcourse.objects.all()
    for course_name in all_courses:
        print(course_name.course_name)
    return render(request, "user/student-courses.html", {'all_courses': all_courses})


def purchase_course(request, course_id):
    course = Addcourse.objects.get(pk=course_id)
    request.session['course_id_in_purchase_page'] = course.course_id
    return render(request, 'user/purchasepage.html', {'course': course})


def test_result(request):
    student_id = request.session.get('student_id_after_login')
    if student_id is not None:
        student_tests = UserTestModel.objects.filter(test_user_id=student_id).order_by('-id')
        paginator = Paginator(student_tests, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "user/test-result.html", {'page_obj': page_obj})
    else:
        messages.error(request, "Student not logged in or session data missing")
        return redirect("student_login")




from django.db.models import Count, Exists, OuterRef
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

def my_courses(request):
    student_id = request.session.get('student_id_after_login')
    if student_id is None:
        messages.warning(request, "No student found, please login again!")
        return redirect('student_login')

    student_courses = StudentCourses.objects.filter(student_id=student_id)
    student_courses_with_question_count = student_courses.annotate(
        question_count=Count('course__question')  # Ensure 'course__question' is correct; check your Course model.
    ).annotate(
        has_attempted_test=Count('student__user_results')  # Use the correct related_name for the reverse relationship.
    )

    context = {
        'student_courses': student_courses_with_question_count
    }
    return render(request, "user/my-courses.html", context)


import os
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from django.http import HttpResponse
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib import messages
from .models import StudentRegModel, Addcourse, StudentCourses

def download_certificate(request, course_id):
    user_id = request.session.get('student_id_after_login')
    if not user_id:
        messages.error(request, "User not logged in.")
        return redirect('student_login')

    try:
        course = Addcourse.objects.get(pk=course_id)
        student_course = StudentCourses.objects.get(student_id=user_id, course=course)

        if student_course.certificate_downloaded:
            messages.warning(request, "You have already downloaded the certificate for this course.")
            return redirect('my_courses')

        # Update the certificate_downloaded status
        student_course.certificate_downloaded = True
        student_course.save()

        # Create the PDF certificate
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{course.course_name}_certificate.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Add a border
        border_width = 2
        border_color = colors.black
        elements.append(Table(
            [['']],
            style=TableStyle([
                ('BOX', (0, 0), (-1, -1), border_width, border_color),
                ('TOPPADDING', (0, 0), (-1, -1), 20),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
                ('LEFTPADDING', (0, 0), (-1, -1), 20),
                ('RIGHTPADDING', (0, 0), (-1, -1), 20),
            ]),
            colWidths=[7.5 * inch],
            rowHeights=[10 * inch]
        ))
        
        # Add certificate title
        title_style = styles['Title']
        title_style.fontSize = 24
        title_style.alignment = 1  # Center align
        elements.append(Paragraph("Certificate of Completion", title_style))
        elements.append(Spacer(1, 20))

        # Add student name
        student = StudentRegModel.objects.get(pk=user_id)
        student_name_style = styles['Heading2']
        student_name_style.fontSize = 20
        student_name_style.alignment = 1
        elements.append(Paragraph(f"This is to certify that", student_name_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>{student.full_name}</b>", student_name_style))
        elements.append(Spacer(1, 12))

        # Add course details
        course_details_style = styles['Normal']
        course_details_style.fontSize = 18
        course_details_style.alignment = 1
        elements.append(Paragraph(f"has successfully completed the course", course_details_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>{course.course_name}</b>", course_details_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Instructor: {course.instructor.full_name}", course_details_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {timezone.now().strftime('%Y-%m-%d')}", course_details_style))
        elements.append(Spacer(1, 36))

        # Add an optional image (e.g., a logo or seal)
        logo_path = os.path.join(settings.STATIC_ROOT, 'path/to/your/logo.png')
        if os.path.exists(logo_path):
            elements.append(Image(logo_path, width=2 * inch, height=2 * inch))
        else:
            messages.warning(request, "Logo not found. Skipping logo on certificate.")

        doc.build(elements)
        return response

    except Addcourse.DoesNotExist:
        messages.error(request, "Course not found.")
        return redirect('my_courses')
    except StudentCourses.DoesNotExist:
        messages.error(request, "You are not enrolled in this course.")
        return redirect('my_courses')





def test(request, course_id):
    course = Addcourse.objects.get(pk=course_id)
    questions = list(Question.objects.filter(course=course).order_by('?')[:10])
    if len(questions) < 10:
        additional_questions = list(Question.objects.filter(course=course).exclude(pk__in=[q.pk for q in questions]).order_by('?')[:10 - len(questions)])
        questions += additional_questions
    random.shuffle(questions)
    return render(request, "user/test.html", {'questions': questions, 'course_id': course_id})


def submit_test(request, course_id):
    if request.method == 'POST':
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                answers[question_id] = value

        try:
            course = Addcourse.objects.get(pk=course_id)
        except Addcourse.DoesNotExist:
            messages.error(request, "Course not found.")
            return redirect('test')

        user_id = request.session.get('student_id_after_login')
        if not user_id:
            messages.error(request, "User not logged in.")
            return redirect('student_login')

        course_name = course.course_name
        unique_identifier = slugify(course_name) 
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        test_name = f"Test for {course_name} ({unique_identifier}) - {timestamp}"

        user_test = UserTestModel.objects.create(
            test_user_id=user_id,
            test_name=test_name,
            test_marks=0
        )

        for question_id, answer in answers.items():
            try:
                question = Question.objects.get(pk=question_id)
            except Question.DoesNotExist:
                messages.error(request, "Question not found.")
                return redirect('test')

            marks = 1 if answer == question.correct_answer else 0
            ResultModel.objects.create(
                user_id=user_id,
                test_id=user_test.id,
                test_name=user_test.test_name,
                question=question.question_text,
                useranswer=answer,
                correctanswer=question.correct_answer,
                marks=marks
            )
            user_test.test_marks += marks

        user_test.save()
        messages.success(request, "Test submitted successfully.")
        return redirect('test_result')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('test')
    

def student_profile(request):
    student_id  = request.session['student_id_after_login']
    print(student_id)
    student = StudentRegModel.objects.get(student_id= student_id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        try:
            profile = request.FILES['profile']
            student.photo = profile
        except MultiValueDictKeyError:
            profile = student.photo
        password = request.POST.get('password')
        location = request.POST.get('location')
        student.full_name = name
        student.email = email
        student.phone_number = phone
        student.password = password
        student.address = location
        student.save()
        messages.success(request , 'updated succesfully!')
        return redirect('student_profile')
    return render(request,"user/student-profile.html",{'student':student})




def view_details(request, test_id):
    test_results = ResultModel.objects.filter(test_id=test_id)
    total_marks = UserTestModel.objects.get(pk=test_id)
    total_marks_final = total_marks.test_marks
    correct_Answers = total_marks_final
    wrong_Answers = 10 - int(correct_Answers)
    percantage = (correct_Answers/10*100)
    results_details = []
    for result in test_results:
        results_details.append({
            'test_name': result.test_name,
            'question': result.question,
            'user_answer': result.useranswer,
            'correct_answer': result.correctanswer,
            'marks': result.marks
        })
    return render(request, "user/view-fulltest-deatils.html", 
                  {'results_details': results_details,
                   "total_marks_final":total_marks_final,
                   "correct_Answers":correct_Answers,
                   "wrong_Answers":wrong_Answers,
                   "percantage":percantage,})






def student_feedback(request):
    if request.method == 'POST':
        selected_course_name = request.POST.get('course_name')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        rating = int(request.POST.get('rating'))
        additional_comments = request.POST.get('additional_comments')
        
        student_id = request.session.get('student_id_after_login')
        
        if selected_course_name and user_name and user_email and student_id is not None:
            StudentFeedback.objects.create(
                student_id=student_id,
                course_name=selected_course_name,
                user_name=user_name,
                user_email=user_email,
                rating=rating,
                additional_comments=additional_comments
            )
            messages.success(request, 'Feedback submitted successfully.')
            return redirect('student_feedback')
        else:
            messages.error(request, 'Incomplete data. Please fill in all required fields.')
    student_id = request.session.get('student_id_after_login')
    if student_id:
        student_courses = StudentCourses.objects.filter(student_id=student_id).values_list('course__course_name', flat=True)
        context = {'student_courses': student_courses}
        return render(request, "user/student-feedback.html", context)
    else:
        messages.error(request, 'You need to be logged in to access this page.')
        return redirect('login')








from django.db import IntegrityError



def user_payment(request, id):
    if request.method == "POST":
        student_id = request.session.get('student_id_after_login')
        if student_id is None:
            return HttpResponseBadRequest('Student ID not found in session')
        student = get_object_or_404(StudentRegModel, pk=student_id)
        course = get_object_or_404(Addcourse, pk=id)
        if StudentCourses.objects.filter(student=student, course=course).exists():
            messages.error(request, 'You are already enrolled in this course.')
            return redirect('my_courses')
        try:
            StudentCourses.objects.create(
                student=student,
                course=course,
                amount=course.price, 
                payment_status="Successful", 
                order_id="1" 
            )
            messages.success(request, 'Enrollment successful!')
        except Exception as e:
            messages.error(request, f'Error enrolling in course: {e}')
            return redirect('my_courses') 
        return redirect('my_courses') 
    else:
        return HttpResponseBadRequest("Invalid request method.")






@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        student_id = request.session.get('student_id_after_login')
        if student_id is None:
            return HttpResponseBadRequest('Student ID not found in session')

        print(student_id, "Student ID")
        try:
            user = StudentRegModel.objects.get(pk=student_id)
        except StudentRegModel.DoesNotExist:
            return HttpResponseBadRequest('Student not found')

        cart = get_object_or_404(CartModel, cart_user=user)
        fee = cart.cart_booking.price
        amount = fee * 100 
        try:
            cart = get_object_or_404(CartModel, cart_user=user)
            StudentCourses.objects.create(
                student=user,
                course=cart.cart_booking,
                amount=fee,
                payment_status="Successful",
                payment_id=1,
                order_id=1
            )
            messages.success(request, 'Payment successfully completed')
            return redirect('my_courses')
        except Exception as e:
            messages.error(request, 'Payment Failed: ' + str(e))
            return redirect('student_courses')






import nltk

from nltk import download
from nltk import pos_tag, sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import re
from nltk.stem import WordNetLemmatizer
        
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

wnl = WordNetLemmatizer()
df_jd=pd.read_csv('dataset/training.csv')
df_jd.dropna(subset=['job_description'], inplace=True)
df_jd['job_description'] = df_jd['job_description'].astype(str)

vectorizer1 = TfidfVectorizer(ngram_range=(1, 2))
job_Description = vectorizer1.fit_transform(df_jd['job_description'])




def preprocess_text(text, wnl):
    text = text.lower()
    text = re.sub('[^a-zA-Z]', ' ', text)
    sentences = sent_tokenize(text)
    features = []
    stop_words = set(stopwords.words("english"))
    for sent in sentences:
        if any(criteria in sent for criteria in ['skills', 'education']):
            words = word_tokenize(sent)
            words = [word for word in words if word not in stop_words]
            tagged_words = pos_tag(words)
            filtered_words = [word for word, tag in tagged_words if tag not in ['DT', 'IN', 'TO', 'PRP', 'WP']]
            features.append(" ".join(filtered_words))
    return " ".join(features)  

import fitz 
def calculate_resume_score(resume_path):
    try:
        with fitz.open(resume_path) as doc:
            resume_text = ""
            for page_number in range(doc.page_count):
                page = doc.load_page(page_number)
                resume_text += page.get_text()
        resume_score = len(resume_text.split())
        max_score = 1000
        scaled_score = (resume_score / max_score) * 100
        return scaled_score
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = "".join(page.extract_text() for page in reader.pages)
    return text


def job(request):
    top_job_descriptions = ""
    resume_score = ''
    matched_percentage = 0 
    if request.method == 'POST' and request.FILES.get('pdf-fileup'):
        uploaded_file = request.FILES['pdf-fileup']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        temp_file_path = fs.path(filename)  
        print(temp_file_path, "path is here")
        resume_score = calculate_resume_score(temp_file_path)
        # Example scenario where resume_score might be None
        resume_score = None

        # Check if resume_score is not None before rounding
        if resume_score is not None:
            resume_score = round(resume_score, 1)
        else:
            print("resume_score is None. Cannot round.")
        request.session['resumepath'] = temp_file_path
        dummy = extract_text_from_pdf(temp_file_path)
        text12 = preprocess_text(dummy, wnl)
        text13 = vectorizer1.transform([text12])
        RAM = cosine_similarity(text13, job_Description).flatten()
        
        max_similarity = max(RAM)
        matched_percentage = max_similarity * 100
        
        top_job_descriptions_df = df_jd.iloc[np.argsort(RAM)[-5:][::-1]]
        top_job_descriptions = top_job_descriptions_df.to_dict('records')
        print(top_job_descriptions,"hallooooooooooooo")
       
    return render(request, "user/job.html", {'top_job_descriptions': top_job_descriptions, 'resume_score': resume_score, 'matched_percentage': matched_percentage})


import pandas as pd
# views.py
import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import Job
from datetime import datetime, timedelta
from django.utils import timezone

def update_jobs(request):
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)
    if response.status_code == 200:
        jobs_data = response.json()['jobs']
        for job in jobs_data:
            Job.objects.update_or_create(
                url=job['url'],
                defaults={
                    'title': job['title'],
                    'company_name': job['company_name'],
                    'category': job['category'],
                    'job_type': job['job_type'],
                    'publication_date': datetime.strptime(job['publication_date'], "%Y-%m-%dT%H:%M:%S"),
                    'candidate_required_location': job['candidate_required_location'],
                    'salary': job.get('salary', ''),
                    'description': job['description']
                }
            )
        return HttpResponse("Jobs updated successfully")
    else:
        return HttpResponse("Failed to fetch jobs")

def job_list(request):
    jobs = Job.objects.filter(publication_date__gte=timezone.now() - timedelta(days=1)).order_by('-publication_date')
    return render(request, 'user/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'user/job_detail.html', {'job': job})


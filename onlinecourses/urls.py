"""
URL configuration for onlinecourses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.conf.urls.static import static
from django.conf import settings


from userapp import views as userviews
from instructorapp import views as insviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',userviews.index,name="index"),
    path('index/about/',userviews.about,name="about"),
    path('index/student-login/',userviews.student_login,name="student_login"),
    path('index/student-register/',userviews.student_register,name="student_register"),
    path('index/contact/',userviews.contact,name="contact"),
    path('index/otp/',userviews.otp,name="otp"),
    path('student/dashboard/',userviews.student_dashboard,name="student_dashboard"),
    path('student/courses/',userviews.student_courses,name="student_courses"),
    path('student/my-courses/',userviews.my_courses,name="my_courses"),
    path('student/test-result/',userviews.test_result,name="test_result"),
    path('student/test/<int:course_id>/',userviews.test,name="test"),
    path('student/test-deatils/<int:test_id>/',userviews.view_details,name="view_details"),
    path('student/profile/',userviews.student_profile,name="student_profile"),
    path('student/feedback/',userviews.student_feedback,name="student_feedback"),
    path('student/logout/',userviews.student_logout,name="student_logout"),
    path('student/razorpay/<int:course_id>/',userviews.purchase_course,name="purchase"),
    path('student/razorpay-paymet/<int:id>', userviews.user_payment, name="user_payment"),
    path('paymenthandler/', userviews.paymenthandler, name='paymenthandler'),
    path('submit-test/<int:course_id>/', userviews.submit_test, name='submit_test'),
    path('student/download_certificate/<int:course_id>/', userviews.download_certificate, name="download_certificate"),
    path('index/instructor-login/',userviews.instructor_login,name="instructor_login"),
    path('instructor/dashboard/',insviews.ins_dashboard,name="ins_dashboard"),
    path('instructor/add-courses/',insviews.add_courses,name="add_courses"),
    path('instructor/view-courses/',insviews.view_courses,name="view_courses"),
    path('instructor/add-question/',insviews.add_question,name="add_question"),
    path('instructor/all-question/',insviews.all_questions,name="all_questions"),
    path('instructor/view-students/',insviews.view_students,name="view_students"),
    path('instructor/view-students-feedbacks/',insviews.view_student_feedbacks,name="view_student_feedbacks"),
    path('instructor/view-students-feedbacks-graph/',insviews.feedbacks_graph,name="ins_feedbacks_graph"),
    path('instructor/logout/',insviews.ins_logout,name="ins_logout"),
    path('instructor/edit-courses/<int:course_id>/',insviews.edit_course,name="edit_course"),
    path('remove-course/<int:course_id>/', insviews.remove_course, name='remove_course'),
    path('remove-question/<int:question_id>/', insviews.remove_question, name='remove_question'),
    path('instructor-mail-reply/rating/<int:rating>/<int:feedback_id>/', insviews.rating_view, name='ins_rating_view'),
    path('remove-feedback/<int:feedback_id>/', insviews.remove_feedback_ins, name='remove_feedback_ins'),
    path('update-jobs/', userviews.update_jobs, name='update_jobs'),
    path('jobs/user/', userviews.job_list, name='job_list'),
    path('job/<int:job_id>/', userviews.job_detail, name='job_detail'),
    path("user/job/",userviews.job,name="job"),
    path("user/chatbot/",userviews.user_chatbot,name="chatbot"),
    path("create-job/", insviews.create_job, name="create_job"),
    path("jobs/", userviews.job_listssss, name="job_listss"),
    path("view-jobs/", insviews.view_jobs, name="view_jobs"),
    path('apply-job/<int:job_id>/', userviews.apply_job, name='apply_job'),
















]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

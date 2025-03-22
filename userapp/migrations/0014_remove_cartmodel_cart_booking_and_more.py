# Generated by Django 5.0.6 on 2025-03-19 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0013_conversation_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmodel',
            name='cart_booking',
        ),
        migrations.RemoveField(
            model_name='cartmodel',
            name='cart_user',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='ResultModel',
        ),
        migrations.RemoveField(
            model_name='studentcourses',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentcourses',
            name='student',
        ),
        migrations.RemoveField(
            model_name='studentfeedback',
            name='student',
        ),
        migrations.RemoveField(
            model_name='usertestmodel',
            name='test_user',
        ),
        migrations.DeleteModel(
            name='CartModel',
        ),
        migrations.DeleteModel(
            name='StudentCourses',
        ),
        migrations.DeleteModel(
            name='StudentFeedback',
        ),
        migrations.DeleteModel(
            name='StudentRegModel',
        ),
        migrations.DeleteModel(
            name='UserTestModel',
        ),
    ]

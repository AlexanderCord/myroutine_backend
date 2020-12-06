from django.core.management.base import BaseCommand, CommandError
from main.models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
import codecs
import sys

#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
#sys.stderr = codecs.getwriter('utf-8')(sys.stderr)

import os
from datetime import date
from myroutine.settings import *
class Command(BaseCommand):
    help = 'Sends notifications'

    def add_arguments(self, parser):
        parser.add_argument('--id')


    def handle(self, *args, **options):
    
        users = Notification.objects.select_related('user_id').filter(email = True).all()
        for user in users:
            user_email = user.user_id.email
            self.stdout.write("Current user #"+str(user.user_id.id)+": " +str(user_email))

                    
            tasks = Task.objects.select_related('category_id').select_related('schedule__task_id').filter(schedule__next_date = date.today(), user_id = user.user_id.id ).all().order_by('-id')

            if len(tasks) > 0:

                msg = "Hello!\n"
                msg += "Reminder from MyRoutine.\n"
                msg += "Here are the tasks for today you've scheduled:\n"
            
                for task in tasks:
                    self.stdout.write("Adding task id#" + str(task.id)+ ", user_id = "+str(task.user_id.id))
                    msg += "- [%s] %s" % (task.category_id.name, task.task) + "\n"
            
                msg += "View more: " + NOTIFICATION_APP_URL
                
                #self.stdout.write(str)
                result = send_mail(
                    'Review your tasks for today',
                    msg,
                    NOTIFICATION_EMAIL_FROM,
                    [user_email],
                    fail_silently=False,
                )
                if result:
                    self.stdout.write(self.style.SUCCESS("Notification has been sent to %s"%user_email))
                else: 
                    self.stdout.write(self.style.ERROR("Error has occured during sending Notification to %s"%user_email))
            else: 
                self.stdout.write("No tasks for today found for user %s" % user_email)
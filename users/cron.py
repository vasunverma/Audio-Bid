from datetime import datetime
from users.models import Job
from django.db.models.query_utils import Q

def dynamic_job_price():
    jobs = Job.objects.filter(Q(status= 0)).order_by("id")
    for job in jobs:
        if job.limit_price != 0 and job.price < job.limit_price:
            dayPassed = (datetime.utcnow().date() - job.created_date.date()).days
            if job.cron_date is None and dayPassed == 1:
                job.cron_date = datetime.now();
                job.price = job.price + 1
                job.save()
            else:
                dayPassed = (job.cron_date.date() - job.created_date.date()).days
                if dayPassed == 1:
                    job.cron_date = datetime.now();
                    job.price = job.price + 1
                    job.save()

            

            
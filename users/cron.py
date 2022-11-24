from users.models import Job

def dynamic_job_price():
    jobs = Job.objects.filter(Q(status= 0))
    for job in jobs:
        if job.limit_price != 0 and job.price < job.limit_price:
            job.price = job.price + 1
            job.save()

            
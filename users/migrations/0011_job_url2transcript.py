# Generated by Django 4.1.2 on 2022-11-13 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_job_name_alter_job_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='url2Transcript',
            field=models.TextField(null=True),
        ),
    ]
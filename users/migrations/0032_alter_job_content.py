# Generated by Django 4.1.3 on 2022-11-24 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0031_job_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='content',
            field=models.TextField(),
        ),
    ]
# Generated by Django 5.1.6 on 2025-05-20 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0003_alter_job_job_name_alter_job_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="job_description",
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="link",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

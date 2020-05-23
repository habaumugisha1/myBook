from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime


class School(models.Model):
    school_name = models.CharField(max_length=2500)
    school_location = models.CharField(max_length=2500)

    def __str__(self):
        return self.school_name


class Department(models.Model):
    school_id = models.ForeignKey(School, related_name='department', on_delete=models.CASCADE,default=False)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name


class Groups(models.Model):
    department_id = models.ForeignKey(Department, related_name='group', on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)
    group_email = models.CharField(max_length=250)

    def __str__(self):
        return self.group_name


class GroupProgress(models.Model):
    files_choices = (
        ("project_title", "Project Title"),
        ("project_proposal", "Project Proposal"),
        ("project_erd", "Project (ERD)"),
        ("time_management", "Time Management"),
        ("project_scope", "Project scope"),
        ("project_cost", "Project Cost"),
        ("project_backend", "Project Backend"),
        ("project_frontend", "Project Frontend"),
        ("project_test", "Project Test"),
        ("deployment", "Deployment"),
        ("project_book", "Project Book"),
    )
    group_id = models.ForeignKey(Groups, related_name='group_progress', on_delete=models.CASCADE)
    files_type = models.CharField(max_length=100, choices=files_choices, default='project_title')
    file_title = models.CharField(max_length=200)
    file_description = models.FileField(null=False, upload_to='project_file')
    status =models.CharField(max_length=120, default='Pending ...')
    progress=models.IntegerField(default=0)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.file_title


class Project(models.Model):
    group_id = models.ForeignKey(Groups, related_name='project', on_delete=models.CASCADE, null=True)
    project_title = models.CharField(max_length=500)
    project_description = models.TextField(max_length=10000)
    status=models.CharField(max_length=120, default='Pending ...')
    progress=models.IntegerField(default=0)
    topic = models.CharField(max_length=100, default='topics')

    def __str__(self):
        return self.project_title

    def get_absolute_url(self):
        return reverse('group-project-detail', kwargs={'pk': self.pk})


class FinalProject(models.Model):
    project_type = (
        ("data_science", "data_science"),
        ("project_proposal", "Project Proposal"),
        ("project_erd", "Project (ERD)"),
        ("time_management", "Time Management"),
    )
    project_type = models.CharField(max_length=100, choices=project_type, default='data_science')
    title = models.CharField(max_length=100)
    introduction = models.TextField(default=False)
    content = models.TextField()
    problem_statement = models.TextField(default=False)
    scope = models.TextField(default=False)
    source_code = models.CharField(max_length=100, default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


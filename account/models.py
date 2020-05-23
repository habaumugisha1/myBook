from django.db import models
from project.models import School, Department, Groups
from users.models import CustomerUser
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Coordinator(models.Model):
    user_name = models.ForeignKey(User, related_name='coordinator', on_delete=models.CASCADE, default=False)

    def __str__(self):
        return f'{self.user_name.first_name}:{self.user_name.last_name} Coordinator'


class Dean(models.Model):
    dean_name = models.ForeignKey(User, related_name='dean', on_delete=models.CASCADE, default=False)
    school_id = models.ForeignKey(School, related_name='dean', on_delete=models.CASCADE, default=False)

    def __str__(self):
        return f'{self.dean_name.first_name}:{self.dean_name.last_name} Dean'


class Supervisor(models.Model):
    supervisor_name = models.ForeignKey(User, related_name='supervisors', on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, default=False, related_name='supervisors', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.supervisor_name.first_name}:{self.supervisor_name.last_name}'


class Hod(models.Model):
    department_id = models.ForeignKey(Department, related_name='hod', on_delete=models.CASCADE)
    hod_name = models.ForeignKey(User, related_name='hod', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hod_name.first_name}:{self.hod_name.last_name} Hod'


class StudentGroup(models.Model):
    department_name = models.ForeignKey(Department, related_name='student_group', on_delete=models.CASCADE)
    student_name = models.ForeignKey(User, related_name='student_group', on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, related_name='student_group', on_delete=models.CASCADE)

    # def __int__(self):
    #     return self.group_id

    def get_absolute_url(self):
        return reverse('student-detail', kwargs={'pk': self.pk})


class FinalProjects(models.Model):
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
    keywords = models.CharField(max_length=300)
    technology = models.CharField(max_length=300)
    source_code = models.CharField(max_length=100, default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

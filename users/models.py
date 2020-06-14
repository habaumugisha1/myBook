from django.db import models
from django.contrib.auth.models import User
from project.models import School, Department


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class CustomerUser(models.Model):
    role_choices = (
        ("student", "student"),
        ("supervisor", "supervisor"),
        ("hod", "hod"),
        ("dean", "dean"),
        ("coordinator", "coordinator"),
    )
    username = models.ForeignKey(User, default=False, related_name='custom', on_delete=models.CASCADE, null=False)
    school = models.ForeignKey(School, related_name='custom', on_delete=models.CASCADE, null=False)
    department = models.ForeignKey(Department, related_name='custom', on_delete=models.CASCADE, null=True)
    role = models.CharField(max_length=20, choices=role_choices, default='student')

    def __str__(self):
        return f'{self.username.last_name}' f'{self.username.first_name}'

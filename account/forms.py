from django import forms
from .models import Supervisor, Hod


class AssignSupervisorToGroup(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['supervisor_name',  'group_id']


class AssignHodToDepartment(forms.ModelForm):
    class Meta:
        model = Hod
        fields = ['department_id',  'hod_name']
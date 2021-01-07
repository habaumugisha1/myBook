from account.models import StudentGroup, Dean, Hod, Supervisor
from project.models import School, Department, Groups, Project, GroupProgress, Annoucements
from users.models import CustomerUser
from .forms import AddGroupForm, AddGroupProgressForm, CreateDepartment, ApproveProject, CreateAnnoucements 
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView,DetailView


@login_required
def school(request):
    schools = School.objects.all()
    context = {
        'schools': schools
    }
    return render(request, 'coordinator/school.html', context=context)


@login_required
def departmentPage(request, pk=None):
    schools = get_object_or_404(School, pk=pk)
    departments = Department.objects.filter(school_id=pk)
    depart_count = departments.count()
    deans = Dean.objects.filter(school_id=pk)
    custom = CustomerUser.objects.filter(school=pk)
    hods = Hod.objects.all()

    context = {

        'schools': schools,
        'departments': departments,
        'deans': deans,
        'custom': custom,
        'hods': hods,
        'depart_count': depart_count,
    }

    return render(request, 'dean/department.html', context=context)


def groups(request, pk, *args, **kwargs):
    users = User.objects.get(pk=pk)
    custom = CustomerUser.objects.filter(username=users)
    supervisors = Supervisor.objects.filter(supervisor_name=users)
    for supervisor in supervisors:
        groups = Groups.objects.filter(id=supervisor.group_id.id)
    
    print(groups)
    context={
        'users':users,
        'custom':custom,
        'groups':groups, 
        'supervisors':supervisors

    }
    return render(request, 'supervisor/group.html', context=context)


@login_required
def department_details(request, pk):
    progres = 0
    group = 0
    p = 0
    project_progress = 0
    label = 0
    departments = Department.objects.get(pk=pk)
    groups = Groups.objects.filter(department_id=departments).order_by('id')
    supervisors = Supervisor.objects.filter(group_id__in=groups)
    for supervisor in supervisors:
        students = StudentGroup.objects.filter(group_id=supervisor.group_id)
    projects = Project.objects.filter(group_id__in=groups).order_by('id')
    customs = CustomerUser.objects.filter(department=departments).filter(role = 'student')
    superCustoms = CustomerUser.objects.filter(department=departments)
    # for group in groups:
    group_progress = GroupProgress.objects.filter(group_id=group)
        # print(group)

        # for progeress in group_progress:
        #     if(progeress.group_id == group):
        #         total = sum([progeress.progress])
        #         print(progeress.progress)
        #         print(total)
            
        # print(group_progress.progress)
    #(department_name=departments)

    # print(group_progress.progress)


    for pro in group_progress:
        group = pro.group_id
    
    for project in projects:
        if project.progress > 0:
            project_progress=project.progress
            label=project.topic

    for groupp in group_progress:
        progres = groupp.progress
        # print(progres)
    arr =[progres]
    # print(arr)

    for project in projects:
        if project.status=='approved':
            p=project
        #    project
            print(p)

    context = {
        'departments': departments,
        'projects': projects,
        'supervisors': supervisors,
        'groups': groups,
        'group':group,
        'customs': customs,
        'students': students,
        'superCustoms':superCustoms,
        'p':p,
        'project_progress':project_progress,
        'label':label,
        'group_progress':group_progress
        }
    return render(request, 'hod/department_detail.html', context=context )


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = StudentGroup


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = StudentGroup
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        # if self.request.user == post.author:
        #     return True
        return True


class GroupProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        # if self.request.user == post.author:
        #     return True
        return True


class GroupProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['group_id', 'project_title', 'project_description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GroupProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project


class GroupProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['project_title', 'project_description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        # if self.request.user == post.author:
        #     return True
        return True


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = StudentGroup
    fields = ['department_name', 'student_name', 'group_id']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = StudentGroup
    fields = ['department_name', 'student_name', 'group_id']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        # if self.request.user == post.author:
        #     return True
        return True


@login_required
def dean_department_detail(request, pk):
    departments = Department.objects.get(pk=pk)
    groups = Groups.objects.filter(department_id=departments).order_by('id')
    groups_numbers=groups.count()
    # supervisors = Supervisor.objects.filter(department__in=departments)
    projects = Project.objects.filter(group_id__in=groups).order_by('id')
    project_count=projects.count()
    customs = CustomerUser.objects.filter(department=departments)
    students = StudentGroup.objects.filter(department_name=departments)
     
    context = {
        'departments': departments,
        'groups_numbers':groups_numbers,
        'projects': projects,
        'project_count':project_count,
        # 'supervisors': supervisors,
        'groups': groups,
        'customs': customs,
        'students': students,
        }
    return render(request, 'dean/department_detail.html', context=context )


@login_required
def singleGroup(request, pk, *args, **kwargs):
    project_progress = 0
    label = 0
    groups = Groups.objects.get(pk=pk)
    projects = Project.objects.filter(group_id=groups)
    supervisors = Supervisor.objects.filter(group_id=groups)
    member = StudentGroup.objects.filter(group_id=groups)
    progress = GroupProgress.objects.filter(group_id=groups)

    for project in projects:
        if project.progress >0:
            label= project.topic
            project_progress=project.progress
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'groups': groups,
        'member': member,
        'progress': progress,
        'project_progress':project_progress,
        'label':label,
        }

    return render(request, 'group/group.html', context=context )

def approve_project(request, pk, *args, **kwargs): 
  
    # fetch the object related to passed id 
    appro = Project.objects.get(pk=pk)
    appro.status='approved'
    appro.progress=20
    appro.topic='Topic of project'
    appro.save(update_fields=["status", "progress", "topic"]) 
    
    context ={
        'appro':appro
    } 
    
  
    return render(request, "hod/approve_project.html", context) 

def reject_project(request, pk, *args, **kwargs):
    appro = Project.objects.get(pk=pk)
    appro.status='Project was rejected'
    appro.progress=0
    appro.save(update_fields=["status", "progress"]) 

    # if request.method == 'GET':
    #     print(appro.status)
    
    context ={
        'appro':appro
    } 
    
  
    return render(request, "hod/reject_project.html", context)

def approve_file(request, pk, *args, **kwargs): 
    group_file=GroupProgress.objects.get(pk=pk)
    group_file.status='approved'
    group_file.progress=25
    # if group_file.files_type == 'Project Proposal':
    #     group_file.progress=25
    #     print(group_file.progress)
    # elif group_file.files_type == 'Project (ERD)':
    #     group_file.progress=15
    # elif group_file.files_type == 'chapter I':
    #     group_file.progress=10
    # elif group_file.files_type == 'chapter II':
    #     group_file.progress=15
    # elif group_file.files_type == 'chapter III':
    #     group_file.progress=15
         
    data=group_file.progress
    lebels=group_file.files_type
    group_file.save(update_fields=["status", "progress"]) 
    # print(data)
    # print(group_file.files_type)
    
    context ={
        'group_file':group_file,
        'data':data,
        'lebels':lebels
    } 
    
  
    return render(request, "supervisor/approve_file.html", context) 

def reject_file(request, pk, *args, **kwargs):
    # appro = Project.objects.get(pk=pk)
    group_file=GroupProgress.objects.get(pk=pk)
    group_file.status='Rejected'
    group_file.progress=0
    data=group_file.progress
    lebels=group_file.files_type
    group_file.save(update_fields=["status", "progress"]) 
    
    context ={
        # 'appro':appro,
        'data':data,
        'lebels':lebels,
        'group_file':group_file
    } 

    return render(request, "supervisor/reject_file.html", context)


@login_required
def groupProgress(request):
    if request.method == 'POST':
        form = AddGroupProgressForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ' your account has been Updated!')
            return redirect('home')
    else:
        form = AddGroupProgressForm()

    context = {
        'form': form
    }
    return render(request, 'group/progress.html', context)


@login_required
def group_detail(request, pk, *args, **kwargs):
    label =0
    project_progress = 0
    labels = 0
    data = 0
    group = Groups.objects.get(pk=pk)
    custom = CustomerUser.objects.filter(username=request.user)
    group_progress=GroupProgress.objects.filter(group_id=group)
    students = StudentGroup.objects.filter(group_id=group)
    teachers = Supervisor.objects.filter(supervisor_name=request.user)
    projects = Project.objects.filter(group_id=group).order_by('id')
    for pt in group_progress:
        print(pt.file_description)
    for project in projects:
        if project.progress >0:
            label=project.topic
            project_progress= project.progress
            print(project_progress, label)

    for pro in group_progress:
        labels = pro.files_type
        data = pro.progress
        print(data)
    
    context = {
        'project_progress':project_progress,
        'label':label,
        'students': students,
        'custom': custom,
        'group':group,
        'group_progress':group_progress,
        'teachers': teachers,
        'projects': projects,
        'labels':labels,
        'data':data
    }
    return render(request, 'supervisor/group_detail.html', context=context)

def singleProject(request, pk, *args, **kwargs):
    project= Project.objects.get(pk=pk)
    context={
     'project':project
    }
    return render(request, 'dean/singleproject.html', context)


@login_required
def hodGroupDetail(request, pk):
    groups = Groups.objects.get(pk=pk)
    projects = Project.objects.filter(group_id=groups)
    supervisors = Supervisor.objects.filter(group_id=groups)
    students_group = StudentGroup.objects.filter(group_id=groups)
    customs = CustomerUser.objects.all()
    hods = Hod.objects.all()
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'groups': groups,
        'customs': customs,
        'hods': hods,
        'students_group': students_group,
        }
    return render(request, 'hod/hod_group.html', context=context )


@login_required
def create_group(request):
    form = AddGroupForm(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                group = form.save(commit=False)
                group.save()
                messages.success(request, 'group was created successfully')
        except Exception as e:
            form = AddGroupForm()
            messages.warning(request, 'Sorry, group not created, try again.Error : {}'.format(e))

    return render(request, 'hod/addgroup.html', {'form': form})


@login_required
def hodSupervisorDetail(request, pk):
    customs_user = CustomerUser.objects.get(pk=pk)
    groups = Groups.objects.all()

    students = StudentGroup.objects.all()
    supervisors = Supervisor.objects.all()

    context = {
            'groups': groups,
            'supervisors': supervisors,
            'students': students,
            'customs_user': customs_user,
            }
    return render(request, 'hod/supervisor.html', context=context)


@login_required
def create_department(request):
    form = CreateDepartment(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                group = form.save(commit=False)
                group.save()
                messages.success(request, 'Department was created successfully')
        except Exception as e:
            form = AddGroupForm()
            messages.warning(request, 'Sorry, Department not created, try again.Error : {}'.format(e))

    return render(request, 'hod/create_department.html', {'form': form})

def create_annoucements(request):
    form = CreateAnnoucements(request.POST)
    if request.method == 'POST':
    
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.save()
            messages.success(request, 'Announcement was created successfully')

    else:
        form = CreateAnnoucements()
    return render(request, 'project/announcement.html', {'form': form})

def single_annoucement(request, pk):
    announcement = Annoucements.objects.get(pk=pk)
    context={
        'announcement': announcement
    }
    return render(request, 'project/annoucement_details.html', context=context)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from project.models import FinalProject
from account.models import FinalProjects
from account.forms import AssignSupervisorToGroup, AssignHodToDepartment
from project.filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def project(request):
    pros = FinalProjects.objects.all()
    counter_pro = pros.count()
    filters = PostFilter(request.GET, queryset=pros)
    pros = filters.qs
    counter_filter = pros.count()
    context = {
        'pros': pros,
        'filters': filters,
        'counter_filter': counter_filter,
        'counter_pro': counter_pro,
    }
    paginate_by = 2
    return render(request, 'project/projects.html', context=context)


class PostListView(ListView):
    model = FinalProjects
    template_name = 'project/post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = FinalProjects
    template_name = 'project/finalprojects_list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return FinalProjects.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = FinalProjects


class PostCreateView(LoginRequiredMixin, CreateView):
    model = FinalProjects
    fields = ['project_type', 'title', 'content', 'introduction', 'problem_statement', 'scope',
              'keywords', 'technology', 'source_code', 'supervisor', 'school']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = FinalProjects
    fields = ['project_type', 'title', 'content', 'introduction', 'problem_statement', 'scope',
              'keywords', 'technology', 'source_code', 'supervisor', 'school']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FinalProjects
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def assign_supervisor_to_group(request):
    form = AssignSupervisorToGroup(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                group = form.save(commit=False)
                group.save()
                messages.success(request, 'Supervisor was assigned to group successfully')
        except Exception as e:
            form = AssignSupervisorToGroup()
            messages.warning(request, 'Sorry, Supervisor not assigned to group, try again.Error : {}'.format(e))

    return render(request, 'hod/assign_supervisor.html', {'form': form})


@login_required
def assign_hod_to_depart(request):
    form = AssignHodToDepartment(request.POST)
    if request.method == 'POST':
        try:
            if form.is_valid():
                group = form.save(commit=False)
                group.save()
                messages.success(request, 'Hod was assigned to Department successfully')
        except Exception as e:
            form = AssignHodToDepartment()
            messages.warning(request, 'Sorry, Hod not assigned to Department, try again.Error : {}'.format(e))

    return render(request, 'dean/assign_hod.html', {'form': form})
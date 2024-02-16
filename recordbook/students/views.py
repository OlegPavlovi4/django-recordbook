from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,DeleteView, DetailView, ListView, UpdateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import logout, login


from .filters import StudentFilter
from .forms import AddStudentForm, ChooseGroupForm, ChooseSubjectForm, FilterStudentForm, LoginUserForm, RegisterUserForm
from .models import Student
from .utils import DataMixin, menu



class StudentHome(DataMixin, ListView):
    model = Student
    template_name = 'students/index.html'
    context_object_name = 'students'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        queryset = self.get_queryset()
        st_filter = StudentFilter(self.request.GET, queryset)
        c_def = self.get_user_context(title='Главная страница', auth=auth, st_filter=st_filter)
        return {**context, **c_def}


    def get_queryset(self):
        queryset = super().get_queryset()
        st_filter = StudentFilter(self.request.GET, queryset)
        return st_filter.qs

    
    # def get_queryset(self):
    #     filters = {}
    #     first_name = self.request.GET.get('first_name')
    #     last_name = self.request.GET.get('last_name')
    #     group = self.request.GET.get('group')
    #     if first_name:
    #         filters['first_name__contains'] = first_name
    #     if last_name:
    #         filters['last_name__contains'] = last_name
    #     if group:
    #         filters['group'] = group
    #     new_context = Student.objects.filter(**filters)
    #     return new_context


class ShowStudent(DataMixin, DetailView):
    model = Student
    template_name = 'students/student.html'
    slug_url_kwarg = 'stud_slug'
    context_object_name = 'st'
    

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        c_def = self.get_user_context(auth=auth)
        return {**context, **c_def}


class AddStudent(LoginRequiredMixin, CreateView):
    form_class = AddStudentForm
    template_name = 'students/addstudent.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return {**context, **c_def}
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'students/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return {**context, **c_def}
    
    def get_success_url(self):
        return reverse_lazy('home')
    

class DeleteStudent(LoginRequiredMixin, DataMixin, DeleteView):
    model = Student
    template_name = 'students/delete_student.html'
    success_url = reverse_lazy('home')
    context_object_name = 'st'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Удалить студента")
        return {**context, **c_def} 


def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    return render(request, 'students/about.html', {'menu': menu, 'title': 'О сайте'})


def students(request):
    students = Student.objects.all()
    context = {
        'students': students,
        'menu': menu,
        'title': 'Студенты',
    }
    return render(request, 'students/students.html', context=context)


def teachers(request):
    return render(request, 'students/teachers.html', {'menu': menu, 'title': 'Преподаватели'})
    

class UpdateStudent(LoginRequiredMixin, DataMixin, UpdateView):
    model = Student
    form_class = AddStudentForm
    template_name = 'students/update_student.html'
    context_object_name = 'st'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Изменить студента")
        return {**context, **c_def} 


class Gradebook(DataMixin, ListView):
    template_name = 'students/gradebook.html'
    context_object_name = 'students'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        auth = self.request.user.is_authenticated
        group = self.request.GET.get('group')
        subject = self.request.GET.get('subject')
        dates = set()
        studs = []

        if group and subject:
            selected_students = Student.objects.filter(group=group)
            for st in selected_students:
                for sub in st.gradebook_set.filter(subject=subject):
                    dates.add(sub.date)
            dates = sorted(dates)

            for st in selected_students:
                marks =[''] * len(dates)
                for sub in st.gradebook_set.filter(subject=subject):
                    marks[dates.index(sub.date)] = sub.mark
                studs.append((f'{st.last_name} {st.first_name[0]}.{st.first_name[0]}.', marks))

        c_def = self.get_user_context(title='Журнал успеваемости',
                                      auth=auth,
                                      group_form=ChooseGroupForm(self.request.GET),
                                      subj_form=ChooseSubjectForm(self.request.GET, group=group),
                                      group=group,
                                      subject=subject,
                                      dates=dates, 
                                      studs=studs)
        return {**context, **c_def} 
    
    def get_queryset(self):
        group = self.request.GET.get('group')
        group = 0 if group == '' else group
        return Student.objects.filter(group=group)
        
    

# def index(request):
#     students = Student.objects.all()
#     context = {
#         'students': students,
#         'menu': menu,
#         'title': 'Главная страница',
#     }

# def show_student(request, stud_slug):
#     student = get_object_or_404(Student, slug=stud_slug)

#     context = {
#         'st': student,
#         'menu': menu,
#     }
#     return render(request, 'students/student.html', context=context)

# def addstudent(request):
#     if request.method == 'POST':
#         form = AddStudentForm(request.POST, request.FILES)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Ошибка!')
#     else:
#         form = AddStudentForm()
#     return render(request, 'students/addstudent.html', {'form': form})
#     return render(request, 'students/index.html', context=context)

# def login(request):
#     return HttpResponse('Авторизация')
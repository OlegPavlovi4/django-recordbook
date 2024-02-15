from django.urls import path

from students.views import AddStudent, DeleteStudent, LoginUser, RegisterUser, ShowStudent, StudentHome, UpdateStudent, about, logout_user, students, teachers # addstudent, index, show_student, login

urlpatterns = [
    path('about/', about,  name='about'),
    path('students/', students,  name='students'),
    path('teachers/', teachers,  name='teachers'),
    path('login/', LoginUser.as_view(),  name='login'),
    path('', StudentHome.as_view(), name='home'),
    path('student/<slug:stud_slug>/', ShowStudent.as_view(), name='student'),
    path('addstudent/', AddStudent.as_view(), name='addstudent'),
    path('register/', RegisterUser.as_view(),  name='register'),
    path('logout/', logout_user, name='logout'),
    path('student/<int:pk>/delete/', DeleteStudent.as_view(), name='delete_student'),
    path('student/<int:pk>/update/', UpdateStudent.as_view(), name='update_student'),
]

    # path('', index, name='home'),
    # path('login/', login,  name='login'),
    # path('student/<slug:stud_slug>/', show_student,  name='student'),
    # path('addstudent/', addstudent, name='addstudent'),

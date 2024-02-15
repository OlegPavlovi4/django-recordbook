from django.contrib import admin
from .models import Gradebook, Student, Group, Subject, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'created_at', 'is_study', 'photo')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name')
    list_editable = ('is_study',)
    list_filter = ('is_study', 'created_at')
    prepopulated_fields = {'slug': ('last_name',)}



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_display_links = ('name', 'course')
    search_fields = ('name', 'course')
    list_filter = ('name', 'course')



@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'created_at', 'photo')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name')
    prepopulated_fields = {'slug': ('last_name',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Gradebook)
class GradebookAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'student', 'date', 'mark')
    list_display_links = ('id', 'subject')
    search_fields = ('subject', 'student')
    list_filter = ('subject', 'student')

    def get_form(self, request, obj=None, **kwargs):
        form = super(GradebookAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['student'].queryset = \
            Student.objects.filter(group_id__in=obj.subject.groups.all())
        return form
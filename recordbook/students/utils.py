menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Студенты', 'url_name': 'students'},
    {'title': 'Преподаватели', 'url_name': 'teachers'},
    {'title': 'Журнал', 'url_name': 'gradebook'},
    ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
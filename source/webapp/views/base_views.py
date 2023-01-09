from django.db.models import Q
from django.utils.http import urlencode
from django.views.generic import ListView


class SearchView(ListView):
    search_form_class = None
    search_form_field = 'search'
    query_name = 'query'
    search_fields = [] # ['title__icontains', 'author__icontains']


    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        if self.search_form_class:
            return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form:
            if self.form.is_valid():
                return self.form.cleaned_data[self.search_form_field]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(self.get_query()) # filter(Q()) == all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.form:
            context['form'] = self.form
            if self.search_value:
                context[self.query_name] = urlencode({self.search_form_field: self.search_value})
                context[self.search_form_field] = self.search_value
        return context

    def get_query(self):
        query = Q()
        for field in self.search_fields:
            kwargs = {field: self.search_value} # {'title__icontains': 'task 1' }
            query = query | Q(**kwargs) # Q(title__icontains='task 1')
        return query
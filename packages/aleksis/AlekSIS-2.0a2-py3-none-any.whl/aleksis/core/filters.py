from django_filters import CharFilter, FilterSet
from material import Layout, Row


class GroupFilter(FilterSet):
    name = CharFilter(lookup_expr="icontains")
    short_name = CharFilter(lookup_expr="icontains")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.layout = Layout(Row("name", "short_name"))

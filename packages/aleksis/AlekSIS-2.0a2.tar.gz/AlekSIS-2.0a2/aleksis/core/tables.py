import django_tables2 as tables
from django_tables2.utils import A


class PersonsTable(tables.Table):
    """Table to list persons."""

    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover table-responsive-xl"}

    first_name = tables.LinkColumn("person_by_id", args=[A("id")])
    last_name = tables.LinkColumn("person_by_id", args=[A("id")])


class GroupsTable(tables.Table):
    """Table to list groups."""

    class Meta:
        attrs = {"class": "table table-striped table-bordered table-hover table-responsive-xl"}

    name = tables.LinkColumn("group_by_id", args=[A("id")])
    short_name = tables.LinkColumn("group_by_id", args=[A("id")])

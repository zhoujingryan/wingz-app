from django_filters.rest_framework import FilterSet


class BaseFilterSet(FilterSet):

    @classmethod
    def filter_for_field(cls, field, field_name, lookup_expr):
        filter_class = super().filter_for_field(field, field_name, lookup_expr)
        labels = getattr(cls.Meta, "field_labels", {})
        filter_name = cls.get_filter_name(field_name, lookup_expr)
        if filter_name in labels:
            filter_class._label = labels[filter_name]
        return filter_class

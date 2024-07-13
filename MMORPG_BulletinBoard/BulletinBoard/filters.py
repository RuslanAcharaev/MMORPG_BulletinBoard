from django_filters import FilterSet, ModelChoiceFilter
from .models import Ad, Response


class AdFilter(FilterSet):
    class Meta:
        model = Ad
        fields = {
            'adCategory': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['adCategory'].label = 'Категория'


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'status': ['exact'],
        }

    responseAd = ModelChoiceFilter(
        field_name='responseAd__title',
        queryset=Ad.objects.all(),
        label='Объявление'
    )

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['responseAd'].queryset = Ad.objects.filter(author_id=kwargs['request'])
        self.filters['status'].label = 'Статус отклика'


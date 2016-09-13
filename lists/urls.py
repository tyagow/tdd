from django.conf.urls import url
from lists.views import NewListView, ViewAndAddToList

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', ViewAndAddToList.as_view(), name='view_list'),
    url(r'^new$', NewListView.as_view(), name='new_list'),
]

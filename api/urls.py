from django.urls import path
from .views import addPerson, fetchNodes, getAll
urlpatterns = [
    path('addPerson/',addPerson.as_view(),name='add-person'),
    path('updatePerson/<int:id>',addPerson.as_view(),name='update-person'),
    path('getPerson/<int:id>',addPerson.as_view(),name='get-person'),
    path('deletePerson/<int:id>',addPerson.as_view(),name='delete-person'),
    path('fetchNode/',fetchNodes.as_view(),name='fetch-person'),
    path('getAll/',getAll.as_view(),name='get-all'),
]
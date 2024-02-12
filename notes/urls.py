from django.urls import path
from notes.views import ListNotes, RetrieveDeleteNote
urlpatterns = [
    path('list/', view=ListNotes.as_view(), name='notes_list'),
    path('list/<int:pk>', view=RetrieveDeleteNote.as_view(), name='notes_detail'),
]

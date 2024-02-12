from django.contrib import admin
from notes.models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'created', 'modified']


admin.site.register(Note, NoteAdmin)

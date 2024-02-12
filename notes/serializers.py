from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'author', 'title',
                  'description', 'created', 'modified']
        read_only_fields = ['id', 'author', 'created', 'modified']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'author': instance.author.email,
            'title': instance.title,
            'description': instance.description,
            'created': instance.created.date()
        }

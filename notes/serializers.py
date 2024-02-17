from rest_framework import serializers
from notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializador de Notas. Define de forma automatica los campos listados en fields.
    Por ejemplo id = serializers.IntegerField(), title = serializers.CharField(), etc..
    """
    class Meta:
        model = Note
        fields = ['id', 'author', 'title',
                  'description', 'created', 'modified']
        read_only_fields = ['id', 'author', 'created', 'modified']

    def to_representation(self, instance):
        """
        Forma en que se LISTAN los objetos.
        """
        return {
            'id': instance.id,
            'author': instance.author.email,
            'title': instance.title,
            'description': instance.description,
            'created': instance.created.date()
        }

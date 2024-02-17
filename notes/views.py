from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from notes.serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated


class ListNotes(ListCreateAPIView):
    """
    Vista de listado y creacion de notas.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = NoteSerializer

    def get_queryset(self):
        """
        Objetos que maneja la clase. Filtra notas del autor (usuario logeado).
        En caso de pasar parametros en la url los toma y filtra las notas cuyo titulo que contienen el parametro.
        """
        queryset = self.serializer_class.Meta.model.objects.filter(
            author=self.request.user)
        q = self.request.query_params.get('q')
        if (q is not None):
            # Si hay parametros en la url y titulos que lo contienen retorna esas notas, sino retorna todas las notas.
            return queryset.filter(title__icontains=q) if len(queryset.filter(title__icontains=q)) > 0 else queryset
        return queryset

    def list(self, request):
        """
        Forma en que se listan las notas.
        """
        notes = self.get_queryset()
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """
        Forma en que se crean las notas.
        """
        serializer.save(author=self.request.user)


class RetrieveDeleteNote(RetrieveUpdateDestroyAPIView):
    """
    Vista de detalle y eliminacion. Requiere autenticacion.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = NoteSerializer

    def get_queryset(self):
        """
        Objetos que maneja la clase. Filtra notas en base al autor (el usuario que esta logeado)
        """
        return self.serializer_class.Meta.model.objects.filter(author=self.request.user)

    def destroy(self, request):
        note = self.get_object()
        self.perform_destroy(instance=note)
        return Response({'Mensaje': 'Nota eliminada correctamente'}, status=status.HTTP_200_OK)

from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from notes.serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated


class ListNotes(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = NoteSerializer

    def get_queryset(self):
        print('EN GET_QUERYSET')
        print(self.request)
        print(self.request.user)
        print(self.request.auth)
        print(self.request.query_params)
        queryset = self.serializer_class.Meta.model.objects.filter(
            author=self.request.user)
        q = self.request.query_params.get('q')
        if (q is not None):
            print('q = ', q)
            return queryset.filter(title__icontains=q) if len(queryset.filter(title__icontains=q)) > 0 else queryset
        print('q = ', q)
        return queryset

    def list(self, request):
        notes = self.get_queryset()
        print(notes)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        print('EN PERFORM_CREATE')
        print(self.request.user, self.request.auth)
        print(serializer)
        serializer.save(author=self.request.user)


class RetrieveDeleteNote(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        print('EN DESTROY DE RETRIEVEDELETENOTE')
        print(request)
        print(*args)
        print(self.get_object())
        note = self.get_object()
        self.perform_destroy(instance=note)
        return Response({'Mensaje': 'Nota eliminada correctamente'}, status=status.HTTP_200_OK)

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404


from .serializers import TaskSerializer
from .models import task

@api_view(['GET', 'POST'])
def manageTasks(request, pk=None):
    if request.method == 'GET':
        if pk:
            task_instance = get_object_or_404(task, id=pk)
            serializer = TaskSerializer(task_instance)
            return Response(serializer.data)
        else:
            tasks = task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def manageTask(request, pk):
    task_instance = get_object_or_404(task, id=pk)

    if request.method == 'PUT':
        serializer = TaskSerializer(instance=task_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        task_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

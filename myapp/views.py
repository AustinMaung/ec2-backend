# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TodoItem
from .serializers import TodoItemSerializer

def get_todo_items(req):
	entries = TodoItem.objects.all()
	data = {
		'entries': list(entries.values())  # Convert queryset to list of dictionaries
	}
	return JsonResponse(data)

@api_view(['POST'])
def create_todo_item(req):
	serializer = TodoItemSerializer(data=req.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_completed(req):
	todo_item = TodoItem.objects.get(title=req.data.get('title'))

	serializer = TodoItemSerializer(todo_item, data=req.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

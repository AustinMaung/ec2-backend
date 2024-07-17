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
		'entries': list(entries.values()) 
	}
	return JsonResponse(data)

@api_view(['POST'])
def create_todo_item(req):
	# Check if a TodoItem with the same title already exists
	title = req.data.get('title')
	if TodoItem.objects.filter(title=title).exists():
		return Response(
			{"error": "Todo item with this title already exists."},
			status=status.HTTP_400_BAD_REQUEST
		)

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

@api_view(['POST'])
def delete_item(req):
	try:
		todo_item = TodoItem.objects.get(title=req.data.get('title'))
	except TodoItem.DoesNotExist:
		return Response({'error': 'TodoItem not found.'}, status=status.HTTP_404_NOT_FOUND)

	todo_item.delete()
	return Response({'message': 'TodoItem deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def update_title(req):
	prev_title = req.data.get('prev_title')
	new_title = req.data.get('new_title')

	# Check if a TodoItem with the same title already exists
	if TodoItem.objects.filter(title=new_title).exists():
		return Response(
			{"error": "Todo item with this title already exists."},
			status=status.HTTP_400_BAD_REQUEST
		)

	try:
		todo_item = TodoItem.objects.get(title=prev_title)
	except TodoItem.DoesNotExist:
		return Response({'error': 'TodoItem not found.'}, status=status.HTTP_404_NOT_FOUND)

	todo_item.title = new_title
	todo_item.save()

	return Response({'message': 'TodoItem title updated successfully.'}, status=status.HTTP_200_OK)


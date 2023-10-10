from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,ToDoSerializer
from rest_framework.response import Response
from .models import User,ToDo
from rest_framework.exceptions import AuthenticationFailed
# Create your views here.
import jwt,datetime
# from datetime import datetime  # Import datetime module
from .dt import get_current_time_formatted



class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'details':serializer.data,'message': 'Signed in successfully'})

class LoginView(APIView):
    def post(self,request):
        password=request.data['password']
        username=request.data['username']
        user=User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()

        }
        token=jwt.encode(payload, 'secret',algorithm='HS256')

        response=Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token
        }
        # print(datetime.datetime.utcnow)
        return response


class UserView(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user=User.objects.filter(id=payload['id']).first()
        serializer=UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'loggedout successfully'
        }
        return response


# Add task using current login user
class AddView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        user_id = serializer.data['id']
        # ////////////////////////////////////////
        # Extract task data from request
        title = request.data.get('title')
        desc = request.data.get('desc')
        time=request.data.get('time')

        # Check if title and desc are provided
        if not title or not desc:
            return Response({'message': 'Title and description are required.'}, status=400)

        # Assuming you have a Task model, create and save a task
        task = ToDo(user=user, title=title, description=desc, time=time)
        task.save()

        # Create a response indicating success
        response = Response({
            'message': 'Task added successfully',
            'title': title,
            'desc': desc,
            'time':time
        })

        return response



class ListView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        user_id = serializer.data['id']
        # print(user)

        # Define current_time and use it for filtering
        current_time = get_current_time_formatted()
        print(current_time)
        
        

        # Filter ToDo objects based on user_id and time
        all_tasks = ToDo.objects.filter(user=user)
        expired_tasks = all_tasks.filter(time__lt=current_time,completed=False)
        pending_tasks = all_tasks.filter(time__gte=current_time, completed=False)
        completed_tasks = all_tasks.filter(completed=True)
        
        # print("all_tasks", all_tasks)
        # print("pending_tasks",pending_tasks) 
        # print("completed_tasks",completed_tasks)
        # print("expired_tasks",expired_tasks)
        # Serialize the filtered tasks
        all_tasks_serializer = ToDoSerializer(all_tasks, many=True)
        expired_tasks_serializer = ToDoSerializer(expired_tasks, many=True)
        pending_tasks_serializer = ToDoSerializer(pending_tasks, many=True)
        completed_tasks_serializer = ToDoSerializer(completed_tasks, many=True)

        # print(all_tasks_serializer.data)
        response = Response({
            
            "pending_tasks": pending_tasks_serializer.data,
            "expired_tasks": expired_tasks_serializer.data,
            "completed_tasks": completed_tasks_serializer.data,
        })
        return response


class UpdateView(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        user_id = serializer.data['id']
        # ////////////////////////////////////////
        # Extract task data from request
        title = request.data.get('title')
        desc = request.data.get('description')
        time=request.data.get('time')
        completed=request.data.get('completed')
        task_id=request.data.get('task_id')
        # Check if title and desc are provided
        if not title or not desc:
            return Response({'message': 'Title and description are required.'}, status=400)

        # Assuming you have a Task model, create and save a task
        task = ToDo(id=task_id,user=user, title=title, description=desc, time=time,completed=completed)
        task.save()

        # Create a response indicating success
        response = Response({
            'message': 'Task updated successfully',
            'title': title,
            'desc': desc,
            'time':time,
            'completed':completed
        })

        return response

class DeleteView(APIView):
    def delete(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        user_id = serializer.data['id']
        # ////////////////////////////////////////
        # Extract task data from request
        task_id=request.data.get('task_id')
        # Check if title and desc are provided
        if not task_id:
            return Response({'message': 'Task id is required.'}, status=400)

        # Assuming you have a Task model, create and save a task
        task = ToDo.objects.filter(id=task_id)
        task.delete()

        # Create a response indicating success
        response = Response({
            'message': 'Task deleted successfully',
            'task_id': task_id,
        })

        return response

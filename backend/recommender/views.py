import datetime
import jwt
from rest_framework.permissions import BasePermission
from jobRecommender import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework import filters
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.response import Response
from .serializers import UserSerializer 
from rest_framework import status, generics
from rest_framework import permissions 
from .serializers import SkillSerializer, TalentProfileSerializer
from .serializers import UserSerializer, JobSerializer
from .models import Skill, TalentProfile, CustomeUser, Job 
from .preprocessor import Preprocessor, similarity
from PyPDF2 import PdfReader
from rest_framework.pagination import PageNumberPagination
import numpy as np 

        
def respond(response):    
    data = {"id":response['id'],
            'username':response['username'],
            'email':response['email'],
            'organization':response.get('organization', ''),
            'hiringManagerName':response.get('hiringManagerName', ''),
            'specialization':response.get('specialization', ''),
            'resume':response.get('resume', ''),
            'role':response.get('role', ''),
            'about':response.get('about', '')
            }
    return data
class IsOwnerOrReadOnly(BasePermission):
    '''
    Custom class to only allow owner of the object edit it.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True 
        return obj.user == request.user 
     
class UserList(APIView, PageNumberPagination):
    def post(self, request, format = None):
        try:
            request.data._mutable = True 
            request.data['is_active'] = True
            request.data._mutable = False      
        except:
            try:
                request.data["is_active"] = True
            except:
                return Response({"message":"Invalid data", "statusCode":403})
             
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(respond(data))
        return Response({"error":serializer.errors, "statusCode":status.HTTP_400_BAD_REQUEST})
    
    def get(self, request, format = None):
        users = CustomeUser.objects.all()[:100]
        users = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(users, many = True)
        data = map(respond, serializer.data)
        return self.get_paginated_response(data)
    
class UserDetail(APIView):
    permission_classes = (permissions.IsAuthenticated
                          ,IsOwnerOrReadOnly)
    queryset = CustomeUser.objects.all()
    serializer_class = UserSerializer 
    lookup_field = 'id'
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
       
class JobList(APIView, PageNumberPagination):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format = None):
        queryset = Job.objects.all()[:100]
        queryset = self.paginate_queryset(queryset, request, view=self)
        serializer = JobSerializer(queryset, many = True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format = None):
        JWT_authenticator = JWTAuthentication()
        data, token = JWT_authenticator.authenticate(request)  
        description = request.data['description']
        preprocessor = Preprocessor(description = description)
        request.data['jobCategory'] = preprocessor.category
        request.data['user'] = token.payload.get('user_id', '')
        serializer = JobSerializer(data  = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error":serializer.errors, "statusCode":status.HTTP_400_BAD_REQUEST})

    
class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated
                          ,IsOwnerOrReadOnly)
    queryset = Job.objects.all()
    serializer_class = JobSerializer 
    lookup_field = 'jobId'
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
       
        
        
class RecommenderView(APIView, PageNumberPagination):
    permission_classes = (permissions.IsAuthenticated,)
    def get_object(self, pk):
        try:
            user = CustomeUser.objects.get(pk = pk)
            return user 
        except CustomeUser.DoesNotExist:
            raise ValueError
    def get(self, request, pk, format = None):
        try:
            user = self.get_object(pk)
            resume = user.resume
            reader = PdfReader(resume)
            resume_text = ''
            for page in reader.pages:
                resume_text += page.extract_text()
            preprocessor = Preprocessor(resume_text)
            recommended = Job.objects.filter(jobCategory = preprocessor.category)
            recommended = self.paginate_queryset(recommended, request, view = self)
            serializer = JobSerializer(recommended, many = True)
            hashmap = {index:data for index, data in enumerate(serializer.data)}
            similarity_probability = []
            ordered_list = []
            for index in range(len(hashmap)):
                similarity_probability.append(similarity(resume_text, hashmap[index]["description"]))
            sorted_indeces = np.argsort(similarity_probability)
            for index in sorted_indeces:
                ordered_list.append(hashmap[index])
            if not ordered_list:
                jobs = Job.objects.annotate(Count('id'))[:10]
                serializer = JobSerializer(jobs, many = True)
                return Response(serializer.data)
            return self.get_paginated_response(ordered_list)
        except:
            return Response({"error":"Something went wrong!", "statusCode":status.HTTP_400_BAD_REQUEST})
        
class ProfileView(APIView, PageNumberPagination):
    permission_classes = (permissions.IsAuthenticated, )
    def put(self, request, userId, format = None):
        try:
            user = TalentProfile.objects.get(pk = userId)
            serializer = TalentProfileSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except:
            serializer = TalentProfileSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"error":serializer.errors, "statusCode":status.HTTP_400_BAD_REQUEST})
        
    def delete(self, request, pk, format = None):
        try:
            user = TalentProfile.objects.get(pk = pk)
            user.delete()
            return self.get_paginated_response(
                {"error":"No content", 
                                                
                "statusCode":status.HTTP_204_NO_CONTENT})
        except:
            return self.get_paginated_response({
                "error":"Bad request",                                    
             "statusCode":status.HTTP_400_BAD_REQUEST})
        
        
    def get(self, request, pk, format = None):
        try:
            user = TalentProfile.objects.get(pk = pk)
            serializer = TalentProfileSerializer(user)
            return self.get_paginated_response(serializer.data)
        except:
            return self.get_paginated_response(
                {"error":ValueError, 
                 "statusCode":status.HTTP_403_FORBIDDEN})
class SkillView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = SkillSerializer
    queryset = Skill.objects.all()
class Search(generics.ListAPIView, PageNumberPagination):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['description', 
                     'qualification', 
                     'responsibility', 
                     'jobTitle', 
                     'jobCategory']  
class LoginView(APIView):
    def generate_token(self, email, userId):
        exp_time = datetime.utcnow() + datetime.timedelta(days=1)
        payload = {
            'userId':userId,
            'email':email
        }
        token = jwt.encode(payload, key = settings.SECRET_KEY, algorithm='HS256')
        return token  

    def post(self, request):
        email = request.email
        password = request.password
        user = authenticate(email = email, password = password)
        token = self.generate_token(user.userId, user.email)
        if user:
            return Response({"access":token, "statusCode":200}) 
        return Response({"message":"User not found", "statusCode":404})
    
        
        
    
# from rest_framework.views import APIView
# from .models import Job, Recommended, User
# from .serializers import RecommendedSerializer
# from rest_framework import status 
# from rest_framework.response import Response
# class RecommenderView(APIView):
#     def get(self, request, pk = None, format = None):
#         queryset = Recommended.objects.all()   
#         serializer = RecommendedSerializer(queryset, many = True)
#         return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
#     def post(self, request, format = None):
#         serializer = RecommendedSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
# class RecommenderForUserView(APIView):
#     def get_object(self, pk):
#         try:
#             queryset = Recommended.objects.get(pk  = pk)
#         except Recommended.DoesNotExist:
#             raise ValueError
#         return queryset
    
#     def get(self, request, pk, format = None):
#         queryset = self.get_object(pk)
#         serializer = RecommendedSerializer(queryset)
#         return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
    
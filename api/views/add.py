from api.models import *
from rest_framework .views import APIView
from rest_framework import status
from rest_framework.response import Response
from api.serializer import *


class addPerson(APIView):
    #create a new person record
    def post(self,request):
        required_fields = ['name','role']
        missing_field = [field for field in required_fields if not request.data.get(field)]
        if missing_field:
            raise ValueError(f'missing required fields: {missing_field}')
        serializer = addPersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'person added successfully','status':status.HTTP_201_CREATED})
        return Response({'error':f'Error! {serializer.errors}','status':status.HTTP_400_BAD_REQUEST})

    #update person record with respect to primary key
    def put(self, request, id):
        if id is None:
            return Response({'error':'missing required field ID','status':status.HTTP_403_FORBIDDEN})
        try:
            person = People.objects.get(id = id)
            serializer = addPersonSerializer(person,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'person updated successfully','status':status.HTTP_200_OK})
            return Response({'error':f'Error! {serializer.errors}','status':status.HTTP_400_BAD_REQUEST})
        except People.DoesNotExist as e:
            error = str(e)
            return Response({'error':f'Error! {error}','status':status.HTTP_404_NOT_FOUND})
    
    #read indivisual person's record
    def get(self, request, id=None):
        if id is None:
            return Response({'error':'missing required field ID','status':status.HTTP_403_FORBIDDEN})
        try:
            person = People.objects.get(id = id,archive=0)
            serializer = addPersonSerializer(person)
            return Response({'data':serializer.data,'status':status.HTTP_200_OK})
        except People.DoesNotExist as e:
            error = str(e)
            return Response({'error':f'Error! {error}','status':status.HTTP_404_NOT_FOUND})
        
    #delete/archive indivisual person record
    def delete(self,request,id):    
        if id is None:
            return Response({'error':'missing required field ID','status':status.HTTP_403_FORBIDDEN})
        try:
            person = People.objects.get(id = id,archive=False)
            person.archive = True
            person.save()
            return Response({'message':'person data archived successfully','status':status.HTTP_200_OK})
        except People.DoesNotExist as e:
            error = str(e)
            return Response({'error':f'Error! {error}','status':status.HTTP_404_NOT_FOUND})
        
# class fetchNodes(APIView):
#     def get(self,request):
#         people = People.objects.filter(is_parent=True) #to fetch on parent nodes 
#         serializer = readPersonSerializer(people,many=True)   
#         result = set()
#         for each in serializer.data:
#             child = People.objects.filter(parent = each['id'])
#             child_serializer = readPersonSerializer(child, many=True)
#             each['children'] = child_serializer.data
#         return Response({'data':serializer.data,'status':status.HTTP_200_OK})

class fetchNodes(APIView):
    def get(self, request):
        try:
            people = People.objects.filter(parent__isnull=True,archive=0)  
            data = self.find_children(people)  
            return Response({'data': data, 'status': status.HTTP_200_OK})
        except People.DoesNotExist as e:
            return Response({'error':f'Erro! {str(e)}','status':status.HTTP_400_BAD_REQUEST})

    def find_children(self, people):
        result = []
        for person in people:
            person_data = addPersonSerializer(person).data  
            children = People.objects.filter(parent=person.id,archive=0) #storing children who has parent_id of a person
            if children.exists():
                #calling the same function again to if the children we found has a children or not
                person_data['children'] = self.find_children(children)  
            else:
                person_data['children'] = []  # No children, empty list
            result.append(person_data)
        return result

class getAll(APIView):
    def get(self,request):
        try:
            people = People.objects.filter(archive=0)
            serializer = readPersonSerializer(people,many=True)
            return Response({'data':serializer.data,'status':status.HTTP_200_OK})
        except People.DoesNotExist as e:
            error = str(e)
            return Response({'error':f'Error! {error}','status':status.HTTP_400_BAD_REQUEST})


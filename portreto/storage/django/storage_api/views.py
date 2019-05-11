from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from django.http import HttpResponse
import hashlib
from django.conf import settings
from .models import File

class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    # Upload Image
    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        # Hash Value
        key = settings.GLOBALS["hash_key"]
        #Hash key
        hash = request.query_params.get('hash')
        #Check if hash key exists
        if hash == None : return Response(status=status.HTTP_400_BAD_REQUEST)
        # Check hash integrity
        hash_object = hashlib.sha256(bytes(key,'utf-8'))
        hex_dig = hash_object.hexdigest()
        if hex_dig != hash : return Response(status=status.HTTP_400_BAD_REQUEST)
        # Validate data
        if not file_serializer.is_valid(): return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Check duplicates
        filename = file_serializer.validated_data['file']
        if len(File.objects.filter(file=filename)) > 0: return Response(status=status.HTTP_409_CONFLICT)
        # Save file
        file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)

    # Get Image
    def get(self, request):
        # get hashing key
        key = settings.GLOBALS["hash_key"]
        # get filename
        filename = request.query_params.get('image')
        hash = request.query_params.get('hash')
        # check filename
        if filename == None : return Response(status=status.HTTP_400_BAD_REQUEST)
        if hash == None : return Response(status=status.HTTP_400_BAD_REQUEST)
        # hash filename and key
        hash_object = hashlib.sha256(bytes(filename+key,'utf-8'))
        hex_dig = hash_object.hexdigest()
        # validate hash
        if hex_dig != hash : return Response(status=status.HTTP_400_BAD_REQUEST)
        # open image and return in
        image = open('data/'+ filename, 'rb')
        response = HttpResponse(content=image)
        response['Content-Type'] = 'image'
        return response

    def delete(self, request):
        # get hashing key
        key = settings.GLOBALS["hash_key"]
        # get filename
        filename = request.query_params.get('image')
        hash = request.query_params.get('hash')
        # check filename
        if filename == None : return Response(status=status.HTTP_400_BAD_REQUEST)
        if hash == None : return Response(status=status.HTTP_400_BAD_REQUEST)
        # hash filename and key
        hash_object = hashlib.sha256(bytes(filename+key,'utf-8'))
        hex_dig = hash_object.hexdigest()
        # validate
        if hex_dig != hash : return Response(status=status.HTTP_400_BAD_REQUEST)
        # query db
        files = File.objects.filter(file=filename)
        # Check if exists
        if len(files) != 1 : return Response(status=status.HTTP_404_NOT_FOUND)
        # Delete file
        file = files[0].delete()
        return Response(status=status.HTTP_200_OK)
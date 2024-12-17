from rest_framework import serializers
from . models import *

class Userserializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
class StudentDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model=StudentDetails
        fields='__all__'
        
class LibraryResourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model=LibraryResourses
        fields='__all__'
        
class StudentFeesSerializers(serializers.ModelSerializer):
    class Meta:
        model=StudentFees
        fields='__all__'
        
class LibrarySerializers(serializers.ModelSerializer):
    class Meta:
        model=Librarian
        fields='__all__'
        
class TecaherSerializers(serializers.ModelSerializer):
    class Meta:
        model=Teachers
        fields='__all__'
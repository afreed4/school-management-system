from rest_framework import serializers
from adminapp. models import *

class LibraryResourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model=LibraryResourses
        fields='__all__'
        
        
class LibrarianSerializers(serializers.ModelSerializer):
    class Meta:
        model=Librarian
        fields='__all__'
        
        
class StudentDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model=StudentDetails
        fields='__all__'
        
class LibrarySerializers(serializers.ModelSerializer):
    class Meta:
        model=Library
        fields='__all___'
        
class GradeSerializers(serializers.ModelSerializer):
    class Meta:
        model=GradeOfStudents
        fields='__all__'
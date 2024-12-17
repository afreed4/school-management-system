from rest_framework import serializers
from adminapp. models import *

class LibraryResourcesSerializers(serializers.ModelSerializer):
    class Meta:
        model=LibraryResourses
        fields='__all__'
        
        
class LibraryHistory(serializers.ModelSerializer):
     class Meta:
        model=Library
        fields='__all__'
    
        
class StudentDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model=StudentDetails
        fields='__all__'
        
class FeesSeriaizers(serializers.ModelSerializer):
    class Meta:
        model=StudentFees
        fields='__all__'
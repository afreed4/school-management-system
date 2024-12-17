from adminapp.models import *
from . serializers import *
from rest_framework import viewsets


class StudentViewSet(viewsets.ModelViewSet):
    queryset=StudentDetails.objects.all()
    serializer_class=StudentDetailsSerializers
    
class LibraryResourcesViewset(viewsets.ModelViewSet):
    queryset=LibraryResourses.objects.all()
    serializer_class=LibraryResourcesSerializers
    
    
class LibrariViewset(viewsets.ModelViewSet):
    queryset=Library.objects.all()
    serializer_class=LibraryHistory
    

    
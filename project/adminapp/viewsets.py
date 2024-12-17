from rest_framework import viewsets
from . models import *
from . serializers import *

class Viewsetuser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = Userserializers
    
class StudentViewSet(viewsets.ModelViewSet):
    queryset=StudentDetails.objects.all()
    serializer_class=StudentDetailsSerializers
    
class LibraryResourcesViewset(viewsets.ModelViewSet):
    queryset=LibraryResourses.objects.all()
    serializer_class=LibraryResourcesSerializers
    
class StudentFeesViewset(viewsets.ModelViewSet):
    queryset=StudentFees.objects.all()
    serializer_class=StudentFeesSerializers
    
class LibraryViewset(viewsets.ModelViewSet):
    queryset=Librarian.objects.all()
    serializer_class=LibrarySerializers
    
class TeacherFeesViewset(viewsets.ModelViewSet):
    queryset=Teachers.objects.all()
    serializer_class=TecaherSerializers
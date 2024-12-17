from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('view_student_by_libraryin/',views.ViewStudentData.as_view(),name='view_student_by_libraryin'),
    
    path('add_library_history/',views.AddLibraryHistory.as_view(),name='add_library_history'),
    path('edit_library_history/',views.EditLibraryHistory.as_view(),name='edit_library_history'),
    path('delete_library_history/',views.DeleteLibraryHistory.as_view(),name='delete_library_history'),
    path('view_library_history/',views.ViewLibraryHistory.as_view(),name='view_library_history'),
    
    path('add_library_resources/',views.AddLibraryDetails.as_view(),name='add_library_resources'),
    path('edit_library_resources/',views.EditLibraryDetails.as_view(),name='edit_library_resources'),
    path('delete_library_resources/',views.DeleteLibraryResources.as_view(),name='delete_library_resources'),
    path('view_library_resources/',views.ViewLibraryResources.as_view(),name='view_library_resources')
]
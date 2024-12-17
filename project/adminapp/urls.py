from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('login/',views.login_view,name='login'),
    
    path('viewstaff/',views.ViewStaff.as_view(),name='viewstaff'),
    path('addstaffadmin/',views.CreateStaff.as_view(),name='addstaffadmin'),
    path('admineditstaff/',views.EditStaff.as_view(),name='admineditstaff'),
    path('deletestaff/',views.DeleteStaff.as_view(),name='deletestaff'),
    
    path('adminviewstudents/',views.ViewStudentData.as_view(),name='adminviewstudents'),
    path('add_student/',views.AddStudents.as_view(),name='add_student'),
    path('edit_students/',views.EditStudents.as_view(),name='edit_students'),
    path('delete_student/',views.DeleteStudent.as_view(),name='delete_student'),
    
    path('view_library_resources/',views.ViewLibraryResources.as_view(),name='view_library_resources'),
    path('add_library_resources/',views.AddLibraryResourses.as_view(),name='add_library_resources'),
    path('edit_library_resources/',views.EditLibraryResources.as_view(),name='edit_library_resources'),
    path('delete_library_resources/',views.DeleteLibraryResources.as_view(),name='delete_library_resources'),
    
    path('add_fees_record/',views.AddFeesRecordOfaStudent.as_view(),name='add_fees_record'),
    path('edit_fees_record/',views.EditFeesRecord.as_view(),name='edit_fees_record'),
    path('view_fees_record_of_a_student/',views.ViewFeesRecords.as_view(),name='view_fees_record_of_a_student'),
    path('delete_fees_record/',views.DeleteFeesRecord.as_view(),name='delete_fees_record'),
    path('view_fees_record_of_all/',views.ViewFeesRecordsOfAll.as_view(),name='view_fees_record_of_all')
]


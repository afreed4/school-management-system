from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('view_student_details/',views.ViewStudentDatails.as_view(),name='view_student_details'),
    
    path('add_fees_record/',views.AddFeesRecordOfaStudent.as_view(),name='add_fees_record'),
    path('edit_fees_record/',views.EditFeesRecord.as_view(),name='edit_fees_record'),
    path('delete_fees_record/',views.DeleteFeesRecord.as_view(),name='delete_fees_record'),
    path('view_fees_record_of_all/',views.ViewFeesRecordsOfAll.as_view(),name='view_fees_record_of_all'),
    path('view_fees_record_of_a_student/',views.ViewFeesRecords.as_view(),name='view_fees_record_of_a_student'),
    
    path('view_library_history/',views.ViewLibraryHistory.as_view(),name='view_library_history')
]
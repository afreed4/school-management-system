from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from django.views.decorators.csrf import csrf_exempt
from adminapp. models import* 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from datetime import timedelta
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.decorators import permission_required
from adminapp.permissions import IsLibraryGroup,IsLibraryOrAdminGroup
from django.core.files.uploadedfile import InMemoryUploadedFile
from decimal import Decimal


class ViewStudentData(APIView):
    permission_classes=[IsLibraryGroup]
    
    def get(self,request):
        user=request.user
        try:
         librariyan=Librarian.objects.get(user=user)
        
        except Librarian.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user"
            })
            
        
            
        if librariyan.user.is_librarian==True:
            student_data=StudentDetails.objects.all()
            data_set=[]
            for x in student_data:
                try:
                    teacher_name=Teachers.objects.filter(grade=x.grade.grades)
                    teachers_name_data=[]
                    for y in teacher_name:
                        teachers_name_data.append({
                            "Name": y.user.full_name if y.user.full_name else "No Name"
                        })    
                except GradeOfStudents.DoesNotExist:
                    student_grade="Not Found"
                    teachers_name_data=[]
                
                data_set.append({
                    "Student ID":x.student_id,
                    "Full Name":x.full_name,
                    "Image":x.profile_image if x.profile_image else None,
                    "DOB":x.date_of_birth,
                    "Address":x.address,
                    "Place":x.place,
                    "Father Name":x.father_name,
                    "Mother Name":x.mother_name,
                    "Father Phone Number":x.father_ph,
                    "email":x.email,
                    "Educational Project":x.educational_project,
                    "Previous School Name":x.previous_school_name,
                    "Grade":x.grade.grades if x.grade.grades else None,
                    "Second Language":x.second_language,
                    "Emergency Contact":x.emergency_contact,
                    "Whatsapp Number":x.watsapp_number,
                    "Fees Due":x.total_payable if x.total_payable!=0 else "No Due",
                    "Teacher Name":teachers_name_data if teachers_name_data else None
                    
                })
            paginator=Paginator(data_set,1)
            pag_params=request.GET.get('page','1')
            
            try:
                page_obj = paginator.page(pag_params)
            except PageNotAnInteger:
                return JsonResponse({"message": "Page number is not an integer"}, status=400)
            except EmptyPage:
                return JsonResponse({"message": "Page number out of range"}, status=400)
            
            return Response({
                "count": paginator.count,
                "Num Pages": paginator.num_pages,
                "Results": page_obj.object_list,
                "Current Page": page_obj.number
            })
       
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have access to perform this operation"
            })
            
            
class ViewLibraryHistory(APIView):
    permission_classes=[IsLibraryOrAdminGroup]
    
    def get(self,request):
        user=request.user
        
        admin=None
        librariyan=None
      
        try:
             admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            pass
        
        if not admin:
            try:
                librariyan=Librarian.objects.get(user=user)
            except Librarian.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the logged in user "
                    })
            
        if (librariyan and librariyan.user.is_librarian==True) or (admin and admin.user.is_superuser==True):
            
            
            try:
                library_history_obj=Library.objects.all()
                data_set=[]
                for x in library_history_obj:
                    data_set.append({
                        "Book Name":x.book.book_name,
                        "Borrow Date":x.borrow_date,
                        "Return Date":x.return_date,
                        "Borrowed by":x.students.full_name,
                        "Librariyan Name":x.librarian.user.full_name if x.librarian else None,
                        
                    })
                    
                return Response({
                    "Status":"Succes",
                    "Message":"Data Fetched Successfully",
                    "Data":data_set
                })
            except Library.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Coudn't find any Library History"
                })
            
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have access to perform this operation"
            })
            
               
            
class AddLibraryHistory(APIView):
    
    permission_classes=[IsLibraryOrAdminGroup] # both Librariyan and Admin have access to the function
    
    def post(self,request):
        user=request.user
        
        admin=None
        librariyan=None
      
        try:
             admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            pass
        
        if not admin:
            try:
                librariyan=Librarian.objects.get(user=user)
            except Librarian.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the logged inn user "
                    })
            
        if (librariyan and librariyan.user.is_librarian==True) or (admin and admin.user.is_superuser==True):
            data=json.loads(request.body)
            book_id=data.get('book_id')
            borrow_date=data.get('borrow_date')
            return_date=data.get('return_date')
            student_id=data.get('student_id')
            
            
            
            if not student_id:
                return Response({
                    "Status":"Failed",
                    "Message":"Please provide book borrowed student's Student ID"
                })
            try:
                student_obj=StudentDetails.objects.get(student_id=student_id)
            except StudentDetails.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Coudn't find any student using provided Student ID, check provided Student ID and try again"
                })
            
            try:
                book_obj=LibraryResourses.objects.get(book_id=book_id)
            except LibraryResourses.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Coudn't find a library book using provided Book ID, check provided Book ID and try again"
                })
                
            try:
                library_obj=Library.objects.create(
                    book=book_obj,
                    borrow_date=borrow_date,
                    return_date=return_date,
                    students=student_obj,
                    librarian=librariyan if librariyan else None  # if a admin added a library history in the table librariyan field it will be Null and if a librariyan add the library history the column will populate with the librariyan's object
                )
                
                library_obj.save()
                
                return Response({
                    "Status":"Success",
                    "Message":f"Successfully assighned {book_obj.book_name} to {student_obj}"
                })
            except Exception as e:
                return Response({
                    "Status":"Failed",
                    "Message":f"An error occured {e}"
                })
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have access to perform this operation"
            })
            


class EditLibraryHistory(APIView):
    permission_classes=[IsLibraryOrAdminGroup] # both Librariyan and Admin have access to the function
    
    def patch(self,request):
        user=request.user
        
        admin=None
        librariyan=None
      
        try:
             admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            pass
        
        if not admin:
            try:
                librariyan=Librarian.objects.get(user=user)
            except Librarian.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the logged inn user "
                    })
            
        if (librariyan and librariyan.user.is_librarian==True) or (admin and admin.user.is_superuser==True):
            data=json.loads(request.body)
            library_id=data.get('library_id')
            
            if not library_id:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't countinue without providing Library ID"
                })
                
            student_id=data.get('student_id')
            book_id=data.get('book_id')
            borrow_date=data.get('borrow_date')
            return_date=data.get('return_date')
            
            try:
                student_obj=StudentDetails.objects.get(student_id=student_id)
            except StudentDetails.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Coudn't find any student using provided Student ID, check provided Student ID and try again"
                })
            
            try:
                book_obj=LibraryResourses.objects.get(book_id=book_id)
            except LibraryResourses.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Coudn't find a library book using provided Book ID, check provided Book ID and try again"
                })
                
            try:
                library_obj=Library.objects.get(library_id=library_id)
                
                library_obj.borrow_date=borrow_date
                library_obj.students=student_obj
                library_obj.book=book_obj
                library_obj.return_date=return_date
                
                library_obj.save()
                
                return Response({
                    "Status":"Success",
                    "Message":f"The Updation of {library_obj.library_id} is completed"
                })
                
            except Library.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Couldn't locate any Library records using provided library ID"
                })
                
            except Exception as e:
                return Response({
                    "Status":"Failed",
                    "Message":f"An error occured {e}"
                })
                
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have access to perform this operation"
            })
            
            
class DeleteLibraryHistory(APIView):
     permission_classes=[IsLibraryOrAdminGroup] # both Librariyan and Admin have access to the function
    
     def delete(self,request):
        user=request.user
        
        admin=None
        librariyan=None
      
        try:
             admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            pass
        
        if not admin:
            try:
                librariyan=Librarian.objects.get(user=user)
            except Librarian.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the logged in user "
                    })
            
        if (librariyan and librariyan.user.is_librarian==True) or (admin and admin.user.is_superuser==True):
            data=json.loads(request.body)
            library_history_id=data.get('library_history_id')
            
            try:
                library_history_obj=Library.objects.get(library_id=library_history_id)
                library_history_obj.delete()
                return Response({
                    "Status":"Success",
                    "Message":f"The deletion of {library_history_obj.library_id} is completed"
                })
                
            except Library.DoesNotExist:
                return Response({
                    "Status":"Success",
                    "Message":"Coudn't locate the library history using provided Library History ID, check provided ID and try again"
                })
                
            except Exception as e:
                return Response({
                    "Status":"Failed",
                    "Message":f"An error occured {e}"
                })
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have access to perform this operation"
            })
     
     
class ViewLibraryResources(APIView):
    permission_classes=[IsLibraryGroup]
    
    def get(self,request):
        user=request.user
        try:
         librariyan=Librarian.objects.get(user=user)
        
        except Librarian.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user"
            })
            
        
            
        if librariyan.user.is_librarian==True:
            data_set=[]
            fees_obj=LibraryResourses.objects.all()
            for x in fees_obj:
                data_set.append({
                    "Book ID":x.book_id,
                    "Book Name":x.book_name,
                    "Book Type":x.book_type,
                    "Author":x.author,
                    "Language":x.language,
                    "Status":x.status,
                })
                
            if data_set:
                return Response({
                    "Status":"Success",
                     "Message":"Library Resources data fetched successfully",
                     "Data":data_set
                })
                
            else:
                  return Response({
                    "Status":"Failed",
                     "Message":"No data found of Library Resources",
                    
                })
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
                    
            
class AddLibraryDetails(APIView):
    permission_classes=[IsLibraryGroup] # only Librariyan have access to the function
    
    def post(self,request):
        user=request.user
        
        try:
             librariyan=Librarian.objects.get(user=user)
        except Librarian.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the logged inn user "
                    })
            
        if librariyan.user.is_librarian==True:
             data=json.loads(request.body)
             book_name=data.get('book_name')
             book_type=data.get('book_type') # eg story, poem, novel etc..
             author=data.get('author')
             language=data.get('language')
             status=data.get('status')
             
             if LibraryResourses.objects.filter(book_name=book_name,author=author,language=language).exists():
                 return Response({
                     "Status":"Failed",
                     "Message":"Provided library book details is allready existed in the database"
                 })
             
             try:
                 book_obj=LibraryResourses.objects.create(
                     book_name=book_name,
                     book_type=book_type,
                     author=author,
                     language=language,
                     status=status
                 )
                 
                 book_obj.save()
                 
                 return Response({
                     "Status":"Success",
                     "Message":"The Library Resources saved successfully"
                 })
             except Exception as e:
                 return Response({
                     "Status":"Failed",
                     "Message":f"An error occured while saving the Libarary Resources {e}"
                 })
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have access to perform this operation"
            })
            
            
class EditLibraryDetails(APIView):
    permission_classes=[IsLibraryGroup]
    
    def patch(self, request):
         user=request.user
         try:
            librariyan=Librarian.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Libraryian"
                })
            
         if librariyan.user.is_librarian==True:
             data=json.loads(request.body)
             book_name=data.get('book_name')
             book_type=data.get('book_type') # eg story, poem, novel etc..
             author=data.get('author')
             language=data.get('language')
             status=data.get('status') #eg if the book is in stock or stock out or taken
             
             book_id=data.get('book_id')
             
             if not book_id:
                 return Response({
                     "Status":"Failed",
                     "Message":"Can't continue without providing Book ID"
                 })
                 
             try:
                 book_obj=LibraryResourses.objects.get(book_id=book_id)
                 if book_name:
                  book_obj.book_name=book_name
                 if book_type:
                  book_obj.book_type=book_type
                 if author:
                  book_obj.author=author
                 if language:
                  book_obj.language=language
                 if status:
                  book_obj.status=status
                  
                 book_obj.save()
                 
                 return Response({
                     "Status":"Success",
                     "Message":f"Book details of Book ID {book_id} updated successfully"
                 })
                 
             except LibraryResourses.DoesNotExist:
                 return Response({
                     "Status":"Failed",
                     "Message":f"Can't find a library resources using provided ID {book_id} check the provided ID and try again"
                 })
                 
             except Exception as e:
                 return Response({
                     "Status":"Failed",
                     "Message":f"An error occured {e}"
                 })
             
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            
            
class DeleteLibraryResources(APIView):
    permission_classes=[IsLibraryGroup]
    
    def delete(self, request):
         user=request.user
         try:
            librariyan=Librarian.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Libraryian"
                })
            
         if librariyan.user.is_librarian==True:
             data=json.loads(request.body)
            
             book_id=data.get('book_id')
             
             if not book_id:
                 return Response({
                     "Status":"Failed",
                     "Message":"Can't continue without providing Book ID"
                 })
                 
             try:
                 book_obj=LibraryResourses.objects.get(book_id=book_id)
                 book_obj.delete()
                 
                 return Response({
                     "Status":"Success",
                     "Message":f"Book details of Book ID {book_id} Deleted successfully"
                 })
                 
             except LibraryResourses.DoesNotExist:
                 return Response({
                     "Status":"Failed",
                     "Message":f"Can't delete the library resources using provided ID {book_id} check the provided ID and try again"
                 })
                 
             except Exception as e:
                 return Response({
                     "Status":"Failed",
                     "Message":f"An error occured {e}"
                 })
             
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            
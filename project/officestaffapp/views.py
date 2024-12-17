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
from adminapp.permissions import IsStaff
from django.core.files.uploadedfile import InMemoryUploadedFile
from decimal import Decimal



class ViewStudentDatails(APIView):
    permission_classes=[IsStaff]
    
    def get(self,request):
        user=request.user
        try:
         staff=Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Staff"
            })
            
        if staff.user.is_staff==True:
            student_data=StudentDetails.objects.all()
            data_set=[]
            for x in student_data:
                try:
                    # student_grade=GradeOfStudents.objects.get(grades=)
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
                "Message":"You don't have permission to perform this action"
            })
            

class AddFeesRecordOfaStudent(APIView):
    permission_classes=[IsStaff]
    
    def post(self, request):
         user=request.user
         try:
            staff=Staff.objects.get(user=user)
         except Staff.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Staff"
                })
            
         if staff.user.is_staff==True:
             data=json.loads(request.body)
             
             student_id=data.get('student_id')
             signature=data.get('signature')
             amount_paid=data.get('amount_paid')
             payment_method=data.get('payment_method')
             total_amount=data.get('total_amount') # if not provided total amount  will default to 15000
             
             payment_status=data.get('payment_status')
             account_holder_name=data.get('account_holder_name')
             bank_name=data.get('bank_name')
             bank_branch=data.get('bank_branch')
             account_number=data.get('account_number')
             ifsc_code=data.get('ifsc_code')
             supporting_documents=data.get('supporting_documents')
             
             if not student_id:
                 return Response({
                     "Status":"Failed",
                     "Message":"Please provide Student ID"
                 })
                 
             fees_record_data=[
                 amount_paid,payment_method,
                 account_holder_name,account_number,ifsc_code,
                 bank_name,bank_branch
             ]
                 
             if all(var in fees_record_data for var in [amount_paid, payment_method, account_holder_name, account_number, ifsc_code, bank_name, bank_branch]):
                 
                 try:
                    amount_paid = Decimal(amount_paid) if amount_paid else Decimal('0.00')
                    total_amount = Decimal(total_amount) if total_amount else Decimal('15000.00')
                 except (ValueError, TypeError) as e:
                    return Response({
                        "Status": "Failed",
                        "Message": f"Invalid value for amount fields: {e}"
                    })
                    
                 
                 try:
                     student_obj=StudentDetails.objects.get(student_id=student_id)
                 except StudentDetails.DoesNotExist:
                     return Response({
                         "Status":"Failed",
                         "Message":f"Can't find the student assossiated with {student_id}"
                     })
                     
                 try:
                     student_fees_obj=StudentFees.objects.create(
                         student=student_obj,
                         signature=signature,
                         amount_paid=amount_paid,
                         payment_method=payment_method,
                         payment_status=payment_status,
                         total_amount=total_amount if total_amount else 15000 ,
                         account_holder_name=account_holder_name,
                         bank_name=bank_name,
                         bank_branch=bank_branch,
                         account_number=account_number,
                         ifsc_code=ifsc_code,
                         supporting_documents=supporting_documents
                     )
                     
                    
                     
                     student_fees_obj.save()
                     return Response({
                         "Status":"Success",
                         "Message":f"Student Fees Record saved successfully total amount={student_fees_obj.total_amount}, Total Due={student_obj.total_payable}, payed amount={amount_paid}"
                     })
                     
                 except Exception as e:
                     return Response({
                         "Status":"Failed",
                         "Message":f"An error occured while saving the student fees record {e}"
                  })
                     
             else:
              return  Response({
                  "Status":"Failed",
                  "Message":"Please include all the below values Amount paid, Payment method, Account holder name, Account number, IFSC code, Bank name, Bank branch"
              })
             
             
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            
            
class EditFeesRecord(APIView):
    permission_classes=[IsStaff]
    
    def patch(self, request):
         user=request.user
         try:
            staff=Staff.objects.get(user=user)
         except Staff.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Staff"
                })
            
         if staff.user.is_staff==True:
             data=json.loads(request.body)
             
             student_id=data.get('student_id')
             signature=data.get('signature')
             amount_paid=data.get('amount_paid')
             payment_method=data.get('payment_method')
             total_amount=data.get('total_amount') # if not provided total amount  will default to 15000
             
             payment_status=data.get('payment_status')
             account_holder_name=data.get('account_holder_name')
             bank_name=data.get('bank_name')
             bank_branch=data.get('bank_branch')
             account_number=data.get('account_number')
             ifsc_code=data.get('ifsc_code')
             supporting_documents=data.get('supporting_documents')
             
             if not student_id:
                 return Response({
                     "Status":"Failed",
                     "Message":"Please provide Student ID"
                 })
                 
             try:
                    amount_paid = Decimal(amount_paid) if amount_paid else Decimal('0.00')
                    total_amount = Decimal(total_amount) if total_amount else Decimal('15000.00')
             except (ValueError, TypeError) as e:
                    return Response({
                        "Status": "Failed",
                        "Message": f"Invalid value for amount fields: {e}"
                    })
                    
             try:
                 student_obj=StudentDetails.objects.get(student_id=student_id)
                 student_fees_obj=StudentFees.objects.filter(student=student_obj).last()
                 
                 if student_fees_obj==None:
                     return Response({
                         "Status":"Failed",
                         "Message":"Can't change the fees record of the student, create a student fees record first"
                     })
                 
                 if signature:
                  student_fees_obj.signature=signature
                 if payment_method:
                  student_fees_obj.payment_method=payment_method
                 if total_amount:
                  student_fees_obj.total_amount=total_amount
                 if payment_status:
                  student_fees_obj.payment_status=payment_status
                 if account_holder_name:
                  student_fees_obj.account_holder_name=account_holder_name
                 if bank_name:
                  student_fees_obj.bank_name=bank_name
                 if bank_branch:
                  student_fees_obj.bank_branch=bank_branch
                 if account_number:
                  student_fees_obj.account_number=account_number
                 if ifsc_code:
                  student_fees_obj.ifsc_code=ifsc_code
                 if supporting_documents:
                  student_fees_obj.supporting_documents=supporting_documents
                 if amount_paid:
                     student_fees_obj.amount_paid=amount_paid
                  
                 student_fees_obj.save()
                 return Response({
                     "Status":"Success",
                     "Message":f"Fees Record of {student_id} changed successfully"
                 })
                     
             except StudentDetails.DoesNotExist:
                 return Response({
                     "Status":"Failed",
                     "Message":f"Can't find any students using the student ID {student_id}"
                 })
             except Exception as e:
                 return Response({
                     "Status":"Failed",
                     "Message":f"and error occured {e}"
                 })
                 
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
                    
class ViewFeesRecordsOfAll(APIView):
    permission_classes=[IsStaff]
    
    def get(self,request):
        user=request.user
        try:
         staff=Staff.objects.get(user=user)
        except Staff.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Staff"
            })
        
        if staff.user.is_staff==True:
            data_set=[]
            fees_obj=StudentFees.objects.all()
            for x in fees_obj:
                data_set.append({
                    "Full Name":x.student.full_name,
                    "total amount":x.total_amount,
                    "Amount Paid":x.amount_paid,
                    "Balance Amount":x.balance_amount,
                    "Payment Status":x.payment_status,
                    "Gender":x.student.gender,
                    "Email":x.student.email,
                    "Father's Phone Number":x.student.father_ph,
                    "Whatsapp Number":x.student.watsapp_number,
                    "Guardian":x.student.guardian,
                    "Profile Image":x.student.profile_image if x.student.profile_image else None
                })
                
            if data_set:
                return Response({
                    "Status":"Success",
                     "Message":"Student Fees data fetched successfully",
                     "Data":data_set
                })
                
            else:
                  return Response({
                    "Status":"Failed",
                     "Message":"No data found of student's fees Record",
                    
                })
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            
                    
                    
class ViewFeesRecords(APIView):
    permission_classes=[IsStaff]
    
    def get(self,request):
         user=request.user
         try:
            staff=Staff.objects.get(user=user)
         except Staff.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Staff"
                })
            
         if staff.user.is_staff==True:
             data=json.loads(request.body)
             student_id=data.get('student_id')
             
             try:
                 student_obj=StudentDetails.objects.get(student_id=student_id)
             except StudentDetails.DoesNotExist:
                 return Response({
                         "Status":"Failed",
                         "Message":f"Can't find the Student using provided student ID {student_id}', check provided Student ID and try again"
                     })
             try:
                  student_fees_data=StudentFees.objects.filter(student=student_obj)
                  data_set=[]
                  
                  for x in student_fees_data:
                      data_set.append({
                          "Total Amount":x.total_amount,
                          "Signature":x.signature,
                          "Paid Amonts":x.amount_paid,
                          "Balance Amount":x.balance_amount,
                          "Payment Method":x.payment_method,
                          "Payment dates":x.payment_date,
                          "Account Holder Name":x.account_holder_name,
                          "Account Number":x.account_number,
                          "Bank Name":x.bank_name,
                          "Bank Branch":x.bank_branch,
                          "Account Number":x.account_number,
                          "IFSC Code":x.ifsc_code,
                          "Supporting Documents":x.supporting_documents if x.supporting_documents else None
                      })
                  
                  return Response({
                      "Status":"Success",
                      "Message":f"The fees records of {student_id} fetched successfully",
                      "Data":data_set
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
                    

class DeleteFeesRecord(APIView):
    permission_classes=[IsStaff]
    
    def delete(self,request):
         user=request.user
         try:
            staff=Staff.objects.get(user=user)
         except Staff.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if staff.user.is_staff==True:
             data=json.loads(request.body)
             student_id=data.get('student_id')
             
             try:
                 student_obj=StudentDetails.objects.get(student_id=student_id)
                 if not student_obj:
                     return Response({
                         "Status":"Failed",
                         "Message":f"Can't find the provided student ID {student_id}'s fees record, check provided Student ID and try again"
                     })
                 student_fees_obj=StudentFees.objects.filter(student=student_obj)
                 
                 student_fees_obj.delete()
                 
                 return Response({
                     "Status":"Success",
                     "Message":f"The fees record of {student_id} has deleted successfully"
                 })
             except Exception as e:
                 return Response({
                     "Status":'Failed',
                     "Message":f"An error occured {e}"
                 })
             
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
                    
                    
class ViewLibraryHistory(APIView):
    
    permission_classes=[IsStaff]
    
    def get(self,request):
         user=request.user
         try:
            staff=Staff.objects.get(user=user)
         except Staff.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if staff.user.is_staff==True:
             data=json.loads(request.body)
             library_id=data.get('library_id')
             
             try:
                 data_set=[]
                 library_obj=Library.objects.filter(library_id=library_id)
                 for x in library_obj:
                     data_set.append({
                         "ID":library_id,
                         "Book Name":x.book.book_name,
                         "Librariyan Name":x.librarian.user.full_name,
                         "Borrow date":x.borrow_date,
                         "Return Date":x.return_date,
                         "Borrowed By":x.students.full_name
                     })
                     
                 return Response({
                     "Status":"Success",
                     "Message":"The Library History Data Fetched Successfully",
                     "Data":data_set
                 })
                 
             except Library.DoesNotExist:
                 return Response({
                     "Status":"Failed",
                     "Message":"Coudn't find any Library History using provided Library ID, check provided ID and try again"
                 })
                
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })()
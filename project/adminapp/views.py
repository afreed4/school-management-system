from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json
from django.views.decorators.csrf import csrf_exempt
from . models import* 
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from datetime import timedelta
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.decorators import permission_required
from .permissions import IsAdminGroup,IsAdministratorGroup
from django.core.files.uploadedfile import InMemoryUploadedFile
from decimal import Decimal

# Create your views here.



@csrf_exempt
def login_view(request):
    user_list=User.objects.values_list('email',flat=True)
    print(user_list)
   
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            print(password)
            
            if email:
                 user=User.objects.get(email=email)
                 user = authenticate(request, username=email, password=password)

                 if user is not None:
                        return JsonResponse({
                            'status': 'Success',
                            'message': 'Login Success',
                            'email': user.email
                        })
                 else:
                        print("can't login")
                        
                        return JsonResponse({
                            'status': 'Failed',
                            'message': 'Invalid Credentials',
                           
                        })
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'Failed',
                'message': 'Invalid JSON format'
            })
    return JsonResponse({
        'status': 'Failed',
        'message': 'Invalid request method'
    })


class ViewStudentData(APIView):
    permission_classes=[IsAdminGroup]
    
    def get(self,request):
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Admin"
            })
            
        if admin.user.is_superuser==True:
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
                "Message":"Requested user is non Admin"
            })
            

# admin adding new staffs
class CreateStaff(APIView):
    permission_classes=[IsAdminGroup]    #admin permission group
    
    def post(self,request):
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in use as Admin"
            })
        
        if admin.user.is_superuser==True:
            data=json.loads(request.body)
            #  user table datas
            full_name=data.get('full_name')
            phone_number=data.get('phone_number')
            date_of_birth=data.get('DOB')
            address=data.get('address')
            gender=data.get('gender')
            email=data.get('email')
            age=data.get('age')
            watsapp_number=data.get('watsapp_number')
            joining_date=data.get('joining_date')
            password=data.get('password')
            joined_date=data.get('joined_date')
            
            district=data.get('district')
            state=data.get('state')
            
            # Staff model Data
            staff_type=data.get('staff_type')
            qualification=data.get('qualification')
            certification=data.get('certification')
            profile_img=data.get('profile_img')
            experience=data.get('experience')
            about=data.get('about')
            
            # Teachers model Data
            teaching_position=data.get('teaching_position')
            specialised_subjects=data.get('specialised_subjects')
            teaching_license=data.get('teaching_license')
            grade=data.get('grade')
            
            if not (full_name and phone_number and email and  staff_type and qualification): #required fields
                return Response({
                    "Status":"Failed",
                    "Message":"Can't add a staff without providing Full Name , Phone Number , Email , Staff Type , Qualification , Certification"
                })
            
            if User.objects.filter(email=email).exists():
                return Response({
                    "Status":"Failed",
                    "Message":f'The email {email} you have provided is allready exists, try again with defferent email'
                })
                
            if User.objects.filter(phone_number=phone_number).exists():
                 return Response({
                    "Status":"Failed",
                    "Message":f'The Phone Number {phone_number} you have provided is allready exists, try again with defferent Phone Number'
                })
            
           
            district_obj=None
            if district:
                    try:
                        district_obj=District.objects.get(name=district)
                    except District.DoesNotExist:
                        return Response({
                            "Status":"Failed",
                            "Message":"Provided District is not available"
                        })
                        
            state_obj=None  
            if state:
                    try:
                        state_obj=State.objects.get(name=state)
                    except State.DoesNotExist:
                        return Response({
                            "Status":"Failed",
                            "Message":"Provided State is not available try different State name"
                        })
                        
                        
            try:
                        new_staff_type=str(staff_type).lower()
                        if staff_type=='librarian':
                            library_user=User.objects.create(
                            full_name=full_name,
                            phone_number=phone_number,
                            date_of_birth=date_of_birth,
                            address=address,
                            gender=gender,
                            email=email,
                            age=age,
                            watsapp_number=watsapp_number,
                            district=district_obj,
                            state=state_obj,
                            is_librarian=True,
                            joining_date=joined_date if joined_date else datetime.datetime.today()
                            )
                            
                            librarian=Librarian.objects.create(
                                user=library_user,
                                qualification=qualification,
                                certification=certification if certification else None,
                                profile_img=profile_img if profile_img else None,
                                experience=experience,
                            )
                            
                            library_user.set_password(password)
                            library_user.save()
                            librarian.save()
                            
                            return Response({
                                "Status":"Success",
                                "Message":f"User {full_name} saved successfully"
                            })
                        
                        elif staff_type=='teaching_staff':
                             teaching_user=User.objects.create(
                                full_name=full_name,
                                phone_number=phone_number,
                                date_of_birth=date_of_birth,
                                address=address,
                                gender=gender,
                                email=email,
                                age=age,
                                watsapp_number=watsapp_number,
                                district=district_obj,
                                state=state_obj,
                                is_teaching_staff=True,
                                joining_date=joined_date if joined_date else datetime.datetime.today()
                             )
                             
                            
                             try:
                                 grade_obj=GradeOfStudents.objects.get(grades=grade)
                             except GradeOfStudents.DoesNotExist:
                                 return Response({
                                     "Status":"Failed",
                                     "Message":"Provided Grade is not available for our school"
                                 })
                             teacher=Teachers.objects.create(
                                 user=teaching_user,
                                 qualification=qualification,
                                 certifiation=certification,
                                 experience=experience,
                                  teaching_position=teaching_position,
                                    specialised_subjects=specialised_subjects,
                                    teaching_license=teaching_license,
                                    grade=grade_obj,
                                    about=about,
                             )
                             
                             teaching_user.set_password(password)
                             teaching_user.save()
                             teacher.save()
                             
                             return Response({
                                "Status":"Success",
                                "Message":f"User {full_name} saved successfully"
                            })
                             
                            
                        staff_user=User.objects.create(
                            full_name=full_name,
                            phone_number=phone_number,
                            date_of_birth=date_of_birth,
                            address=address,
                            gender=gender,
                            email=email,
                            age=age,
                            watsapp_number=watsapp_number,
                            district=district_obj,
                            state=state_obj,
                            is_staff=True,
                            joining_date=joined_date if joined_date else datetime.datetime.today()
                        )
                        
                        
                        new_staff_type=str(staff_type).lower()
                        staff_type_mapping={
                            'administrative': 'is_administrative',
                            'accountant': 'is_accountant',
                            'clerk': 'is_clerk',
                            'it_administrator': 'is_IT_administrator',
                            }              
                        
                        if new_staff_type in staff_type_mapping:
                            staff_data = {
                                'user': staff_user,
                                'qualification': qualification,
                                'certification': certification if certification else None,
                                'experience': experience,
                                'profile_img': profile_img if profile_img else None,
                                'about': about,
                                staff_type_mapping[new_staff_type]: True,  # Dynamically set the specific field
                            }
                            staff = Staff(**staff_data)
                            staff_user.set_password(password)
                            staff_user.save()
                            staff.save()
                            
                            return Response({
                                "Status":"Success",
                                "Message":f"User {full_name} saved successfully"
                            })
                        else:
                            return Response({
                                "Status":"Failed",
                                "Message":f"Invalid staff type provided. Valid types are: Librarian, Teaching Staff, Accountant, Clerck, IT Administrator."
                            })
                    
            except Exception as e:
                        return Response({
                            "Status":"Failed",
                            "Message": f"An error occurred: {str(e)}"
                        })
                        
        else:
             return Response({
                "Status":"Failed",
                "Message":"You don't have permission to add staff"
            })
                        
                
                
class EditStaff(APIView):
    permission_classes=[IsAdminGroup]
    
    def patch(self,request):
       
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in use as Admin"
            })
        
        if admin.user.is_superuser==True:
            
            # User model datas
            data=json.loads(request.body)
            full_name=data.get('full_name')
            phone_number=data.get('phone_number')
            date_of_birth=data.get('DOB')
            address=data.get('address')
            gender=data.get('gender')
            age=data.get('age')
            watsapp_number=data.get('watsapp_number')
            district=data.get('district')
            state=data.get('state')
            
            #staff model datas
            experience=data.get('experience')
            about=data.get('about')
            user_id=data.get('staff_id')
            
            #Teacher model datas
            grade=data.get('grade')
            teaching_position=data.get('teaching_position')
            specialised_subjects=data.get('specialised_subjects')
            
            new_user_id=str(user_id)[:2].upper()
                
            if district:
                try:
                    district_obj=District.objects.get(name=district)
                except District.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the provided district check you'r district and try again"
                    })
                    
            if state:
                try:
                    state_obj=State.objects.get(name=state)
                except State.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the provided State check you'r State and try again"
                    })
                    
            if grade:
                try:
                    grade_obj=GradeOfStudents.objects.get(grades=grade)
                except GradeOfStudents.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"The provided Grade is not available in our school"
                    })
                  
               
            if new_user_id=='AD' or new_user_id=='AC' or new_user_id=='CL' or user_id=='IT':
                try:
                    staff_obj=Staff.objects.get(staff_id=user_id)
                except Staff.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":f"Can't find the Administrator using {user_id}"
                    })
                    
                if full_name:
                 staff_obj.user.full_name=full_name
                if date_of_birth:
                 staff_obj.user.date_of_birth=date_of_birth
                if address:
                 staff_obj.user.address=address
                if gender:
                 staff_obj.user.gender=gender
                if age:
                 staff_obj.user.age=age
                if watsapp_number:
                 staff_obj.user.watsapp_number=watsapp_number
                if state:
                    staff_obj.user.state=state_obj
                if district:
                    staff_obj.user.district=district_obj
                
                if experience:
                 staff_obj.experience=experience
                if about:
                 staff_obj.about=about
                
                staff_obj.user.save()
                staff_obj.save()
                
                return Response({
                    "Status":"Success",
                    "Message":f"User {full_name} Updated Successfully"
                })
                
            elif new_user_id=='TE':
                try:
                    teacher_obj=Teachers.objects.get(teachers_id=user_id)
                except Teachers.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":f"There is no Teachers who's assossiated with provided Staff ID {user_id}"
                    })
                if full_name:
                 teacher_obj.user.full_name=full_name
                if date_of_birth:
                 teacher_obj.user.date_of_birth=date_of_birth
                if address:
                 teacher_obj.user.address=address
                if gender:
                 teacher_obj.user.gender=gender
                if age:
                 teacher_obj.user.age=age
                if watsapp_number:
                 teacher_obj.user.watsapp_number=watsapp_number
                if state:
                    teacher_obj.user.state=state_obj
                if district:
                    teacher_obj.user.district=district_obj
                    
                if experience:
                 teacher_obj.experience=experience
                teacher_obj.grade=grade_obj
                if teaching_position:
                 teacher_obj.teaching_position=teaching_position
                if specialised_subjects:
                 teacher_obj.specialised_subjects=specialised_subjects
                if about:
                 teacher_obj.about=about
                if grade:
                    teacher_obj.grade=grade_obj
                 
                teacher_obj.user.save()
                teacher_obj.save()
                
                return Response({
                    "Status":"Success",
                    "Message":f"User {full_name} Updated Successfully"
                })
                
                
            elif new_user_id=='LI':
                try:
                 librarian_obj=Librarian.objects.get(id_of_librarian=user_id)
                except Librarian.DoesNotExist:
                     return Response({
                        "Status":"Failed",
                        "Message":f"There is no Librariyan who's assossiated with provided Staff ID {user_id}"
                    })
                if full_name:
                 librarian_obj.user.full_name=full_name
                if date_of_birth:
                 librarian_obj.user.date_of_birth=date_of_birth
                if address:
                 librarian_obj.user.address=address
                if gender:
                 librarian_obj.user.gender=gender
                if age:
                 librarian_obj.user.age=age
                if watsapp_number:
                 librarian_obj.user.watsapp_number=watsapp_number
                if state:
                    librarian_obj.user.state=state
                if district:
                    librarian_obj.user.district=district
                
                if experience:
                 librarian_obj.experience=experience
                
                librarian_obj.user.save()
                librarian_obj.save()
                
                return Response({
                    "Status":"Success",
                    "Message":f"User {full_name} Updated Successfully"
                })
                
            else:
                return Response({
                    "Status":"Failed",
                    "Message":"Invalid User id or no case found"
                })
                
                 
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            

class DeleteStaff(APIView):
    permission_classes=[IsAdminGroup]
    
    def delete(self,request):
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Admin"
            })
        
        if admin.user.is_superuser==True:
            data=json.loads(request.body)
            staff_id=data.get('staff_id')
            
            if not staff_id:
             return Response({
                "Status":"Failed",
                "Message":"Please Provide a custom ID"
            })
            
            new_staff_id=str(staff_id)[:2].upper()
            if new_staff_id=='TE':
                try:
                    teacher_obj=Teachers.objects.get(teachers_id=staff_id)
                    
                    teacher_obj.user.delete()
                    teacher_obj.delete()
                    return Response({
                        "Status":"Success",
                        "Message":"User dealeted Successfully"
                    })
                except Teachers.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the User, check the provided Staff ID and try again"
                    })
                    
            elif new_staff_id=='LI':
                try:
                    librarian_obj=Librarian.objects.get(id_of_librarian=staff_id)
                    
                    librarian_obj.user.delete()
                    librarian_obj.delete()
                    return Response({
                        "Status":"Success",
                        "Message":"User dealeted Successfully"
                    })
                except Librarian.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the User, check the provided Staff ID and try again"
                    })
                    
            elif new_staff_id=='AD' or new_staff_id=='AC' or new_staff_id=='CL' or new_staff_id=='IT':
                try:
                    staff_obj=Staff.objects.get(staff_id=staff_id)
                    
                    staff_obj.user.delete()
                    staff_obj.delete()
                    return Response({
                        "Status":"Success",
                        "Message":"User dealeted Successfully"
                    })
                except Staff.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Can't find the User, check the provided Staff ID and try again"
                    })
                    
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
        

class ViewStaff(APIView):
    permission_classes=[IsAdminGroup]
    
    def get(self,request):
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Admin"
            })
        
        if admin.user.is_superuser==True:
            data_set=[]
            staff_obj=Staff.objects.all()
            for x in staff_obj:
                data_set.append({
                    "Full Name":x.user.full_name,
                    "Qualification":x.qualification,
                    "Phone Number":x.user.phone_number,
                    "Date of birth":x.user.date_of_birth,
                    "Address":x.user.address,
                    "Gender":x.user.gender,
                    "Email":x.user.email,
                    "Age":x.user.age,
                    "Whatsapp Number":x.user.watsapp_number,
                    "District":x.user.district.name,
                    "Joining date":x.user.joining_date
                })
                
            if data_set:
                return Response({
                    "Status":"Success",
                     "Message":"Staff data fetched successfully",
                     "Data":data_set
                })
                
            else:
                  return Response({
                    "Status":"Failed",
                     "Message":"No data found of staff's",
                    
                })
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            

class AddStudents(APIView):
    
    permission_classes=[IsAdminGroup]
    def post(self,request):
        user=request.user
        try:
            admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in use as Admin"
                })
            
        if admin.user.is_superuser==True:
            data=json.loads(request.body)
            full_name=data.get('full_name')
            date_of_birth=data.get('DOB')
            profile_image=data.get('profile_image')
            address=data.get('address')
            place=data.get('place')
            father_name=data.get('father_name')
            mother_name=data.get('mother_name')
            father_ph=data.get('father_phone_number')
            gender=data.get('gender')
            guardian=data.get('guardian')
            joining_date=data.get('joining_date')
            email=data.get('email')
            educational_project=data.get('educational_project')
            previous_school_name=data.get('previous_school_name')
            second_language=data.get('second_language')
            emergency_contact=data.get('emergency_contact')
            watsapp_number=data.get('whatsapp_number')
            
            country_code=data.get('country_code')
            grade=data.get('grade')
            
            student_important_data=[full_name,date_of_birth,profile_image,address,guardian,email,educational_project,second_language,emergency_contact,watsapp_number,grade]
            
            if all(var in student_important_data for var in [full_name, date_of_birth, profile_image, address, guardian, email, educational_project, second_language, emergency_contact, watsapp_number, grade]):
                
                if StudentDetails.objects.filter(email=email).exists():
                    return Response({
                        "Status":"Failed",
                        "Message":f"Provided Email {email} allready existed try again with deffrent email "
                    })
                
                if country_code:
                    country_code_obj=None
                    try:
                        country_code_obj=Country_Codes.objects.get(calling_code=country_code)
                    except Country_Codes.DoesNotExist:
                        return Response({
                            "Status":"Failed",
                            "Message":f"Provided Country code is not available try with diffrent Coundry code"
                        })
                        
                grade_obj=None
                try:
                    grade_obj=GradeOfStudents.objects.get(grades=grade)
                except GradeOfStudents.DoesNotExist:
                    return Response({
                        "Status":"Failed",
                        "Message":"Provided Grade is not available in our school try grades from 1 to 12"
                    })
                    
                try:
                    student_obj=StudentDetails.objects.create(
                        full_name=full_name,
                        date_of_birth=date_of_birth,
                        profile_image=profile_image,
                        address=address,
                        place=place,
                        father_name=father_name,
                        mother_name=mother_name,
                        father_ph=father_ph,
                        country_code=country_code_obj,
                        gender=gender,
                        guardian=guardian,
                        joining_date=joining_date if joining_date else datetime.datetime.today(),
                        email=email,
                        educational_project=educational_project,
                        previous_school_name=previous_school_name,
                        grade=grade_obj,
                        second_language=second_language,
                        emergency_contact=emergency_contact,
                        watsapp_number=watsapp_number,
                    )
                    
                    student_obj.save()
                    return Response({
                        "Status":"Success",
                        "Message":f"Student Successfully saved {email}"
                    })
                
                except Exception as e:
                    return Response({
                        "Status":"Failed",
                        "Message":f" An error occures {e}"
                    })
            
            else:
                return Response({
                    "Status":"Failed",
                    "Message":f"Provide all Datas of student, important datas are Full Name, Date Of Birth, Profile Image, Address, Guardian, Email, Educational Project, Second Language, Emergency Contact, Watsapp Number, Grade"
                })
            
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            
    
class EditStudents(APIView):
    permission_classes=[IsAdminGroup]
    def post(self,request):
        user=request.user
        try:
            admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in use as Admin"
                })
            
        if admin.user.is_superuser==True:
            data=json.loads(request.body)
            full_name=data.get('full_name')
            date_of_birth=data.get('DOB')
            profile_image=data.get('profile_image')
            address=data.get('address')
            place=data.get('place')
            father_name=data.get('father_name')
            mother_name=data.get('mother_name')
            father_ph=data.get('father_phone_number')
           
            guardian=data.get('guardian')
        
            educational_project=data.get('educational_project')
           
            second_language=data.get('second_language')
            emergency_contact=data.get('emergency_contact')
            watsapp_number=data.get('whatsapp_number')
            
            student_id=data.get('student_id')
            
            grade=data.get('grade')
            
            if not student_id:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't continue without providing Students ID"
                })
            
            try:
                student_obj=StudentDetails.objects.get(student_id=student_id)
            except StudentDetails.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":f"Can't find the Student using the provided Student ID {student_id}"
                })
                
            grade_obj=None
            try:
                grade_obj=GradeOfStudents.objects.get(grades=grade)
            except GradeOfStudents.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"The Grade is not available in our school try again between 1st grade to 12 grade"
                })
            
            if full_name:
             student_obj.full_name=full_name
            if date_of_birth:
             student_obj.date_of_birth=date_of_birth
            if profile_image:
                student_obj.profile_image=profile_image
            if address:
                student_obj.address=address
            if place:
                student_obj.place=place
            if father_name:
                student_obj.father_name=father_name
            if mother_name:
                student_obj.mother_name=mother_name
            if father_ph:
                student_obj.father_ph=father_ph
            if guardian:
                student_obj.guardian=guardian
            if educational_project:
                student_obj.educational_project=educational_project
            if second_language:
                student_obj.second_language=second_language
            if emergency_contact:
                student_obj.emergency_contact=emergency_contact
            if watsapp_number:
                student_obj.watsapp_number=watsapp_number
            if grade:
                student_obj.grade=grade_obj
            
            student_obj.save()
            
            return Response({
                "Status":"Success",
                "Message":f"Student {student_id} updated successfully"
            })
                
            
        else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
            
    
class DeleteStudent(APIView):
    
    permission_classes=[IsAdminGroup]
    
    def delete(self,request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
             data=json.loads(request.body)
             student_id=data.get('student_id')
             
             if not student_id:
                 return Response({
                     "Status":"Failed",
                     "Message":"Can't delete a user without providing Student ID"
                 })
             
             try:
                  student_obj=StudentDetails.objects.get(student_id=student_id)
                  student_obj.delete()
                  return Response({
                      "Status":"Success",
                      "Message":f"Successfully deleted {student_id}"
                  })
                  
             except StudentDetails.DoesNotExist:
                    return Response({
                        "Status":"Success",
                        "Message":f"Can't find the Student using the provided Student ID {student_id} Check you'r provided ID and try again"
                    })
                    
         else:
            return Response({
                "Status":"Failed",
                "Message":"You don't have permission to perform this action"
            })
                    
                    


class AddLibraryResourses(APIView):
    permission_classes=[IsAdminGroup]
    
    def post(self, request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
                "Message":"You don't have permission to perform this action"
            })
            
            
class ViewLibraryResources(APIView):
    permission_classes=[IsAdminGroup]
    
    def get(self,request):
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Admin"
            })
        
        if admin.user.is_superuser==True:
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
             
                    
                    
class EditLibraryResources(APIView):
    permission_classes=[IsAdminGroup]
    
    def patch(self, request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
    permission_classes=[IsAdminGroup]
    
    def delete(self, request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
            
            

class ViewFeesRecordsOfAll(APIView):
    permission_classes=[IsAdminGroup]
    
    def get(self,request):
        user=request.user
        try:
         admin=Admin.objects.get(user=user)
        except Admin.DoesNotExist:
            return Response({
                "Status":"Failed",
                "Message":"Can't find the logged in user as Admin"
            })
        
        if admin.user.is_superuser==True:
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
            

            
class AddFeesRecordOfaStudent(APIView):
    permission_classes=[IsAdminGroup]
    
    def post(self, request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
    permission_classes=[IsAdminGroup]
    
    def patch(self, request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
                    
                    
                    
class ViewFeesRecords(APIView):
    permission_classes=[IsAdminGroup]
    
    def get(self,request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
    permission_classes=[IsAdminGroup]
    
    def delete(self,request):
         user=request.user
         try:
            admin=Admin.objects.get(user=user)
         except Admin.DoesNotExist:
                return Response({
                    "Status":"Failed",
                    "Message":"Can't find the logged in user as Admin"
                })
            
         if admin.user.is_superuser==True:
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
                    
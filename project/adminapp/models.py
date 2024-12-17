from django.db import models
import re
from django.contrib.auth.models import Permission,Group
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
from django.utils import timezone
import random
from django.core.validators import RegexValidator
import phonenumbers
from django.conf import settings
import uuid
from django.db import models


phone_regex = RegexValidator(
        regex=r'^\d{9,15}$', 
        message="Phone number must be between 9 and 15 digits."
    )

class Country_Codes(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    calling_code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.country_name} ({self.calling_code})"
    
    class Meta:
        ordering = ['calling_code']
        
class State(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name
        
GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Others')
    ]

class UserManager(BaseUserManager):
    def create_user(self, email=None, phone_number=None, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError('Either email or phone number must be provided')

        # Normalize the email if provided
        if email:
            email = self.normalize_email(email)

        # Handle phone number validation if provided and not a superuser
        if phone_number and not extra_fields.get('is_superuser'):
            full_number = f"{extra_fields.get('country_code')}{phone_number}"
            try:
                parsed_number = phonenumbers.parse(full_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number.")
                phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            except phonenumbers.NumberParseException:
                raise ValidationError("Invalid phone number format.")

        # Create and return the user object
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if email is None:
            raise ValueError('Superuser must have an email address.')

        return self.create_user(email=email, phone_number=phone_number, password=password, **extra_fields)



class User(AbstractBaseUser,PermissionsMixin):
     
     # common fields for any staff's
     created_at = models.DateTimeField(auto_now_add=True)
     full_name=models.CharField(max_length=250)
     phone_number=models.CharField(max_length=15,validators=[phone_regex],null=True,blank=True,unique=True)
     date_of_birth=models.DateField(null=True, blank=True)
     address=models.CharField(max_length=500,null=True,blank=True)
     gender=models.CharField(max_length=16,choices=GENDER_CHOICES,null=True,blank=True)
     email = models.EmailField(unique=True, null=True, blank=True)
     age=models.CharField(max_length=4,null=True,blank=True)
     watsapp_number=models.CharField(max_length=15,blank=True,null=True)
     district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
     state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
     joining_date = models.DateField(null=True,blank=True)
     
     # super user or other staffs
     is_staff=models.BooleanField(default=False)
     is_superuser=models.BooleanField(default=False)
     
     # teachers and supporting staffs
     is_librarian=models.BooleanField(default=False)
     is_teaching_staff=models.BooleanField(default=False)
     
     objects = UserManager()
     REQUIRED_FIELDS = []
     USERNAME_FIELD = 'email'  
     
     groups = models.ManyToManyField(
        Group,
        related_name='app1_user_groups',  # Add a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Override user_permissions field with a unique related_name
     user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='app1_user_permissions'  # Add a unique related_name
    )
    
     def __str__(self):
        return self.email if self.email else self.phone_number
    
    #  def has_perm(self, perm, obj=None):
    #      if self.is_admin:
    #          return True
    #     return super().has_perm(perm, obj)
    
    #  def has_module_perms(self, app_label):
    #     return self.is_admin
    
     def has_perm(self, perm, obj=None):
      if self.is_superuser:
        return True  # Grant full permissions for admins
      return super().has_perm(perm, obj)

     def has_module_perms(self, app_label):
      if self.is_superuser:
        return True  # Admins have permissions to all apps
      return super().has_module_perms(app_label)

    
    
GRADE_CHOICE=[
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
]
class GradeOfStudents(models.Model):
    grades=models.CharField(max_length=20,choices=GRADE_CHOICE)



SECOND_LANGUAGE_CHOICE=[
    ('hindi','Hindi'),
    ('malayalam','Malayalam'),
    ('arabic','Arabic'),
    ('sanskrit','SansKrit')
]

class StudentDetails(models.Model):
    auto_id=models.AutoField(primary_key=True)
    student_id=models.CharField(max_length=20, unique=True, editable=False, blank=True)
    full_name=models.CharField(max_length=250)
    date_of_birth=models.DateField(null=True, blank=True)
    
    profile_image=models.ImageField(upload_to='s-student-profile-images/', null=True, blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    place=models.CharField(max_length=100,null=True,blank=True)
    father_name=models.CharField(max_length=60,null=True,blank=True)
    mother_name=models.CharField(max_length=80,null=True,blank=True)
    father_ph= models.CharField(max_length=15,validators=[phone_regex],null=True,blank=True)
    country_code = models.ForeignKey(Country_Codes, on_delete=models.SET_NULL, null=True, blank=True)
    gender=models.CharField(max_length=16,choices=GENDER_CHOICES,null=True,blank=True)
    guardian=models.CharField(max_length=100,null=True,blank=True)
    
    joining_date = models.DateField(null=True,blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    educational_project=models.CharField(max_length=17,choices=[('english_medium','English Medium'),('malayalam_medium','Malayalam Medium')])
    previous_school_name=models.CharField(max_length=200,null=True,blank=True)
    grade=models.ForeignKey(GradeOfStudents,on_delete=models.SET_NULL,null=True,blank=True)  #student's class 
    second_language=models.CharField(max_length=10,choices=SECOND_LANGUAGE_CHOICE)
    emergency_contact=models.CharField(max_length=10, validators=[phone_regex],null=True, blank=True)
    watsapp_number=models.CharField(max_length=15,null=True,blank=True)
    total_payable=models.DecimalField(max_digits=15,default='15000',null=True,blank=True,editable=False,decimal_places=2)
    
    
    def save(self,*args,**kwargs):
        #generate the student ID 
        if not self.student_id:
            self.student_id=f'ST{str(uuid.uuid4())[:5].upper()}' # Format: ST{uuid}
        
        super(StudentDetails, self).save(*args,**kwargs)
        
    def __str__(self):
            return self.student_id
        
        
        
PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
      ]
    
PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    

class StudentFees(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=15,default='15000',decimal_places=2)
    signature = models.CharField(max_length=256, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    balance_amount=models.DecimalField(max_digits=17,editable=False,decimal_places=2,null=True,blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES,default='cash')
    payment_date = models.DateTimeField(default=timezone.now)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    account_holder_name = models.CharField(max_length=50,null=True,blank=True)
    bank_name = models.CharField(max_length=50,null=True,blank=True)
    bank_branch = models.CharField(max_length=50,null=True,blank=True)
    account_number = models.CharField(max_length=50,null=True,blank=True)
    ifsc_code = models.CharField(max_length=50,null=True,blank=True)
    supporting_documents = models.FileField(upload_to='payment-request/', blank=True, null=True)
    
    
    
    def save(self, *args, **kwargs):
            super(StudentFees, self).save(*args, **kwargs)
    # Get total paid amount so far for the student (excluding current payment)
            total_paid = StudentFees.objects.filter(student=self.student).aggregate(total=models.Sum('amount_paid'))['total'] or 0

           # Calculate the updated balance amount
            self.balance_amount = self.total_amount - total_paid

           # Update the student's total_payable field
            self.student.total_payable = self.balance_amount
            self.student.save()

            # Prevent negative balance
            if self.balance_amount < 0:
                raise ValueError("Total amount paid cannot exceed the total amount due.")
           
            # Update student's total_payable field
            # Save the updated balance amount
            super(StudentFees, self).save(update_fields=['balance_amount'])
            self.student.save()

           
         

             
        
    def __str__(self):
        return f'{self.amount_paid} payed by {self.student.full_name}'  

        
        
class Staff(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='staff')
    qualification=models.CharField(max_length=120,null=True,blank=True)
    certification=models.ImageField(upload_to='s-staff-certificate-images/', blank=True)
    profile_img=models.ImageField(upload_to='s-staff-profile-images/', null=True, blank=True)
    experience=models.CharField(max_length=50,null=True,blank=True)
    about=models.CharField(max_length=200,null=True,blank=True)
    staff_id=models.CharField(max_length=80,unique=True,editable=False,blank=True, primary_key=True)
    
    # office staff types
    is_administrative=models.BooleanField(default=False)
    is_accountant=models.BooleanField(default=False)
    is_clerk=models.BooleanField(default=False)
    is_IT_administrator=models.BooleanField(default=False)
    
    # Genarate ID for each staff excluding Librarian and Teaching Staff
    def save(self,*args,**kwargs):
        if self.is_administrative==True:
            self.staff_id=f'ADST{self.user.id}' #format ADST{ID} ID for Administrative
        elif self.is_accountant==True:
            self.staff_id=f'AC{self.user.id}' #format AC{ID} ID for Accountant
        elif self.is_clerk==True:
            self.staff_id=f'CL{self.user.id}' #format CL{ID} ID for Clerk
        elif self.is_IT_administrator==True:
            self.staff_id=f'ITADST{self.user.id}' #format ITADST{ID} ID for IT Administrative
        super(Staff, self).save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.user.full_name} {self.staff_id}'  
    

# difrent type of teachers
TEACHERS_POSITION=[
    ('prt','PRT'), 
    ('tgt','TGT'), 
    ('pgt','PGT'), # Post graduate teacher
    ('pe','PE')   # Physical education teacher
]


class Teachers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='teacher')
    qualification=models.CharField(max_length=120,null=True,blank=True)
    certifiation=models.ImageField(upload_to='s-teacher-certificate-images/', blank=True,null=True)
    profile_img=models.ImageField(upload_to='s-teacher-profile-images/', null=True, blank=True)
    experience=models.CharField(max_length=50,null=True,blank=True)
    teachers_id=models.CharField(max_length=100,unique=True,editable=False,blank=True, primary_key=True)
    grade=models.ForeignKey(GradeOfStudents,on_delete=models.CASCADE,null=True,blank=True)
    teaching_position=models.CharField(max_length=20,choices=TEACHERS_POSITION,null=True,blank=True)
    specialised_subjects=models.CharField(max_length=90,null=True,blank=True)
    teaching_license=models.CharField(max_length=80,null=True,blank=True)
    about=models.CharField(max_length=200,null=True,blank=True)
   
        
    def save(self, *args, **kwargs):
        #generate the teachers ID 
      
        if not self.teachers_id:
            self.teachers_id=f'TE{self.user.id}' # Format: TE{id}
        super(Teachers, self).save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.user.full_name}{self.teachers_id}'
    
    
        

    
BOOK_STATUS=[
    ('stock_out','Stock Out'),
    ('stock_in','Stock In'),
    ('taken','Taken')
]
    
BOOK_TYPE=[
    ('story','Story'),
    ('poem','Poem'),
    ('short_story','Short Strory'),
    ('novel','Novel'),
    ('drama','Drama')
]

class LibraryResourses(models.Model):
    book_id=models.AutoField(primary_key=True,unique=True)
    book_name=models.CharField(max_length=80,null=True,blank=True)
    book_type=models.CharField(max_length=20,null=True,blank=True,choices=BOOK_TYPE)
    author=models.CharField(max_length=30,null=True,blank=True)
    language=models.CharField(max_length=30,null=True,blank=True)
    status=models.CharField(choices=BOOK_STATUS,max_length=10)
    
    def __str__(self):
        return f'{self.book_name} by {self.author}'


class Librarian(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='librarian')
    qualification=models.CharField(max_length=120,null=True,blank=True)
    certification=models.ImageField(upload_to='s-librarian-certificate-images/', blank=True)
    profile_img=models.ImageField(upload_to='s-librarian-profile-images/', null=True, blank=True)
    experience=models.CharField(max_length=50,null=True,blank=True)

    id_of_librarian=models.CharField(max_length=100,unique=True,editable=False,blank=True,null=True)
    # books=models.ForeignKey(Library,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        #generate the teachers ID 
        if not self.id_of_librarian:
            self.id_of_librarian=f'LIB{self.user.id}' # Format: TE{id}
        super(Librarian, self).save(*args,**kwargs)
    
    def __str__(self):
        return f'{self.id_of_librarian}'
    

class Library(models.Model):
    book=models.ForeignKey(LibraryResourses,on_delete=models.DO_NOTHING)
    borrow_date=models.DateField()
    return_date=models.DateField()
    students=models.ForeignKey(StudentDetails,on_delete=models.DO_NOTHING)
    librarian=models.ForeignKey(Librarian,on_delete=models.CASCADE,null=True,blank=True)
    library_id=models.CharField(max_length=90,blank=True,null=True,unique=True)
    
    def save(self,*args,**kwargs):
        #generate the library ID 
        if not self.library_id:
            self.library_id=f'{str(uuid.uuid4())[:5].upper()}' 
        
        super(Library, self).save(*args,**kwargs)
    
    
    def __str__(self):
        return f'{self.book.book_name} borrowed by {self.students.full_name}'
    
    
class Admin(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin')
    qualification=models.CharField(max_length=120,null=True,blank=True)
    certifiation=models.ImageField(upload_to='s-admin-certificate-images/', blank=True)
    profile_img=models.ImageField(upload_to='s-admin-profile-images/', null=True, blank=True)
    experience=models.CharField(max_length=50,null=True,blank=True)
    role=models.CharField(max_length=25,null=True,blank=True)
    

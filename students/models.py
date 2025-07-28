from django.db import models
from django.contrib.auth.models import User
from svadmin.models import Company 

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    profilepic = models.ImageField(upload_to='profilepics/')
    dob = models.DateField()
    paddress = models.TextField()
    caddress = models.TextField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="eligible_students", null=True
    )
    def __str__(self):
        return self.name

# class AptitudeTestResult(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     date = models.DateField()
#     venue = models.CharField(max_length=100)
#     status = models.CharField(max_length=15, choices=[('pass', 'Pass'), ('fail', 'Fail'), ('not_appeared', 'Not Appeared')])

#     def __str__(self):
#         return f"{self.student.name} - {self.company.name} - {self.date}"

class Academic(models.Model):
    COURSE_CHOICES = [
        ('10th', '10th'),
        ('12th', '12th'),
        ('bcom', 'BCom'),
        ('bca', 'BCA'),
        ('mca', 'MCA'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    sem = models.CharField(max_length=10, blank=True, null=True)
    cgpa = models.FloatField(blank=True, null=True)
    backlog = models.IntegerField(blank=True, null=True)
    marks = models.FloatField(blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return self.student.name
    

    from students.models import Student
from svadmin.models import Company

class StudentCompanyAssociation(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='company_associations')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='student_associations')
    test_status = models.CharField(max_length=15, choices=[('pass', 'Pass'), ('fail', 'Fail'), ('not_appeared', 'Not Appeared')], default='not_appeared')
    
    def __str__(self):
        return f"{self.student.name} - {self.company.name}"
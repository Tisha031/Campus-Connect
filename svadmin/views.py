from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import EmailContent
from students.models import Student,Academic, StudentCompanyAssociation
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .forms import CompanyForm
from .models import Company

from django.conf import settings

from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
# from students.models import AptitudeTestResult

from django.shortcuts import render, get_object_or_404
from svadmin.models import Company, EmailContent

@staff_member_required
def svadmin(request):
    noOfStaff = User.objects.filter(is_staff=True, is_superuser=False).count()
    noOfEmailContent = EmailContent.objects.all().count()
    noOfComapny = Company.objects.all().count()
    noOfStudents = User.objects.filter(
        is_staff=False, is_superuser=False).count()

    infoCards = [
        {
            'title': 'Staff',
            'value': noOfStaff,
            'url': 'generatestaff'
        },
        {
            'title': 'Email Content',
            'value': noOfEmailContent,
            'url': 'emailcontent'
        },
        {
            'title': 'Students',
            'value': noOfStudents,
            'url': 'allstudents'
        },
        {
            'title': 'Company',
            'value': noOfComapny,
            'url': 'company'
        }
    ]
    context = {
        'infoCards': infoCards
    }
    return render(request, 'svadmin/home.html', context)


@staff_member_required
def generatestaff(request):
    getStaff = User.objects.filter(is_staff=True, is_superuser=False)
    print("Staff: ", getStaff)
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if name == "" or email == "" or username == "" or password == "" or cpassword == "":
            messages.error(request, "All fields are required")
            return redirect('generatestaff')
        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('generatestaff')
        if len(password) < 6:
            messages.error(request, "Password must be atleast 6 characters")
            return redirect('generatestaff')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('generatestaff')
        staff = User.objects.create_user(first_name=name,
                                         username=username, email=email, password=password)
        staff.is_staff = True
        staff.save()
        messages.success(request, "Staff added successfully")
        return redirect('generatestaff')
    return render(request, 'svadmin/generatestaff.html', {'getStaff': getStaff})

@staff_member_required
def emailcontent(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        venue = request.POST.get('venue')
        date = request.POST.get('date')
        body = request.POST.get('body')
        company_id = request.POST.get('company-id')  # Get company id from dropdown

        if not all([subject, venue, date, body, company_id]):
            messages.error(request, "All fields are required")
            return redirect('emailcontent')

        company = get_object_or_404(Company, id=company_id)  # Get the company by ID

        # Create the email content object and associate it with the selected company
        email_content = EmailContent(
            subject=subject,
            venue=venue,
            date=date,
            body=body,
            company=company,
        )
        email_content.save()

        # Optionally, associate eligible students if needed, e.g., for email distribution
        eligible_students = Student.objects.all()  # You can filter eligible students based on conditions
        email_content.eligible_students.set(eligible_students)  # Link the students to the email content
        email_content.save()

        messages.success(request, "Email content saved successfully.")
        return redirect('emailcontent')

    # Fetch all companies to display in the dropdown
    companies = Company.objects.all()  # Fetch all companies
    getEmailContent = EmailContent.objects.all()  # Fetch existing email content to display if any

    return render(request, 'svadmin/emailcontent.html', {
        'companies': companies,  # Pass companies to the template for the dropdown
        'getEmailContent': getEmailContent,  # Pass existing email content for display
    })

@staff_member_required
def allstudents(request):
    student = User.objects.filter(
        is_staff=False, is_superuser=False)
    studentDetails = Student.objects.filter(user__in=student)
    return render(request, 'svadmin/allstudents.html', {'studentDetails': studentDetails})

@staff_member_required
def student_detail(request, username):  # Change pk to username
    student = get_object_or_404(Student, user__username=username)  # Use username to fetch student
    academic_details = Academic.objects.filter(student=student)  # Fetch related academic details

    context = {
        'student': student,
        'academic_details': academic_details,
    }
    return render(request, 'svadmin/student_detail.html', context)

@staff_member_required
def company(request):
    getCompany = Company.objects.all()  # Fetch all companies

    # Handle form submission
    if request.method == 'POST':
        # Collect form data safely within the POST block
        name = request.POST.get('name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Validate required fields
        if not all([name, address, email, phone]):
            messages.error(request, "All fields are required.")
            return redirect('company')

        # Save the company details
        new_company = Company(name=name, address=address, email=email, phone=phone)
        new_company.save()

        messages.success(request, "Company added successfully.")
        return redirect('company')

    # Render the template with existing company data
    return render(request, 'svadmin/company.html', {'getCompany': getCompany})
# @staff_member_required
# def view_eligible_students(request, test_result_id):
#     test_result = get_object_or_404(AptitudeTestResult, id=test_result_id)
#     students = AptitudeTestResult.objects.filter(company=test_result.company)  # Fetch students related to the company

#     if request.method == 'POST':
#         for student in students:
#             status = request.POST.get(f'status-{student.student.id}')
#             if status:
#                 # Logic to send email based on status
#                 if status == 'pass':
#                     email_body = f"Congratulations {student.student.name}, you have passed the aptitude test for {test_result.company.name}!"
#                 elif status == 'fail':
#                     email_body = f"Keep going, {student.student.name}. Work hard for the next opportunity!"
#                 elif status == 'not_appeared':
#                     email_body = f"Dear {student.student.name}, please inform the department regarding your absence in the aptitude test."

#                 # Send email logic here
#                 email_message = EmailMessage(
#                     subject=f"Test Result for {test_result.company.name}",
#                     body=email_body,
#                     from_email=settings.EMAIL_HOST_USER,
#                     to=[student.student.user.email]
#                 )
#                 email_message.send()

#         messages.success(request, "Emails sent successfully.")
#         return redirect('testresults')

#     return render(request, 'svadmin/view_eligible_students.html', {'test_result': test_result, 'students': students})

def test_results(request):
    companyDetails = Company.objects.all()  # or filter specific companies
    return render(request, 'svadmin/testresults.html', {'companyDetails': companyDetails})

from django.shortcuts import render, get_object_or_404
from .models import Company
from django.db import transaction

@staff_member_required
def company_detail(request, id):
    # Fetch the company details
    company = get_object_or_404(Company, id=id)

    # Fetch associated students via the StudentCompanyAssociation model
    student_associations = StudentCompanyAssociation.objects.filter(company=company)

    # Ensure that if no students are associated with the company, it displays a message
    if not student_associations.exists():
        messages.warning(request, f"No students associated with {company.name}. Please ensure students are linked correctly.")

    if request.method == "POST":
        for association in student_associations:
            # Get the updated status for each student
            status = request.POST.get(f'status-{association.id}')
            if status and association.test_status != status:
                association.test_status = status
                association.save()

                # Send appropriate email based on status
                student_email = association.student.user.email
                if status == 'pass':
                    email_subject = "Congratulations!"
                    email_body = f"Dear {association.student.name},\n\nCongratulations on passing the test at {company.name}!"
                elif status == 'fail':
                    email_subject = "Better Luck Next Time"
                    email_body = f"Dear {association.student.name},\n\nWork hard and prepare for future opportunities. Good luck!"
                elif status == 'not_appeared':
                    email_subject = "Test Attendance Required"
                    email_body = f"Dear {association.student.name},\n\nPlease inform the department about your absence at the test conducted by {company.name}."

                # Send email
                email_message = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [student_email],
                )
                email_message.send()

        messages.success(request, "Test results updated and emails sent successfully.")
        return redirect('company_detail', id=company.id)

    context = {
        'company': company,
        'student_associations': student_associations,
    }
    return render(request, 'svadmin/company_detail.html', context)

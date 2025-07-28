from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from students.models import Student, Academic
from django.db.models import Q, Sum, Subquery, OuterRef, F
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from svadmin.models import EmailContent
from svadmin.models import Company

from students.models import StudentCompanyAssociation



def staff(request):
    user = request.user
    filterUser = User.objects.get(username=user)
    emailSubjectForStaff = EmailContent.objects.all()
    companies = Company.objects.all()  # Fetch all companies for the dropdown

    latest_academic_records = Academic.objects.filter(student=OuterRef('pk')).order_by('-sem')

    students = Student.objects.annotate(
        latest_academic_record_id=Subquery(latest_academic_records.values('id')[:1]),
        student_name=F('user__first_name'),
        email=F('user__email'),
    )

    latest_academic_records = Academic.objects.filter(
        id__in=Subquery(students.values('latest_academic_record_id')))

    students = students.annotate(
        total_backlogs=Sum('academic__backlog'),
        current_cgpa=Subquery(latest_academic_records.filter(student=OuterRef('pk')).values('cgpa')[:1])
    )

    filter_applied = False
    selected_company = None

    if request.method == 'POST':
        filter_applied = True

        # Company Selection
        selected_company_id = request.POST.get('company')
        if selected_company_id:
            try:
                selected_company = Company.objects.get(id=selected_company_id)
            except Company.DoesNotExist:
                messages.error(request, "Invalid company selected.")
                return redirect('staff')

        # Email Sending Logic
        if 'send-email' in request.POST:
            emailSubjectfromStaff = request.POST.get('email-subject')
            try:
                emailContentFromDB = EmailContent.objects.get(subject=emailSubjectfromStaff)
            except EmailContent.DoesNotExist:
                messages.error(request, "Invalid email subject selected.")
                return redirect('staff')

            formatted_date = emailContentFromDB.date.strftime('%d-%m-%Y %H:%M:%S')
            email_body = f"""<p>{emailContentFromDB.body}</p>
                             <p>Date: {formatted_date}</p>
                             <p>Location: {emailContentFromDB.venue}</p>"""
            emailtosend = EmailMessage(
                emailContentFromDB.subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [s.email for s in students]
            )
            emailtosend.content_subtype = "html"
            emailtosend.send()

            # Store eligible students with selected company in `StudentCompanyAssociation`
            if selected_company:
                for student in students:
                    StudentCompanyAssociation.objects.create(
                        student=student,
                        company=selected_company
                    )
            messages.success(request, "Email sent successfully and students linked to the company.")
            return redirect('staff')

        # Filtering Logic
        else:
            backlogsCondition = request.POST.get('backlogs-condition')
            backlogs = request.POST.get('backlogs')
            cgpaCondition = request.POST.get('cgpa-condition')
            cgpa = request.POST.get('cgpa')

            backlogsConditionQ = Q(total_backlogs__gt=backlogs) if backlogsCondition == 'greater' else Q(
                total_backlogs__lt=backlogs) if backlogsCondition == 'lesser' else Q(total_backlogs=backlogs)
            cgpaConditionQ = Q(current_cgpa__gt=cgpa) if cgpaCondition == 'greater' else Q(
                current_cgpa__lt=cgpa) if cgpaCondition == 'lesser' else Q(current_cgpa=cgpa)
            students = students.filter(backlogsConditionQ, cgpaConditionQ)

    return render(request, "staff/filterstudents.html", {
        "user": filterUser,
        "students": students,
        'emailSubjectForStaff': emailSubjectForStaff,
        'filter_applied': filter_applied,
        'companies': companies,
        'selected_company': selected_company,
    })

def viewcompanydetails(request):
    getCompany = Company.objects.all()  # Fetch all companies

    # Render the template with existing company data
    return render(request, 'staff/viewcompanydetails.html', {'getCompany': getCompany})
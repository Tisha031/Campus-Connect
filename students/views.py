from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from urllib.parse import unquote
from .models import Student, Academic
from django.contrib.auth.models import User


@login_required
def home(request):
    user = request.user
    try:
        userdetails = Student.objects.get(user=user)
    except:
        userdetails = None
    return render(request, 'students/home.html', {'user': user, 'userdetails': userdetails})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        profilepic = request.FILES['profilepic']

        if profilepic.size > 2 * 1024 * 1024:
            messages.warning(
                request, "The maximum file size that can be uploaded is 2MB")
            return redirect('profile')
        else:
            fs = FileSystemStorage(
                location='students/static/students/images/userspic')
            filename = fs.save(profilepic.name, profilepic)
            profilepicurl = unquote(fs.url(filename))
        dob = request.POST.get('dob')
        paddress = request.POST.get('paddress')
        caddress = request.POST.get('caddress')

        # Update or create the Student instance
        student, created = Student.objects.update_or_create(
            user=user,
            defaults={
                'name': name,
                'mobile': mobile,
                'pincode': pincode,
                'profilepic': profilepicurl,
                'dob': dob,
                'paddress': paddress,
                'caddress': caddress,
            }
        )
        messages.success(request, "Profile updated successfully")
        return redirect('profile')
    try:
        userdetails = Student.objects.get(user=user)
    except:
        userdetails = None
    return render(request, 'students/profile.html', {'user': user, 'userdetails': userdetails})

@login_required
def academicdetails(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    academicdetails = Academic.objects.filter(user=user)
    if request.method == 'POST':
        course = request.POST.get('course')
        if student is not None:
            if course in ['bca', 'mca', 'bcom']:
                sem = request.POST.get('semester')
                backlog = request.POST.get('backlogs')
                cgpa = request.POST.get('cgpa')
                academic, created = Academic.objects.update_or_create(
                    user=user,
                    student=student,
                    course=course,
                    defaults={
                        'sem': sem,
                        'backlog': backlog,
                        'cgpa': cgpa,
                    }
                )
            else:
                marks = request.POST.get('marks')
                certificate = request.FILES.get('certificate')
                academic, created = Academic.objects.update_or_create(
                    user=user,
                    student=student,
                    course=course,
                    defaults={
                        'marks': marks,
                        'certificate': certificate,
                    }
                )
            messages.success(request, "Academic details updated successfully")
            return redirect('academicdetails')
        else:
            messages.warning(request, "Please fill the profile details first")
            return redirect('profile')
    return render(request, 'students/academicdetails.html', {'academicdetails': academicdetails})
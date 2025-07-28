from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse


def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser is True:
            return redirect('svadmin')
        elif request.user.is_staff is True:
            return redirect('staff')
        elif request.user.is_active is True:
            # TODO: Before redirecting to home, check if user is active or not
            return redirect('home')
        else:
            messages.error(request, "Please activate your account")
            return redirect('login')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)
                return redirect('svadmin')
            elif user.is_staff:
                auth_login(request, user)
                return redirect('staff')
            else:
                auth_login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['cpassword']

        if email == "" or password == "" or confirmPassword == "":
            messages.error(request, "All fields are required")
            return redirect('register')
        if len(password) < 6:
            messages.error(request, "Password must be atleast 6 characters")
            return redirect('register')
        if password != confirmPassword:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        user = get_user_model().objects.create_user(
            username=email, email=email, password=password, is_active=False)
        user.save()

        token = default_token_generator.make_token(user)

        email_subject = "Activate your account"
        email_body = render_to_string('accounts/activate.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token
        })
        # TODO: Sending invalid token
        to_email = email
        emailtosend = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [to_email]
        )
        emailtosend.content_subtype = "html"
        emailtosend.send()
        messages.success(
            request, "Account created successfully. Please check your email to activate your account")
        return redirect('login')
    return render(request, 'accounts/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, "Thank you for your email confirmation. Now you can login your account.")
            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return HttpResponse('Activation link is invalid!')


def reset(request):
    return render(request, 'accounts/reset.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')

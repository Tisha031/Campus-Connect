from django.db import models
from django.apps import apps



class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def get_eligible_students(self):
        from svadmin.models import EmailContent  # Avoid circular import
        from students.models import Student
        return Student.objects.filter(email_contents__company=self).distinct()

    def __str__(self):
        return self.name


class EmailContent(models.Model):
    subject = models.CharField(max_length=100)
    date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    body = models.TextField()
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="email_contents", null=True
    )
    eligible_students = models.ManyToManyField(
    'students.Student', related_name="email_contents", blank=True
)


    def __str__(self):
        return self.subject


# Generated by Django 5.0.3 on 2024-12-04 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_delete_aptitudetestresult'),
        ('svadmin', '0006_delete_eligiblestudent'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='svadmin.company'),
        ),
    ]

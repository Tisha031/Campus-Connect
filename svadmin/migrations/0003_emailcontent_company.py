# Generated by Django 5.0.3 on 2024-11-28 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svadmin', '0002_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailcontent',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='email_contents', to='svadmin.company'),
        ),
    ]

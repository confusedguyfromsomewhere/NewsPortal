# Generated by Django 4.2.1 on 2023-05-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newspaper', '0003_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='message',
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]

# Generated by Django 4.2.14 on 2024-07-25 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0015_auto_20220526_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='coin',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('Approved', 'Approved'), ('Declined', 'Declined'), ('Pending', 'Pending')], default='Pending', max_length=20),
        ),
    ]

# Generated by Django 3.0.5 on 2022-05-23 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20220309_1302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined']},
        ),
        migrations.AlterField(
            model_name='user',
            name='_wallet_address',
            field=models.CharField(help_text='BEP20 address', max_length=100, null=True),
        ),
    ]
# Generated by Django 5.0.2 on 2024-04-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profileuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileuser',
            name='addless_line_1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='addless_line_2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='country',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='userProfilePic'),
        ),
        migrations.AlterField(
            model_name='profileuser',
            name='state',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
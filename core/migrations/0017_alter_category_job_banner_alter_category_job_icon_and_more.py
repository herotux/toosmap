# Generated by Django 5.1.5 on 2025-02-13 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_remove_user_district_user_district_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category_job',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='media/categories/banners/'),
        ),
        migrations.AlterField(
            model_name='category_job',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='media/categories/icons/'),
        ),
        migrations.AlterField(
            model_name='category_job',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/categories/images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_code',
            field=models.CharField(default='8185097596', max_length=10, unique=True),
        ),
    ]

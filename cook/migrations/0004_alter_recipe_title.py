# Generated by Django 4.2.3 on 2023-10-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0003_alter_community_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
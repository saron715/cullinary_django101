# Generated by Django 4.2.3 on 2023-10-15 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cook', '0002_alter_recipe_cuisine_type_alter_recipe_likes_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='community',
            unique_together={('name', 'cuisine_type')},
        ),
    ]

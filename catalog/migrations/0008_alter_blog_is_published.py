# Generated by Django 5.1 on 2024-08-20 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_rename_publication_attribute_blog_is_published"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="is_published",
            field=models.BooleanField(default=True, verbose_name="опубликовано"),
        ),
    ]

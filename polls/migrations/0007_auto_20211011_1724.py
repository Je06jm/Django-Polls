# Generated by Django 3.2.7 on 2021-10-11 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0006_auto_20211011_1712"),
    ]

    operations = [
        migrations.AlterField(
            model_name="option",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]

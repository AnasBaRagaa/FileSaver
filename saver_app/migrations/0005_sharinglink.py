# Generated by Django 4.0.1 on 2022-01-27 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('saver_app', '0004_alter_data_file_alter_data_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharingLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='saver_app.data')),
            ],
        ),
    ]

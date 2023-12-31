# Generated by Django 3.1.2 on 2021-10-24 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('description', models.TextField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='photos.category')),
            ],
            options={
                'verbose_name': 'Broker',
                'verbose_name_plural': 'Broker',
            },
        ),
    ]

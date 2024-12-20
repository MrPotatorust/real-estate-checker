# Generated by Django 5.1.1 on 2024-11-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField(null=True)),
                ('sq_m', models.FloatField(null=True)),
                ('img', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=10)),
                ('rentable', models.BooleanField(null=True)),
                ('property_type', models.CharField(max_length=100, null=True)),
                ('site', models.IntegerField()),
                ('datetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'property_listings_merged',
            },
        ),
    ]

# Generated by Django 3.0.6 on 2020-05-14 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lemonade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('position', models.CharField(max_length=40)),
                ('commission_percentage', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('lemonade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sales.Lemonade')),
                ('sales_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sales.Staff')),
            ],
        ),
    ]

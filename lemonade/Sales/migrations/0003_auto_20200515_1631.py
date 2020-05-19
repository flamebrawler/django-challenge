# Generated by Django 3.0.6 on 2020-05-15 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0002_auto_20200514_0108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='lemonade',
        ),
        migrations.CreateModel(
            name='LemonadeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('lemonade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sales.Lemonade')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='lemonade',
            field=models.ManyToManyField(to='Sales.LemonadeSet'),
        ),
    ]

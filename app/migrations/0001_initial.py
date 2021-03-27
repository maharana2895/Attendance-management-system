# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('is_leave', models.BooleanField(default=False)),
                ('detail', models.TextField(default='无')),
                ('leave_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ClassInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('detail', models.TextField(default='无', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ExamContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('date', models.DateField(auto_now=True)),
                ('state', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateField(blank=True, null=True)),
                ('end_time', models.DateField(blank=True, null=True)),
                ('explain', models.TextField(default='无', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='MajorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(auto_now=True)),
                ('head', models.TextField(max_length=200)),
                ('content', models.TextField(max_length=500)),
                ('level', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('studentNum', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=64)),
                ('username', models.CharField(max_length=15)),
                ('nickname', models.CharField(max_length=30, null=True)),
                ('hobby', models.CharField(max_length=30, null=True)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.IntegerField(default=1)),
                ('phone', models.CharField(max_length=11)),
                ('motto', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('cid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ClassInfo')),
                ('major', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.MajorInfo')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserType'),
        ),
        migrations.AddField(
            model_name='notice',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserInfo'),
        ),
        migrations.AddField(
            model_name='leave',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserInfo'),
        ),
        migrations.AddField(
            model_name='exam',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ExamContent'),
        ),
        migrations.AddField(
            model_name='exam',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserInfo'),
        ),
        migrations.AddField(
            model_name='attendence',
            name='stu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserInfo'),
        ),
    ]

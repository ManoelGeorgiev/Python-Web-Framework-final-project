# Generated by Django 4.0.3 on 2022-04-11 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_comment_options_commentlikebutton'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.tag'),
            preserve_default=False,
        ),
    ]

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        # You need to replace 'your_app_name' with the app that contains EVS_violation and EVS_reason models
        ('your_app_name', 'last_migration_file'), 
    ]

    operations = [
        migrations.CreateModel(
            name='SSIOViolationRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_id', models.IntegerField()),
                ('date_recorded', models.DateTimeField(auto_now_add=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('resolved_at', models.DateTimeField(null=True, blank=True)),
                ('resolved_by_staff_id', models.IntegerField(null=True, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('violation', models.ForeignKey(
                    to='your_app_name.EVS_violation', 
                    on_delete=django.db.models.deletion.CASCADE
                )),
                ('reason', models.ForeignKey(
                    to='your_app_name.EVS_reason', 
                    null=True,
                    blank=True,
                    on_delete=django.db.models.deletion.SET_NULL
                )),
            ],
        ),
    ]

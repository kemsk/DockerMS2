from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SSIOMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.CharField(max_length=20, unique=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('encoder', 'Encoder')], default='encoder', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('student_id', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ViolationRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('ticket_number', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('photo_proof', models.ImageField(blank=True, null=True, upload_to='violations/')),
                ('date_recorded', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_resolved', models.BooleanField(default=False)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('claimed', 'ID Claimed'), ('resolved', 'Resolved')], default='pending', max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('reason', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='evs_app.reason')),
                ('recorded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recorded_violations', to='evs_app.ssiomember')),
                ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_violations', to='evs_app.ssiomember')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evs_app.student')),
                ('violation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evs_app.violation')),
            ],
        ),
    ]

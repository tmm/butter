# Generated by Django 2.0.3 on 2018-08-20 00:49

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_subtype', models.CharField(blank=True, choices=[('SA', 'Savings'), ('CH', 'Checking'), ('CD', 'CD'), ('CC', 'Credit Card'), ('MM', 'Money Market')], max_length=2)),
                ('a_type', models.CharField(blank=True, choices=[('C', 'Credit'), ('D', 'Depository')], max_length=2)),
                ('account_id', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mask', models.CharField(blank=True, max_length=4)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('official_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
                'db_table': 'api_account',
            },
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('current', models.DecimalField(decimal_places=2, max_digits=10)),
                ('limit', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'balance',
                'verbose_name_plural': 'balances',
                'db_table': 'api_balance',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('institution_id', models.CharField(blank=True, max_length=4)),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'institution',
                'verbose_name_plural': 'institutions',
                'db_table': 'api_institution',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50), size=None)),
                ('category_id', models.CharField(blank=True, max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('name', models.CharField(blank=True, max_length=100)),
                ('payment_meta', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pending', models.BooleanField()),
                ('pending_transaction_id', models.CharField(blank=True, max_length=50)),
                ('transaction_id', models.CharField(blank=True, max_length=50)),
                ('transaction_type', models.CharField(blank=True, choices=[('SP', 'Special'), ('PL', 'Place')], max_length=2)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='api.Account')),
            ],
            options={
                'verbose_name': 'transaction',
                'verbose_name_plural': 'transactions',
                'db_table': 'api_transaction',
            },
        ),
        migrations.CreateModel(
            name='TransactionLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lon', models.FloatField(verbose_name='longitude')),
                ('lat', models.FloatField(verbose_name='latitude')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('state', models.CharField(blank=True, max_length=2)),
                ('store_number', models.CharField(blank=True, max_length=30)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'verbose_name': 'transaction location',
                'verbose_name_plural': 'transaction locations',
                'db_table': 'api_transaction_location',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_location',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.TransactionLocation'),
        ),
        migrations.AddField(
            model_name='account',
            name='balance',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Balance'),
        ),
        migrations.AddField(
            model_name='account',
            name='institution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Institution'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to=settings.AUTH_USER_MODEL),
        ),
    ]

 """
Management command to create initial data for the system
"""
from django.core.management.base import BaseCommand
from core.models import User, Company


class Command(BaseCommand):
    help = 'Create initial users and companies for the system'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating initial data...')
        
        # Create companies
        company1, created = Company.objects.get_or_create(name='Sample Company')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created company: {company1.name}'))
        else:
            self.stdout.write(f'Company already exists: {company1.name}')
        
        company2, created = Company.objects.get_or_create(name='Tech Corp')
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created company: {company2.name}'))
        else:
            self.stdout.write(f'Company already exists: {company2.name}')
        
        # Create root user
        if not User.objects.filter(username='root').exists():
            root_user = User.objects.create_user(
                username='root',
                password='root123',
                email='root@example.com',
                role='root',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS('Created root user (username: root, password: root123)'))
        else:
            self.stdout.write('Root user already exists')
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@example.com',
                role='admin',
                company=company1
            )
            self.stdout.write(self.style.SUCCESS('Created admin user (username: admin, password: admin123)'))
        else:
            self.stdout.write('Admin user already exists')
        
        # Create user1
        if not User.objects.filter(username='user1').exists():
            user1 = User.objects.create_user(
                username='user1',
                password='user123',
                email='user1@example.com',
                role='user1',
                company=company1
            )
            self.stdout.write(self.style.SUCCESS('Created user1 (username: user1, password: user123)'))
        else:
            self.stdout.write('User1 already exists')
        
        # Create additional admin for second company
        if not User.objects.filter(username='admin2').exists():
            admin2 = User.objects.create_user(
                username='admin2',
                password='admin123',
                email='admin2@example.com',
                role='admin',
                company=company2
            )
            self.stdout.write(self.style.SUCCESS('Created admin2 user (username: admin2, password: admin123)'))
        else:
            self.stdout.write('Admin2 user already exists')
        
        self.stdout.write(self.style.SUCCESS('\nInitial data creation complete!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  Root:   username=root,   password=root123')
        self.stdout.write('  Admin:  username=admin,  password=admin123')
        self.stdout.write('  User1:  username=user1,  password=user123')
        self.stdout.write('  Admin2: username=admin2, password=admin123')

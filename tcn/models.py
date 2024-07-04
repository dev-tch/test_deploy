#from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint

class Office(models.Model):
    ref = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    number_of_windows = models.IntegerField()
    counter = models.IntegerField(default=0)  # New field

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    USER_ROLES = [
        ('manager', 'Manager'),
        ('client', 'Client'),
        ('agent', 'Agent')
    ]
    role = models.CharField(max_length=10, choices=USER_ROLES, default='manager')
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True) 
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='users')

    class Meta:
        # Add unique related_name for groups and user_permissions
        default_related_name = 'custom_users'

    # Override groups and user_permissions with unique related_names
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        help_text='Specific permissions for this user.',
        related_query_name='custom_user',
    )

    def __str__(self):
        return f'{self.username} - CustomUser'

class Window(models.Model):
    number_window = models.IntegerField(primary_key=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    agent  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number_of_served_tickets = models.IntegerField(default=0)  # Default value set to zero
    def save(self, *args, **kwargs):
        if self.number_window is not None and self.number_window > self.office.number_of_windows:
            raise ValidationError('number of windows not compatible with value already defined in office')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Window {self.id} at {self.office.name} assigned to {self.agent.username}'
    
# new model to track office for client 

class CounterNotify(models.Model):
    is_enabled = models.BooleanField(default=False)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='counter_notifications')
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='counter_notifications')
    class Meta:
        constraints = [
            UniqueConstraint(fields=['client', 'office'], name='unique_client_office')
        ]
    def __str__(self):
        return f"CounterNotify: {self.client.username} - {self.office.name}"

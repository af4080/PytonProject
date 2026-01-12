from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = (
        ('manager', 'מנהל'),
        ('worker', 'עובד'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    team = models.ForeignKey(Team, on_delete=models.CASCADE,null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



    def __str__(self):
        return self.user.username

class Task(models.Model):
        STATUS_CHOICES = (
            ('new', 'חדש'),
            ('in_progress', 'בתהליך'),
            ('done', 'הושלם'),
        )

        title = models.CharField(max_length=200)
        description = models.TextField()
        due_date = models.DateField()

        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='new'
        )

        team = models.ForeignKey(Team, on_delete=models.CASCADE)

        assigned_to = models.ForeignKey(
            User,
            on_delete=models.SET_NULL,
            null=True,
            blank=True
        )

        def __str__(self):
            return self.title



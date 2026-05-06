from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Friendship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    addressee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('requester', 'addressee')
        indexes = [
            models.Index(fields=['requester']),
            models.Index(fields=['addressee']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.requester.username} -> {self.addressee.username} ({self.status})"


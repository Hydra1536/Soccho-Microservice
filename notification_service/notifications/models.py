from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPE_CHOICES = [
        ('lend_confirm', 'Lending Confirmation'),
        ('payment_received', 'Payment Received'),
        ('due_reminder', 'Due Date Reminder'),
    ]
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    payload_encrypted = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['recipient', 'is_read'])]
    
    def __str__(self):
        return f"[{self.type}] {self.recipient.username}"


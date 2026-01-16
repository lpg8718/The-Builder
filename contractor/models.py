from django.db import models
from The_Builder.models import Users as User

class ContractorProject(models.Model):
    # USER → किस user ने project बनाया
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    # BASIC DETAILS
    project_title = models.CharField(max_length=200)
    project_category = models.CharField(
        max_length=100,
        choices=[
            ("Building Construction", "Building Construction"),
            ("Road Work", "Road Work"),
            ("Interior Work", "Interior Work"),
            ("Plumbing", "Plumbing"),
            ("Electric Work", "Electric Work"),
            ("Painting", "Painting"),
        ]
    )

    # FINANCIAL DETAILS
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    payment_terms = models.CharField(
        max_length=50,
        choices=[
            ("Milestone Based", "Milestone Based"),
            ("Weekly Billing", "Weekly Billing"),
            ("Monthly Billing", "Monthly Billing"),
        ]
    )
    advance_payment = models.PositiveIntegerField(null=True, blank=True)

    # LOCATION
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    full_address = models.TextField(blank=True, null=True)

    # TIMELINE
    start_date = models.DateField()
    deadline = models.DateField()

    # REQUIREMENTS
    required_workers = models.PositiveIntegerField(null=True, blank=True)
    required_skills = models.CharField(max_length=255, blank=True, null=True)

    # DESCRIPTION
    project_description = models.TextField(blank=True, null=True)

    # FILE UPLOADS
    attachments = models.FileField(upload_to="project_files/", blank=True, null=True)

    # AUTO DETAILS
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_title


class ProjectAttachment(models.Model):
    project = models.ForeignKey(ContractorProject, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="project_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """Message model for contractor and thekedar communication"""
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="received_messages"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['receiver', 'is_read']),
        ]
    
    def __str__(self):
        return f"{self.sender.user_full_name} → {self.receiver.user_full_name}"
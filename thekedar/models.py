from django.db import models
from The_Builder.models import Users
from contractor.models import ContractorProject


class ProjectApplication(models.Model):

    # Relations
    project = models.ForeignKey(
        ContractorProject,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    applicant = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="project_applications"
    )

    # Form Fields
    experience_years = models.PositiveIntegerField()
    proposed_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    estimated_duration = models.PositiveIntegerField(
        help_text="Duration in days"
    )
    machines_equipment = models.TextField()
    why_select_you = models.TextField()

    # Application Status
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Approved", "Approved"),
            ("Rejected", "Rejected"),
        ],
        default="Pending"
    )

    # Timestamp
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "applicant")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.applicant.user_username} → {self.project.project_title}"

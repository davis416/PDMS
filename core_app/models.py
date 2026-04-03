from django.db import models

class Donor(models.Model):
    DonorID = models.AutoField(primary_key=True)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=20, blank=True, null=True)
    Address = models.TextField(blank=True, null=True)
    Preferred_Communication = models.CharField(
        max_length=10, 
        choices=[('EMAIL', 'Email'), ('PHONE', 'Phone'), ('MAIL', 'Mail')], 
        default='EMAIL'
    )
    Total_Donated = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    Propensity_Score = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.Email

class Campaign(models.Model):
    CampaignID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Target_Amount = models.DecimalField(max_digits=15, decimal_places=2)
    Start_Date = models.DateField()
    End_Date = models.DateField(db_index=True)  # indexed for active-campaign filter
    
    def __str__(self):
        return self.Name

class Donation(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('CC', 'Credit Card'),
        ('BANK', 'Bank Transfer'),
        ('CASH', 'Cash')
    ]
    
    DonationID = models.AutoField(primary_key=True)
    DonorID = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)  # indexed for filtering
    Payment_Method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    Date = models.DateTimeField(auto_now_add=True, db_index=True)  # indexed for ordering
    CampaignID = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    
    def __str__(self):
        return f"Donation {self.DonationID} - {self.Amount}"

class Volunteer(models.Model):
    VolunteerID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Skills = models.TextField(help_text="Comma-separated skills")
    CampaignID = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='volunteers')
    Hours_Worked = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.Name

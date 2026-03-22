import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core_app.models import Donor, Campaign, Donation, Volunteer
from ml_engine.model_training import train_model

class Command(BaseCommand):
    help = 'Seeds the database with mock data and trains the initial ML Model.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Seeding database...'))
        
        # Clean up old data
        Donation.objects.all().delete()
        Campaign.objects.all().delete()
        Donor.objects.all().delete()
        Volunteer.objects.all().delete()

        # 1. Create Campaigns
        c1 = Campaign.objects.create(
            Name="Annual Fund 2026",
            Target_Amount=50000.00,
            Start_Date=timezone.now().date(),
            End_Date=(timezone.now() + timedelta(days=90)).date()
        )
        c2 = Campaign.objects.create(
            Name="Disaster Relief Q1",
            Target_Amount=20000.00,
            Start_Date=(timezone.now() - timedelta(days=30)).date(),
            End_Date=(timezone.now() + timedelta(days=30)).date()
        )

        # 2. Create Donors and Donations
        payment_methods = ['CC', 'BANK', 'CASH']
        for i in range(1, 101):
            donor = Donor.objects.create(
                Email=f"donor{i}@example.com",
                Total_Donated=0.00
            )
            
            # Randomly create 1-5 donations for this donor
            num_donations = random.randint(1, 5)
            total = 0
            for _ in range(num_donations):
                amt = random.choice([25.0, 50.0, 100.0, 250.0, 500.0])
                total += amt
                Donation.objects.create(
                    DonorID=donor,
                    Amount=amt,
                    Status='COMPLETED',
                    Payment_Method=random.choice(payment_methods),
                    CampaignID=random.choice([c1, c2, None])
                )
                
                # Mock the date back in time arbitrarily
                # Note: modifying auto_now_add field needs a separate save after create
                d = Donation.objects.last()
                d.Date = timezone.now() - timedelta(days=random.randint(1, 365))
                d.save()
            
            donor.Total_Donated = total
            donor.save()

        # 3. Create Volunteers
        Volunteer.objects.create(Name="Alice Smith", Skills="Event Planning, Data Entry")
        Volunteer.objects.create(Name="Bob Jones", Skills="Marketing, Calling")

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded 100 donors and their donations.'))

        # 4. Train the AI Model
        self.stdout.write(self.style.NOTICE('Training Propensity Model...'))
        success = train_model()
        if success:
            self.stdout.write(self.style.SUCCESS('Successfully trained Propensity Model.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to train Propensity Model. Check logs.'))
            
        self.stdout.write(self.style.SUCCESS('Project setup complete! You are ready to start the server.'))

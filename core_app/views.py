import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from .models import Donor, Donation, Campaign, Volunteer

logger = logging.getLogger(__name__)

# --- Role-Based Access Control Helpers ---
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Administrators').exists()

# --- Donor Management (CRUD) ---
@login_required
@user_passes_test(is_admin)
def donor_list(request):
    donors = Donor.objects.all().order_by('-Total_Donated')
    
    # Real-time Reporting Metrics
    total_funds = Donation.objects.filter(Status='COMPLETED').aggregate(total=models.Sum('Amount'))['total'] or 0.00
    active_campaigns = Campaign.objects.filter(End_Date__gte=timezone.now().date()).count()
    total_donors = donors.count()
    
    # Retention rate
    retained_donors = Donor.objects.annotate(num_donations=models.Count('donations')).filter(num_donations__gt=1).count()
    retention_rate = (retained_donors / total_donors * 100) if total_donors > 0 else 0

    context = {
        'donors': donors,
        'total_funds': total_funds,
        'active_campaigns': active_campaigns,
        'total_donors': total_donors,
        'retention_rate': round(retention_rate, 1)
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def donor_create(request):
    from .forms import DonorForm
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = DonorForm()
    return render(request, 'donor_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(is_admin)
def donor_detail(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    donations = donor.donations.all().order_by('-Date')
    return render(request, 'donor_detail.html', {'donor': donor, 'donations': donations})

@login_required
@user_passes_test(is_admin)
def donor_update(request, pk):
    from .forms import DonorForm
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor_detail', pk=donor.pk)
    else:
        form = DonorForm(instance=donor)
    return render(request, 'donor_form.html', {'form': form, 'action': 'Update'})

@login_required
@user_passes_test(is_admin)
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        return redirect('admin_dashboard')
    return render(request, 'donor_confirm_delete.html', {'donor': donor})



# --- Donation Processing & Automated Communication ---

from django.contrib import messages

def send_receipt(donor_email, amount, donation_id):
    """Trigger official tax-compliant receipt via SMTP."""
    subject = f"Official Tax-Compliant Receipt for Donation #{donation_id}"
    message = f"Thank you for your generous donation of Ksh {amount}.\n\nThis serves as an official tax receipt for your records. No goods or services were provided in exchange for this contribution."
    try:
        send_mail(
            subject,
            message,
            'no-reply@pdms-system.org',
            [donor_email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send email to {donor_email}: {e}")

@login_required
@user_passes_test(is_admin)
@transaction.atomic
def manual_donation(request):
    """Allow administrators to manually input cash/cheque donations."""
    from .forms import ManualDonationForm
    if request.method == 'POST':
        form = ManualDonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.Status = 'COMPLETED'
            # ACID setup: save donation, then lock and update donor total
            donation.save()
            
            donor = Donor.objects.select_for_update().get(pk=donation.DonorID.pk)
            donor.Total_Donated = float(donor.Total_Donated) + float(donation.Amount)
            donor.save()
            
            # Send Receipt
            send_receipt(donor.Email, donation.Amount, donation.DonationID)
            
            messages.success(request, f"Manual donation of Ksh {donation.Amount} recorded for {donor.Email}.")
            return redirect('manual_donation')
    else:
        form = ManualDonationForm()
    
    return render(request, 'manual_donation.html', {'form': form})

def process_donation(request):
    """
    Public portal view showing active campaigns, handling donations,
    and showing donor history via email "login".
    Ensures ACID properties via @transaction.atomic.
    """
    # 1. Fetch active campaigns with progress
    campaigns = Campaign.objects.annotate(
        collected=models.Sum('donations__Amount', filter=models.Q(donations__Status='COMPLETED'))
    ).filter(End_Date__gte=timezone.now().date()).order_by('End_Date')
    
    context = {'campaigns': campaigns}

    # 2. Handle "Login" or "Donation" POST requests
    if request.method == 'POST':
        action = request.POST.get('action')
        email = request.POST.get('email')
        
        if action == 'login' and email:
            try:
                donor = Donor.objects.get(Email=email)
                context['donor_history'] = donor.donations.all().order_by('-Date')
                context['donor_email'] = email
            except Donor.DoesNotExist:
                context['error_message'] = f"No donation history found for {email}."
                
        elif action == 'donate' and email:
            amount = request.POST.get('amount')
            
            if not amount or float(amount) < 1:
                context['error_message'] = 'Minimum donation amount is Ksh 1.'
                return render(request, 'public_portal.html', context)
                
            payment_method = request.POST.get('payment_method', 'CC')
            campaign_id = request.POST.get('campaign_id')
            
            try:
                with transaction.atomic():
                    # ACID: Transaction starts here
                    donor, created = Donor.objects.get_or_create(Email=email)
                    campaign = Campaign.objects.get(pk=campaign_id) if campaign_id else None
                    
                    # Secure Processing logic (e.g. Stripe/PayPal) goes here. 
                    donation = Donation.objects.create(
                        DonorID=donor,
                        Amount=amount,
                        Status='COMPLETED',
                        Payment_Method=payment_method,
                        CampaignID=campaign
                    )
                    
                    # Update Total Donated
                    donor.Total_Donated = float(donor.Total_Donated) + float(amount)
                    donor.save()
                    
                # Trigger Automated Communication outside atomic block to ensure email fires after commit
                send_receipt(donor.Email, donation.Amount, donation.DonationID)
                
                context['success_message'] = 'Donation successful! Thank you.'
            except Exception as e:
                logger.error(f"Donation failed: {e}")
                context['error_message'] = 'Donation failed. Please try again.'
                
        elif action == 'volunteer':
            name = request.POST.get('volunteer_name')
            skills = request.POST.get('volunteer_skills')
            
            try:
                Volunteer.objects.create(
                    Name=name,
                    Skills=skills
                )
                context['success_message'] = f'Thank you for volunteering, {name}! Our team will contact you shortly.'
            except Exception as e:
                logger.error(f"Volunteer registration failed: {e}")
                context['error_message'] = 'Volunteer registration failed. Please try again.'

    return render(request, 'public_portal.html', context)


# --- Volunteer Management Module ---
@login_required
@user_passes_test(is_admin)
def volunteer_list(request):
    volunteers = Volunteer.objects.all().order_by('Name')
    return render(request, 'volunteer_dashboard.html', {'volunteers': volunteers})

@login_required
@user_passes_test(is_admin)
def volunteer_create(request):
    from .forms import VolunteerForm
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('volunteer_list')
    else:
        form = VolunteerForm()
    return render(request, 'volunteer_form.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(is_admin)
def volunteer_update(request, pk):
    from .forms import VolunteerForm
    volunteer = get_object_or_404(Volunteer, pk=pk)
    if request.method == 'POST':
        form = VolunteerForm(request.POST, instance=volunteer)
        if form.is_valid():
            form.save()
            return redirect('volunteer_list')
    else:
        form = VolunteerForm(instance=volunteer)
    return render(request, 'volunteer_form.html', {'form': form, 'action': 'Edit'})

# --- Admin User Management ---
@login_required
@user_passes_test(is_admin)
def admin_user_list(request):
    admins = User.objects.filter(is_staff=True)
    return render(request, 'admin_user_dashboard.html', {'admins': admins})

@login_required
@user_passes_test(is_admin)
def admin_user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('admin_user_list')
    else:
        form = UserCreationForm()
    return render(request, 'admin_user_form.html', {'form': form})

# --- Campaign Management ---
@login_required
@user_passes_test(is_admin)
def campaign_list(request):
    campaigns = Campaign.objects.annotate(
        collected=models.Sum('donations__Amount', filter=models.Q(donations__Status='COMPLETED'))
    ).order_by('-Start_Date')
    return render(request, 'campaign_dashboard.html', {'campaigns': campaigns})

@login_required
@user_passes_test(is_admin)
def campaign_create(request):
    from .forms import CampaignForm
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm()
    return render(request, 'campaign_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(is_admin)
def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    donors = Donor.objects.filter(donations__CampaignID=campaign, donations__Status='COMPLETED').distinct()
    collected = campaign.donations.filter(Status='COMPLETED').aggregate(total=models.Sum('Amount'))['total'] or 0.00
    
    return render(request, 'campaign_detail.html', {'campaign': campaign, 'donors': donors, 'collected': collected})

@login_required
@user_passes_test(is_admin)
def campaign_update(request, pk):
    from .forms import CampaignForm
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaign_list')
    else:
        form = CampaignForm(instance=campaign)
    return render(request, 'campaign_form.html', {'form': form, 'action': 'Update'})

@login_required
@user_passes_test(is_admin)
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        campaign.delete()
        return redirect('campaign_list')
    return render(request, 'campaign_confirm_delete.html', {'campaign': campaign})


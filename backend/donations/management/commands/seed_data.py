import random
from django.core.management.base import BaseCommand
from donations.models import DonationCampaign, Donation
from volunteers.models import VolunteerOpportunity, VolunteerApplication

class Command(BaseCommand):
    help = 'Seeds the database with initial data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        self.clear_data()
        self.seed_campaigns()
        self.seed_opportunities()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def clear_data(self):
        self.stdout.write('Clearing existing data...')
        Donation.objects.all().delete()
        DonationCampaign.objects.all().delete()
        VolunteerApplication.objects.all().delete()
        VolunteerOpportunity.objects.all().delete()

    def seed_campaigns(self):
        self.stdout.write('Seeding donation campaigns...')
        campaigns = [
            {
                'title': 'Sponsor a Child’s Education',
                'description': 'Provide a full year of schooling for an underprivileged child. Your donation covers tuition, books, and uniforms, giving them a chance for a brighter future.',
                'short_description': 'Help a child get the education they deserve.',
                'goal_amount': 5000
            },
            {
                'title': 'Clean Water for a Village',
                'description': 'Fund the construction of a well to provide clean and safe drinking water to an entire village. This project will improve health and sanitation for hundreds of people.',
                'short_description': 'Bring clean, safe drinking water to a community in need.',
                'goal_amount': 15000
            },
            {
                'title': 'Support for Homeless Shelters',
                'description': 'Help us provide essential supplies like food, blankets, and hygiene kits to local homeless shelters. Your contribution makes a direct impact on those in need.',
                'short_description': 'Provide essential supplies to homeless shelters.',
                'goal_amount': 8000
            }
        ]

        for camp_data in campaigns:
            campaign = DonationCampaign.objects.create(**camp_data)
            # Create some random donations for each campaign
            for _ in range(random.randint(5, 20)):
                Donation.objects.create(
                    campaign=campaign,
                    donor_name=f'Donor {random.randint(1, 100)}',
                    donor_email=f'donor{random.randint(1, 100)}@example.com',
                    amount=random.uniform(10, 500),
                    payment_method=random.choice(['stripe', 'paypal']),
                    payment_status='completed',
                    is_anonymous=random.choice([True, False])
                )

    def seed_opportunities(self):
        self.stdout.write('Seeding volunteer opportunities...')
        opportunities = [
            {
                'title': 'Community Garden Volunteer',
                'description': 'Help us maintain our community garden, which provides fresh produce to local families. Tasks include planting, weeding, and harvesting.',
                'short_description': 'Lend a hand in our community garden.',
                'opportunity_type': 'ongoing',
                'location': 'City Park Community Garden',
                'skills_required': 'No special skills required, just a willingness to help!',
                'time_commitment': '3 hours per week',
                'max_volunteers': 20,
                'start_date': '2025-08-10T09:00:00Z'
            },
            {
                'title': 'Annual Charity Gala Assistant',
                'description': 'Assist with the setup, registration, and coordination of our annual charity gala. This is a great opportunity to be part of a major fundraising event.',
                'short_description': 'Help make our annual charity gala a success.',
                'opportunity_type': 'one_time',
                'location': 'Grand Ballroom, City Center',
                'skills_required': 'Good communication and organizational skills.',
                'time_commitment': '8 hours on the event day',
                'max_volunteers': 50,
                'start_date': '2025-09-15T17:00:00Z'
            }
        ]

        for opp_data in opportunities:
            VolunteerOpportunity.objects.create(**opp_data)

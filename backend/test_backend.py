#!/usr/bin/env python3
"""
Test script to verify JoyWorld@WebSite Backend functionality
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test various API endpoints"""
    print("🧪 Testing JoyWorld@WebSite Backend API...")
    
    endpoints_to_test = [
        {"url": f"{BASE_URL}/api/campaigns/", "name": "Donation Campaigns"},
        {"url": f"{BASE_URL}/api/donations/", "name": "Donations"},
        {"url": f"{BASE_URL}/volunteers/api/opportunities/", "name": "Volunteer Opportunities"},
        {"url": f"{BASE_URL}/volunteers/api/applications/", "name": "Volunteer Applications"},
        {"url": f"{BASE_URL}/contact/api/messages/", "name": "Contact Messages"},
        {"url": f"{BASE_URL}/contact/api/newsletter/", "name": "Newsletter Subscriptions"},
    ]
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(endpoint["url"], timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint['name']}: OK (Status: {response.status_code})")
                data = response.json()
                if 'results' in data:
                    print(f"   📊 Found {len(data['results'])} items")
                elif isinstance(data, list):
                    print(f"   📊 Found {len(data)} items")
            else:
                print(f"⚠️  {endpoint['name']}: Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {endpoint['name']}: Connection failed - Is the server running?")
        except Exception as e:
            print(f"❌ {endpoint['name']}: Error - {str(e)}")
    
    print("\n🌐 Testing Admin Panel...")
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        if response.status_code == 200:
            print("✅ Admin panel: Accessible")
        else:
            print(f"⚠️  Admin panel: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Admin panel: Error - {str(e)}")

def test_donation_creation():
    """Test creating a donation"""
    print("\n💰 Testing Donation Creation...")
    
    donation_data = {
        "campaign": 1,  # Assuming we have a campaign with ID 1
        "donor_name": "Test Donor",
        "donor_email": "test@example.com",
        "amount": 25.00,
        "payment_method": "stripe",
        "is_anonymous": False,
        "message": "Test donation from API"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/donations/",
            json=donation_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 201:
            print("✅ Donation creation: Success")
            data = response.json()
            if 'client_secret' in data:
                print("   💳 Stripe payment intent created")
            elif 'approval_url' in data:
                print("   💳 PayPal payment created")
        else:
            print(f"⚠️  Donation creation: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Donation creation: Error - {str(e)}")

def test_contact_form():
    """Test contact form submission"""
    print("\n📧 Testing Contact Form...")
    
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "subject": "Test Contact Message",
        "message": "This is a test message from the API",
        "message_type": "general"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/contact/api/messages/",
            json=contact_data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 201:
            print("✅ Contact form: Success")
        else:
            print(f"⚠️  Contact form: Status {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Contact form: Error - {str(e)}")

if __name__ == "__main__":
    print("🚀 JoyWorld@WebSite Backend Test Suite")
    print("=" * 50)
    
    test_api_endpoints()
    test_donation_creation()
    test_contact_form()
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("📋 If you see connection errors, make sure to:")
    print("   1. Run: python manage.py runserver")
    print("   2. Keep the server running in another terminal")
    print("   3. Then run this test script again")

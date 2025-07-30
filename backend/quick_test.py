#!/usr/bin/env python3
"""Quick test to verify API endpoints are working"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("🧪 Quick Backend API Test")
print("=" * 40)

# Test campaign endpoints
try:
    response = requests.get(f"{BASE_URL}/api/campaigns/", timeout=2)
    print(f"✅ Campaigns API: {response.status_code} - Found {len(response.json())} campaigns")
except Exception as e:
    print(f"❌ Campaigns API: {e}")

# Test admin panel
try:
    response = requests.get(f"{BASE_URL}/admin/", timeout=2)
    print(f"✅ Admin Panel: {response.status_code} - Accessible")
except Exception as e:
    print(f"❌ Admin Panel: {e}")

print("\n🎯 If you see successful responses, your backend is working!")
print("📋 Next: Open http://127.0.0.1:8000/admin/ in your browser")
print("🔐 Login with: admin / (password you set earlier)")

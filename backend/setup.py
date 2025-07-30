#!/usr/bin/env python3
"""
JoyWorld@WebSite Backend Setup Script
"""

import os
import subprocess
import sys

def run_command(command, description="Running command"):
    """Run a shell command and handle errors"""
    print(f"{description}: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def setup_backend():
    """Setup the Django backend"""
    print("🚀 Setting up JoyWorld@WebSite Backend...")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        print("❌ Failed to install requirements")
        return False
    
    # Copy environment file
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            run_command("copy .env.example .env", "Creating environment file")
            print("📝 Please edit .env file with your configuration")
        else:
            print("❌ .env.example file not found")
            return False
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        print("❌ Failed to create migrations")
        return False
        
    if not run_command("python manage.py migrate", "Running migrations"):
        print("❌ Failed to run migrations")
        return False
    
    # Create superuser
    print("Creating superuser...")
    run_command("python manage.py createsuperuser", "Creating superuser")
    
    # Seed data
    if not run_command("python manage.py seed_data", "Seeding database with sample data"):
        print("⚠️ Failed to seed data, continuing anyway")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput", "Collecting static files"):
        print("⚠️ Failed to collect static files")
    
    print("✅ Backend setup complete!")
    print("📋 Next steps:")
    print("   1. Edit the .env file with your configuration")
    print("   2. Configure your payment gateways (Stripe, PayPal)")
    print("   3. Configure your email settings")
    print("   4. Run: python manage.py runserver")
    print("   5. Visit: http://localhost:8000/admin/")
    
    return True

if __name__ == "__main__":
    setup_backend()

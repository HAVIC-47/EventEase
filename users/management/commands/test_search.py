#!/usr/bin/env python
"""
Quick test to check existing users and search functionality
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Q

class Command(BaseCommand):
    help = 'Test user search functionality'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking User Database...")
        
        # Show all users
        all_users = User.objects.all()
        self.stdout.write(f"Total users in database: {all_users.count()}")
        
        for user in all_users[:10]:  # Show first 10 users
            self.stdout.write(f"- {user.username} | {user.first_name} {user.last_name} | {user.email}")
        
        if all_users.count() > 10:
            self.stdout.write(f"... and {all_users.count() - 10} more users")
        
        self.stdout.write("\n🧪 Testing Search Queries...")
        
        # Test specific searches that were failing
        test_queries = ['ami', 'faisal', 'akhi', 'alice', 'bob', 'social']
        
        for query in test_queries:
            results = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
            
            self.stdout.write(f"\nSearch for '{query}': {results.count()} results")
            for user in results[:3]:
                self.stdout.write(f"  - {user.username}: {user.first_name} {user.last_name}")
        
        self.stdout.write("\n📊 Search Summary:")
        if all_users.count() == 0:
            self.stdout.write("❌ No users found in database!")
        else:
            self.stdout.write(f"✅ {all_users.count()} users available for search")
        
        # Check for demo social users
        demo_users = User.objects.filter(username__contains='social')
        if demo_users.exists():
            self.stdout.write(f"✅ Found {demo_users.count()} demo social users")
            for user in demo_users:
                self.stdout.write(f"  - {user.username}")
        else:
            self.stdout.write("⚠️ No demo social users found. Run 'python manage.py demo_social' to create them.")
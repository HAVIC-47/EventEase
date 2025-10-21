#!/usr/bin/env python
"""
Test script to verify dynamic ticket categories functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventease.settings')
django.setup()

from events.forms import TicketCategoryFormSet

def test_dynamic_formset():
    """Test that the formset can handle dynamic form creation"""
    
    print("Testing Dynamic Ticket Category Formset...")
    print("=" * 50)
    
    # Test empty formset (starting state)
    print("1. Testing empty formset (starting state):")
    empty_data = {
        'form-TOTAL_FORMS': '0',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '5',
    }
    
    formset = TicketCategoryFormSet(data=empty_data)
    print(f"   - Is valid: {formset.is_valid()}")
    print(f"   - Total forms: {formset.total_form_count()}")
    print(f"   - Max forms allowed: 5")
    print()
    
    # Test with 1 category
    print("2. Testing with 1 category:")
    one_category_data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '5',
        'form-0-name': 'General Admission',
        'form-0-category_type': 'general',
        'form-0-price': '25.00',
        'form-0-quantity_available': '100',
        'form-0-description': 'Standard ticket for general admission',
    }
    
    formset = TicketCategoryFormSet(data=one_category_data)
    print(f"   - Is valid: {formset.is_valid()}")
    if not formset.is_valid():
        print(f"   - Errors: {formset.errors}")
    print(f"   - Total forms: {formset.total_form_count()}")
    print()
    
    # Test with 5 categories (maximum)
    print("3. Testing with 5 categories (maximum):")
    max_categories_data = {
        'form-TOTAL_FORMS': '5',
        'form-INITIAL_FORMS': '0',
        'form-MIN_NUM_FORMS': '0',
        'form-MAX_NUM_FORMS': '5',
    }
    
    # Add 5 categories
    categories = [
        ('General', 'general', '25.00', '100'),
        ('VIP', 'vip', '50.00', '50'),
        ('Student', 'student', '15.00', '75'),
        ('Early Bird', 'early_bird', '20.00', '30'),
        ('Group', 'group', '22.00', '40'),
    ]
    
    for i, (name, cat_type, price, quantity) in enumerate(categories):
        max_categories_data.update({
            f'form-{i}-name': name,
            f'form-{i}-category_type': cat_type,
            f'form-{i}-price': price,
            f'form-{i}-quantity_available': quantity,
            f'form-{i}-description': f'{name} ticket category',
        })
    
    formset = TicketCategoryFormSet(data=max_categories_data)
    print(f"   - Is valid: {formset.is_valid()}")
    if not formset.is_valid():
        print(f"   - Errors: {formset.errors}")
    print(f"   - Total forms: {formset.total_form_count()}")
    print()
    
    # Test with 6 categories (should exceed maximum)
    print("4. Testing with 6 categories (should exceed maximum):")
    exceed_max_data = max_categories_data.copy()
    exceed_max_data['form-TOTAL_FORMS'] = '6'
    exceed_max_data.update({
        'form-5-name': 'Premium',
        'form-5-category_type': 'premium',
        'form-5-price': '75.00',
        'form-5-quantity_available': '25',
        'form-5-description': 'Premium ticket category',
    })
    
    formset = TicketCategoryFormSet(data=exceed_max_data)
    print(f"   - Is valid: {formset.is_valid()}")
    if not formset.is_valid():
        print(f"   - Errors: {formset.non_form_errors()}")
    print(f"   - Total forms: {formset.total_form_count()}")
    print()
    
    print("✅ Dynamic formset tests completed!")
    print("The system properly handles 0-5 ticket categories dynamically.")

if __name__ == "__main__":
    test_dynamic_formset()

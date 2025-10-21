from django import forms
from .models import Review, EventReview, VenueReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title for your review...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with our service...'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set empty_label so rating starts with no selection
        self.fields['rating'].empty_label = "Select a rating"
        self.fields['title'].label = "Review Title"
        self.fields['content'].label = "Your Review"


class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['rating', 'organization_rating', 'venue_rating', 'value_rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'overall'
                }
            ),
            'organization_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'organization'
                }
            ),
            'venue_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'venue'
                }
            ),
            'value_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'value'
                }
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title for your review...'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this event...'
            })
        }
        
    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = "Overall Rating"
        self.fields['organization_rating'].label = "Organization"
        self.fields['venue_rating'].label = "Venue Quality"
        self.fields['value_rating'].label = "Value for Money"
        self.fields['title'].label = "Review Title"
        self.fields['comment'].label = "Your Review"
        self.fields['comment'].required = False
    
    def save(self, commit=True):
        review = super().save(commit=False)
        if self.event:
            review.event = self.event
        if self.user:
            review.user = self.user
        if commit:
            review.save()
        return review


class VenueReviewForm(forms.ModelForm):
    class Meta:
        model = VenueReview
        fields = ['rating', 'ambience_rating', 'service_rating', 'cleanliness_rating', 'value_rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'overall'
                }
            ),
            'ambience_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'ambience'
                }
            ),
            'service_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'service'
                }
            ),
            'cleanliness_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'cleanliness'
                }
            ),
            'value_rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)], 
                attrs={
                    'class': 'form-control star-rating-select',
                    'data-rating-type': 'value'
                }
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title for your venue review...'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this venue...'
            })
        }
        
    def __init__(self, *args, **kwargs):
        self.venue = kwargs.pop('venue', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = "Overall Rating"
        self.fields['ambience_rating'].label = "Ambience & Atmosphere"
        self.fields['service_rating'].label = "Service Quality"
        self.fields['cleanliness_rating'].label = "Cleanliness & Maintenance"
        self.fields['value_rating'].label = "Value for Money"
        self.fields['title'].label = "Review Title"
        self.fields['comment'].label = "Your Review"
        self.fields['comment'].required = False
    
    def save(self, commit=True):
        review = super().save(commit=False)
        if self.venue:
            review.venue = self.venue
        if self.user:
            review.user = self.user
        if commit:
            review.save()
        return review
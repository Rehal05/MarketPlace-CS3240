from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    
    # Allow optional max price, and keep same style as min price
    price_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={  # use NumberInput widget
            'class': 'form-input', # same as price_min
            'placeholder': 'Maximum price (optional)',
            'step': '0.01',
            'min': '0',
        })
    )
    class Meta:
        model = Post
        fields = ['title', 'image_url', 'description', 'price_min', 'price_max']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter post title',
                'required': True
            }),
            'image_url': forms.FileInput(attrs={
                'class': 'form-input-file',
                'accept': 'image/*'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe your item...',
                'rows': 5
            }),
            'price_min': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Minimum price',
                'step': '0.01',
                'min': '0'
            }),
            'price_max': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Maximum price',
                'step': '0.01',
                'min': '0'
            }),
        }
        labels = {
            'title': 'Title',
            'image_url': 'Upload Image',
            'description': 'Description',
            'price_min': 'Minimum Price ($)',
            'price_max': 'Maximum Price ($)(Optional)',
        }

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')

        if price_min is not None and price_max is not None:
            if price_min > price_max:
                raise forms.ValidationError(
                    "Minimum price cannot be greater than maximum price."
                )
        
        return cleaned_data

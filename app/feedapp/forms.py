from django import forms
from .models import Offer, Post

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'electronics, furniture, sale'}),
        help_text="Enter comma-separated keywords"
    )

    class Meta:
        model = Post
        fields = [
            'title', 'image', 'image_url', 'description',
            'category', 'location', 'latitude', 'longitude',
            'tags', 'price_min', 'price_max', 'allow_offers', 'min_offer_price'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter post title',
                'required': True
            }),
            'image': forms.FileInput(attrs={
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
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input', 'placeholder': 'City, State'
            }),
            'allow_offers': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'}),
        }
        labels = {
            'title': 'Title',
            'image': 'Upload Image',
            'description': 'Description',
            'price_min': 'Minimum Price ($)',
            'price_max': 'Maximum Price ($)',
        }

    def clean(self):
        cleaned_data = super().clean()
        price_min = cleaned_data.get('price_min')
        price_max = cleaned_data.get('price_max')
        min_offer = cleaned_data.get('min_offer_price')
        allow_offers = cleaned_data.get('allow_offers')
        if price_min is not None and price_max is not None:
            if price_min > price_max:
                raise forms.ValidationError(
                    "Minimum price cannot be greater than maximum price."
                )
        if cleaned_data.get('min_offer_price') and price_min and cleaned_data['min_offer_price'] < price_min:
            raise forms.ValidationError("Minimum offer must be at least the minimum listing price.")
        if not allow_offers:
            cleaned_data['min_offer_price'] = None
        elif min_offer is None:
            self.add_error('min_offer_price', 'Minimum offer price required when offers enabled.')
        return cleaned_data

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['amount', 'message']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.01'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3})
        }

    def __init__(self, post, *args, **kwargs):
        self.post = post
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        min_offer = self.post.min_offer_price or self.post.price_min
        if min_offer and amount < min_offer:
            raise forms.ValidationError('Offer below seller minimum; auto-rejected.')
        return amount

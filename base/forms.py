from django import forms

from allauth.account.forms import SignupForm

PAYMENTS_CHOICES =(

    ('S','Stripe'),
    ('C','Cash On Delivier '),
     ('P','PayPal'),


)

class CheckoutForm(forms.Form):
    city = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'id':"email",'class':"form-control",'placeholder':"City or District Near"}))
    phone_number = forms.CharField(max_length=15,widget=forms.NumberInput(attrs={'placeholder':"Phone Number" ,'maxlength':"15",'class':"form-control py-0"}))
    street_address = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'id':"address",'class':"form-control",'placeholder':"City or 1234 Main St"}))
    apartment_address = forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'id':"address-2",'class':"form-control",'placeholder':"Apartment or suite"}))
    pin_code=forms.CharField(max_length=8,widget=forms.NumberInput(attrs={'placeholder':"Pin Code" ,'maxlength':"8",'class':"form-control"}))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    save_info=forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_option =forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENTS_CHOICES)



class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name',widget=forms.TextInput(attrs={'placeholder':"First Name"}))
    last_name = forms.CharField(max_length=30, label='Last Name',widget=forms.TextInput(attrs={'placeholder':"First Name"}))
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

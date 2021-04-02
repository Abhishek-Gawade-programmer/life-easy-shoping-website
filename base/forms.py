from django import forms

PAYMENTS_CHOICES =(

    ('S','Stripe'),
    ('C','Cash On Delivier '),
     ('P','PayPal'),


)

class CheckoutForm(forms.Form):
    city = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'id':"email",'class':"form-control",'placeholder':"City or District Near"}))
    phone_number = forms.CharField(max_length=8,widget=forms.NumberInput(attrs={'placeholder':"Phone Number" ,'maxlength':"8",'class':"form-control py-0"}))
    street_address = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'id':"address",'class':"form-control",'placeholder':"City or 1234 Main St"}))
    apartment_address = forms.CharField(max_length=250,required=False,widget=forms.TextInput(attrs={'id':"address-2",'class':"form-control",'placeholder':"Apartment or suite"}))
    pin_code=forms.CharField(max_length=8,widget=forms.NumberInput(attrs={'placeholder':"Pin Code" ,'maxlength':"8",'class':"form-control"}))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    save_info=forms.BooleanField(widget=forms.CheckboxInput(),required=False)
    payment_option =forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENTS_CHOICES)


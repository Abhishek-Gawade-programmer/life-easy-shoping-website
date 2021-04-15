from django import forms



CATEGORY_CHOICES=(
    ('A','Available'),
    ('NA','Not Available'),

)
LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)







class CreateNewForm(forms.Form):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'id':"f2 input-char-counter",'class':"form-control",'length':"100",'maxlength':'100'}))

    
    price = forms.CharField(max_length=10,widget=forms.NumberInput(attrs={'id':"f2",'class':"form-control" }))
    discount_price = forms.CharField(max_length=10,widget=forms.NumberInput(attrs={'id':"f3",'class':"form-control" }))

    category =forms.BooleanField(widget=forms.CheckboxInput(),required=True)

    label_name=forms.CharField(max_length=14,widget=forms.TextInput(attrs={'id':"f4 input-char-counter",'class':"form-control",'length':"14",'maxlength':'14'}))

    label =forms.ChoiceField(choices=LABEL_CHOICES,widget=forms.Select(attrs={'class':"form-control"}))

    
    description = forms.CharField(max_length=250,widget=forms.Textarea(attrs={'name':"description",'id':"post_content"}),required=False)
    image = forms.ImageField()





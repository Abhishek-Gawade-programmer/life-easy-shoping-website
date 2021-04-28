from django import forms
from base.models import Item


CATEGORY_CHOICES=(
    ('A','Available'),
    ('NA','Not Available'),

)
LABEL_CHOICES=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
)



class CreateNewItemForm(forms.Form):
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'id':"f2 input-char-counter",'class':"form-control",'length':"100",'maxlength':'100'}))

    
    price = forms.CharField(max_length=10,widget=forms.NumberInput(attrs={'id':"f2",'class':"form-control" }))
    discount_price = forms.CharField(max_length=10,widget=forms.NumberInput(attrs={'id':"f3",'class':"form-control" }),required=False)

    category =forms.BooleanField(widget=forms.CheckboxInput(),required=False)

    label_name=forms.CharField(max_length=14,widget=forms.TextInput(attrs={'id':"f4 input-char-counter",'class':"form-control",'length':"14",'maxlength':'14'}),required=False)

    label =forms.ChoiceField(choices=LABEL_CHOICES,widget=forms.Select(attrs={'class':"form-control"}))

    
    description = forms.CharField(max_length=1500,widget=forms.Textarea(attrs={'name':"description",'id':"post_content"}),required=False)
    image = forms.ImageField(widget=forms.FileInput(),required=False)
    image2 = forms.ImageField(widget=forms.FileInput(),required=False)
    image3 = forms.ImageField(widget=forms.FileInput(),required=False)
    image4 = forms.ImageField(widget=forms.FileInput(),required=False)
    image5 = forms.ImageField(widget=forms.FileInput(),required=False)
    image6 = forms.ImageField(widget=forms.FileInput(),required=False)


    def clean_title(self,*args,**kwargs):
        x=Item.objects.filter(title=self.cleaned_data.get('title'))

        if x.exists():
            # messages.error(self.request,f" { self.request.user.username } Don't have Any Item in The Cart")
            raise forms.ValidationError('The title already exists')

        return self.cleaned_data.get('title')

    def clean_description(self,*args,**kwargs):
        if not self.cleaned_data.get('description'):
            raise forms.ValidationError('Description Cannot be empty')

        return self.cleaned_data.get('description')


  
class GeeksForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

















    







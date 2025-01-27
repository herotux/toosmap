from django import forms
from django.utils.safestring import mark_safe  # اضافه کردن mark_safe
from .models import user, Province, City, role_user, role

class UserForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.all(), required=False, widget=forms.Select(attrs={'placeholder': 'استان را انتخاب کنید', 'class': 'rtl-input'}))
    city = forms.ModelChoiceField(queryset=City.objects.none(), required=False, widget=forms.Select(attrs={'placeholder': 'شهر را انتخاب کنید', 'class': 'rtl-input'}))
    role = forms.ModelChoiceField(queryset=role.objects.all(), required=True, widget=forms.Select(attrs={'placeholder': 'گروه کاربری را انتخاب کنید', 'class': 'rtl-input'}))
    mobile_verified = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={'class': 'rtl-input'}))

    class Meta:
        model = user
        fields = [
            'username', 'first_name', 'last_name', 'mobile', 'national_code', 'email',
            'password', 'province', 'role', 'city', 'region', 'year', 'month', 'day', 'national', 'mobile_verified'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'نام کاربری را وارد کنید', 'class': 'rtl-input'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'نام را وارد کنید', 'class': 'rtl-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی را وارد کنید', 'class': 'rtl-input'}),
            'mobile': forms.TextInput(attrs={'placeholder': ' (مثال :09121234567)شماره موبایل را وارد کنید', 'class': 'rtl-input'}),
            'national_code': forms.TextInput(attrs={'placeholder': 'کد ملی را وارد کنید', 'class': 'rtl-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل را وارد کنید', 'class': 'rtl-input'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'رمز عبور را وارد کنید', 'class': 'rtl-input'}),
            'region': forms.TextInput(attrs={'placeholder': 'محله یا روستا را وارد کنید', 'class': 'rtl-input'}),
            'year': forms.Select(attrs={'placeholder': 'سال را انتخاب کنید', 'class': 'rtl-input'}),
            'month': forms.Select(attrs={'placeholder': 'ماه را انتخاب کنید', 'class': 'rtl-input'}),
            'day': forms.Select(attrs={'placeholder': 'روز را انتخاب کنید', 'class': 'rtl-input'}),
            'national': forms.CheckboxInput(attrs={'class': 'rtl-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'province' in self.data:
            province_id = int(self.data.get('province'))
            self.fields['city'].queryset = City.objects.filter(province_id=province_id)

        # اضافه کردن ستاره قرمز برای فیلدهای اجباری
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span class='required-star'>*</span>")
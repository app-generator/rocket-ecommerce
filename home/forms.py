from django import forms
from apps.common.models import Product
from django.forms import ClearableFileInput
from django.utils.html import format_html
from django_quill.forms import QuillFormField
from django.utils.safestring import mark_safe

class ImageWidget(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        
        if value and hasattr(value, 'url'):
            output.append('<div style="display: flex;">')
            output.append('<div style="display: flex; flex-direction: column; justify-content: center;">')
            output.append('</div>')
            output.append('<img src="{}" style="max-height:100px;">'.format(value.url))
            output.append('</div>')
        
        output.append(super().render(name, value, attrs, renderer))
        
        return format_html(''.join(output))

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('product_stripe', )
        labels = {
            'price': mark_safe('Price (Read Only) - <span>Please edit the value in Stripe</span>'),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = field.label
            self.fields[field_name].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            self.fields[field_name].widget.attrs['required'] = False
            self.fields['featured'].widget.attrs['class'] = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            self.fields['discount'].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            if field_name.startswith('img_'):
                self.fields[field_name].widget = ImageWidget()
                self.fields['img_main'].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"'
                self.fields['img_1'].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"'
                self.fields['img_2'].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"'
                self.fields['img_3'].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"'
                self.fields['img_4'].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"'
                self.fields['img_5'].widget.attrs['class'] = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"'
            self.fields['price'].widget.attrs['readonly'] = True


class PrivacyPolicyForm(forms.Form):
    legal_privacy = QuillFormField()

class TermsForm(forms.Form):
    legal_terms = QuillFormField()

class HelpForm(forms.Form):
    legal_help = QuillFormField()
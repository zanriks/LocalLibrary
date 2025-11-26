from django import forms
from django.forms import ModelForm
from .models import BookInstance
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks (default 3 weeks)."
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Проверка: не в прошлом ли дата
        if data < _get_current_date():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Проверка: не далее 4 недель в будущем
        if data > _get_current_date() + _get_max_renewal_delta():
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data

# Вспомогательные функции для тестирования и чистоты кода
def _get_current_date():
    from datetime import date
    return date.today()

def _get_max_renewal_delta():
    from datetime import timedelta
    return timedelta(weeks=4)

# Если используеете ModelForm, то RenewBookForm можно заменить на RenewBookModelForm
# class RenewBookModelForm(ModelForm):
#     class Meta:
#         model = BookInstance
#         fields = ['due_back']
#         labels = {'due_back': _('Renewal date')}
#         help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3 weeks).')}
#
#     def clean_due_back(self):
#         data = self.cleaned_data['due_back']
#         from datetime import date, timedelta
#         if data < date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))
#         if data > date.today() + timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
#         return data
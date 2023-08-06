from django import forms
from edc_constants.constants import NO, YES
from edc_crf.modelform_mixins import CrfModelFormMixin
from edc_form_validators.form_validator import FormValidator

from ..models import Followup


class FollowupFormValidator(FormValidator):
    def clean(self):
        self.required_if(YES, field="alive", field_required="in_care")
        self.required_if(NO, field="in_care", field_required="reason_not_in_care")
        self.validate_other_specify(field="reason_not_in_care")
        self.required_if(YES, field="alive", field_required="has_next_appointment")
        self.required_if(
            YES, field="has_next_appointment", field_required="next_appointment_date"
        )


class FollowupForm(CrfModelFormMixin, forms.ModelForm):
    form_validator_cls = FollowupFormValidator

    class Meta:
        model = Followup
        fields = "__all__"

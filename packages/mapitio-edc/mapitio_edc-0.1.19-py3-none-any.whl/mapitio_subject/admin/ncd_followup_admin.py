from django.contrib import admin
from django.utils.safestring import mark_safe
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin import SimpleHistoryAdmin
from mapitio_subject.admin.fieldsets import comment_fieldset_tuple

from ..admin_site import mapitio_subject_admin
from ..exim_resources import NcdFollowupResource
from ..forms import NcdFollowupForm
from ..models import NcdFollowup
from .modeladmin import CrfModelAdminMixin


@admin.register(NcdFollowup, site=mapitio_subject_admin)
class NcdFollowupAdmin(CrfModelAdminMixin, SimpleHistoryAdmin):
    form = NcdFollowupForm

    resource_class = NcdFollowupResource

    additional_instructions = mark_safe(
        "<span style='color:#ff8000'>Complete for data as of the patient's last attended clinic visit</span>"
    )

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Diabetes",
            {
                "fields": (
                    "diabetic",
                    "diabetes_dx_date_known",
                    "diabetes_dx_date",
                    "diabetes_dx_date_estimated",
                    "diabetes_rx",
                    "other_diabetes_rx",
                ),
            },
        ),
        (
            "Hypertension",
            {
                "fields": (
                    "hypertensive",
                    "hypertension_dx_date_known",
                    "hypertension_dx_date",
                    "hypertension_dx_date_estimated",
                    "hypertension_rx",
                    "other_hypertension_rx",
                ),
            },
        ),
        comment_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ("diabetes_rx", "hypertension_rx")

    radio_fields = {
        "diabetic": admin.VERTICAL,
        "diabetes_dx_date_known": admin.VERTICAL,
        "diabetes_dx_date_estimated": admin.VERTICAL,
        "hypertensive": admin.VERTICAL,
        "hypertension_dx_date_known": admin.VERTICAL,
        "hypertension_dx_date_estimated": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }

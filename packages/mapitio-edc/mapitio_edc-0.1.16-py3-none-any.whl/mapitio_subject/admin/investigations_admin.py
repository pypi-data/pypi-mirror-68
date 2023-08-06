from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_crf import CrfModelResource
from edc_form_label.form_label_modeladmin_mixin import FormLabelModelAdminMixin
from edc_model_admin import SimpleHistoryAdmin
from import_export.admin import ExportActionModelAdmin
from import_export.fields import Field
from mapitio_subject.admin.fieldsets import comment_fieldset_tuple

from ..admin_site import mapitio_subject_admin
from ..forms import InvestigationsForm
from ..models import Investigations
from .modeladmin import CrfModelAdminMixin


class InvestigationsResource(CrfModelResource):
    chest_xray_findings_names = Field()

    def dehydrate_chest_xray_findings_names(self, obj):
        names = [obj.name for obj in obj.chest_xray_findings.all()]
        names.sort()
        return ",".join(names)

    class Meta(CrfModelResource.Meta):
        model = Investigations


@admin.register(Investigations, site=mapitio_subject_admin)
class InvestigationsAdmin(
    CrfModelAdminMixin,
    FormLabelModelAdminMixin,
    ExportActionModelAdmin,
    SimpleHistoryAdmin,
):
    form = InvestigationsForm

    resource_class = InvestigationsResource

    fieldsets = (
        (None, {"fields": ("subject_visit", "report_datetime")}),
        (
            "Chest X-ray",
            {
                "fields": (
                    "chest_xray_requested",
                    "chest_xray_findings_documented",
                    "chest_xray_findings",
                    "chest_xray_findings_other",
                )
            },
        ),
        (
            "ECG",
            {
                "fields": (
                    "ecg_requested",
                    "ecg_findings_documented",
                    "ecg_findings",
                    "ecg_findings_other",
                )
            },
        ),
        (
            "ECHO",
            {
                "fields": (
                    "echo_requested",
                    "echo_findings_documented",
                    "echo_findings",
                    "echo_findings_other",
                )
            },
        ),
        comment_fieldset_tuple,
        audit_fieldset_tuple,
    )

    filter_horizontal = ["chest_xray_findings", "ecg_findings", "echo_findings"]

    radio_fields = {
        "chest_xray_requested": admin.VERTICAL,
        "chest_xray_findings_documented": admin.VERTICAL,
        "ecg_requested": admin.VERTICAL,
        "ecg_findings_documented": admin.VERTICAL,
        "echo_requested": admin.VERTICAL,
        "echo_findings_documented": admin.VERTICAL,
        "crf_status": admin.VERTICAL,
    }

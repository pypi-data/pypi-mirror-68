from edc_model import models as edc_models

from .model_mixins import CrfModelMixin, IndicatorsModelMixin


class Indicators(IndicatorsModelMixin, CrfModelMixin, edc_models.BaseUuidModel):

    height = edc_models.HeightField(null=True, blank=True)

    class Meta(CrfModelMixin.Meta):
        verbose_name = "Indicators"
        verbose_name_plural = "Indicators"

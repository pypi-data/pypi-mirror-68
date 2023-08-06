from edc_model import models as edc_models

from sarscov2.model_mixins import CoronaKapModelMixin, CoronaKapDiseaseModelMixin


class CoronavirusKap(
    CoronaKapDiseaseModelMixin, CoronaKapModelMixin, edc_models.BaseUuidModel,
):
    class Meta:
        verbose_name = "Coronavirus Knowledge, Attitudes, and Practices"
        verbose_name_plural = "Coronavirus Knowledge, Attitudes, and Practices"

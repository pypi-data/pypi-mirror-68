from django.utils.translation import gettext as _

from jsonstore import CharField, IntegerField

from aleksis.apps.chronos import models as chronos_models
from aleksis.core import models as core_models

core_models.Person.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
core_models.Group.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)

core_models.Group.field(
    untis_subject=CharField(
        verbose_name=_("UNTIS subject"),
        help_text=_(
            "The UNTIS import will use this for matching course groups"
            "(along with parent groups)."
        ),
        blank=True,
        max_length=255,
    )
)

# Chronos models
chronos_models.Subject.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.Room.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.SupervisionArea.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.Lesson.field(
    lesson_id_untis=IntegerField(verbose_name=_("Lesson id in UNTIS"), null=True, blank=True)
)
chronos_models.Lesson.field(
    element_id_untis=IntegerField(
        verbose_name=_("Number of lesson element in UNTIS"), null=True, blank=True
    )
)
chronos_models.Lesson.field(
    term_untis=IntegerField(verbose_name=_("Term id in UNTIS"), null=True, blank=True)
)
chronos_models.LessonPeriod.field(
    element_id_untis=IntegerField(
        verbose_name=_("Number of lesson element in UNTIS"), null=True, blank=True
    )
)
chronos_models.LessonSubstitution.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.SupervisionSubstitution.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.AbsenceReason.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.Absence.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.Event.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.Holiday.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)
chronos_models.ExtraLesson.field(
    import_ref_untis=IntegerField(verbose_name=_("UNTIS import reference"), null=True, blank=True)
)

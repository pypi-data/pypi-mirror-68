from django.db import transaction

from .importers.absences import import_absences
from .importers.common_data import (
    import_absence_reasons,
    import_breaks,
    import_classes,
    import_rooms,
    import_subjects,
    import_supervision_areas,
    import_teachers,
    import_time_periods,
)
from .importers.events import import_events
from .importers.holidays import import_holidays
from .importers.lessons import import_lessons
from .importers.substitutions import import_substitutions


@transaction.atomic
def untis_import_mysql():
    # Coomon data for Chronos
    subjects_ref = import_subjects()
    rooms_ref = import_rooms()
    absence_reasons_ref = import_absence_reasons()

    # Common data for core
    teachers_ref = import_teachers()
    classes_ref = import_classes(teachers_ref)

    # Time periods
    time_periods_ref = import_time_periods()
    breaks_ref = import_breaks(time_periods_ref)

    # Holidays
    holidays_ref = import_holidays()

    # Supervisions
    supervision_areas_ref = import_supervision_areas(breaks_ref, teachers_ref)

    # Lessons
    import_lessons(time_periods_ref, rooms_ref, subjects_ref, teachers_ref, classes_ref)

    # Substitutions
    import_absences(absence_reasons_ref, time_periods_ref, teachers_ref, classes_ref, rooms_ref)
    import_substitutions(
        teachers_ref, subjects_ref, rooms_ref, classes_ref, supervision_areas_ref, time_periods_ref,
    )

    # Events
    import_events(time_periods_ref, teachers_ref, classes_ref, rooms_ref)

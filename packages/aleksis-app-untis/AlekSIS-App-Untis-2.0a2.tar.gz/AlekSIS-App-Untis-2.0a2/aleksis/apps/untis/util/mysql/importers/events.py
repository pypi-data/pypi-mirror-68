import logging

from tqdm import tqdm

from aleksis.apps.chronos import models as chronos_models

from .... import models as mysql_models
from ..util import (
    TQDM_DEFAULTS,
    connect_untis_fields,
    get_first_period,
    get_last_period,
    get_term,
    move_weekday_to_range,
    run_default_filter,
    untis_date_to_date,
)

logger = logging.getLogger(__name__)


def import_events(time_periods_ref, teachers_ref, classes_ref, rooms_ref):
    ref = {}

    # Get term
    term = get_term()
    term_date_start = untis_date_to_date(term.datefrom)
    term_date_end = untis_date_to_date(term.dateto)

    # Get absences
    events = (
        run_default_filter(mysql_models.Event.objects, filter_term=False)
        .filter(datefrom__lte=term.dateto, dateto__gte=term.datefrom)
        .order_by("event_id")
    )

    existing_events = []
    for event in tqdm(events, desc="Import events", **TQDM_DEFAULTS):
        import_ref = event.event_id

        logger.info("Import event {}".format(import_ref))

        # Build values
        comment = event.text

        date_from = untis_date_to_date(event.datefrom)
        date_to = untis_date_to_date(event.dateto)
        period_from = event.lessonfrom
        period_to = event.lessonto
        weekday_from = date_from.weekday()
        weekday_to = date_to.weekday()

        # Check min/max weekdays
        weekday_from = move_weekday_to_range(time_periods_ref, weekday_from)
        weekday_to = move_weekday_to_range(time_periods_ref, weekday_to)

        # Check min/max periods
        first_period = get_first_period(time_periods_ref, weekday_from)
        last_period = get_last_period(time_periods_ref, weekday_from)

        if period_from == 0:
            period_from = first_period
        if period_to == 0:
            period_to = last_period

        time_period_from = time_periods_ref[weekday_from][period_from]
        time_period_to = time_periods_ref[weekday_to][period_to]

        groups = []
        teachers = []
        rooms = []

        # Get groups, teachers and rooms
        raw_events = connect_untis_fields(event, "eventelement", 10)
        for raw_event in raw_events:
            el = raw_event.split("~")

            # Group
            if el[0] != "0" and el[0] != "":
                group = classes_ref[int(el[0])]
                groups.append(group)

            # Teacher
            if el[2] != "0" and el[2] != "":
                teacher = teachers_ref[int(el[2])]
                teachers.append(teacher)

            # Room
            if el[3] != "0" and el[3] != "":
                room = rooms_ref[int(el[3])]
                rooms.append(room)

        new_event, created = chronos_models.Event.objects.get_or_create(
            import_ref_untis=import_ref,
            defaults={
                "date_start": date_from,
                "date_end": date_to,
                "period_from": time_period_from,
                "period_to": time_period_to,
                "title": comment,
            },
        )

        if created:
            logger.info("  New event created")

        # Sync simple fields
        if (
            new_event.date_start != date_from
            or new_event.date_end != date_to
            or new_event.period_from != time_period_from
            or new_event.period_to != time_period_to
            or new_event.title != comment
        ):
            new_event.date_start = date_from
            new_event.date_end = date_to
            new_event.period_from = time_period_from
            new_event.period_to = time_period_to
            new_event.title = comment
            new_event.save()
            logger.info("  Time range and title updated")

        # Sync m2m-fields
        new_event.groups.set(groups)
        new_event.teachers.set(teachers)
        new_event.rooms.set(rooms)

        existing_events.append(import_ref)
        ref[import_ref] = new_event

        # Delete all no longer existing events
        for e in chronos_models.Event.objects.filter(
            date_start__lte=term_date_start, date_end__gte=term_date_end
        ):
            if e.import_ref_untis and e.import_ref_untis not in existing_events:
                logger.info("Event {} deleted".format(e.id))
                e.delete()

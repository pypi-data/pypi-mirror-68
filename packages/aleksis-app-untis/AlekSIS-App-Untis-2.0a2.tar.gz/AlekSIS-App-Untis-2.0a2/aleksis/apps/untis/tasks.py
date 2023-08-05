from aleksis.core.util.core_helpers import celery_optional

from .util.mysql.main import untis_import_mysql as _untis_import_mysql


@celery_optional
def untis_import_mysql():
    """Celery task for import of UNTIS data from MySQL."""
    _untis_import_mysql()

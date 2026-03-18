import threading
from dbos import DBOS, DBOSConfig
from src.common.settings import settings
from src.workflows import WORKFLOWS


if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "kdp-workflows",
        "system_database_url": settings.db_url,
        "conductor_key": settings.conductor_key,
        "conductor_url": "ws://dbos-conductor:8090/",
    }
    DBOS(config=config)
    DBOS.launch()
    DBOS.apply_schedules(WORKFLOWS)
    threading.Event().wait()

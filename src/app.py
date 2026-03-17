import threading
from dbos import DBOS, DBOSConfig
from src.common.settings import settings
from workflows.defend import bronze

WORKFLOWS = [bronze]

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "kdp-workflows",
        "system_database_url": settings.db_url,
    }
    DBOS(config=config)
    DBOS.launch()
    for workflow in WORKFLOWS:
        workflow()
    threading.Event().wait()

from datetime import datetime
from typing import Any
import aioboto3
from dbos import DBOS
from types_aiobotocore_emr_serverless.literals import JobRunStateType
from common.settings import settings
from models.job import JobContext
from src.common.emr import (
    get_or_create_application,
    start_application_if_needed,
    wait_for_app_started,
    start_job,
    stop_application,
    wait_for_job,
)


@DBOS.workflow()
async def run_emr_job(run_time: datetime, context: dict[str, Any]) -> JobRunStateType:
    parsed_context: JobContext = JobContext(**context)
    session: aioboto3.Session = aioboto3.Session()
    async with session.client(
        "emr-serverless", region_name=settings.aws_region
    ) as emr_client:
        app_id = await get_or_create_application(emr_client, context=parsed_context)

        await start_application_if_needed(emr_client, app_id=app_id)
        await wait_for_app_started(emr_client, app_id=app_id)

        job_id = await start_job(emr_client, context=parsed_context, app_id=app_id)

        result: JobRunStateType = await wait_for_job(
            emr_client, app_id=app_id, job_id=job_id
        )

        await stop_application(emr_client, app_id)

    return result

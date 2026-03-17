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


def run_workflow(run_time: datetime, context: dict[str, Any]):
    DBOS.start_workflow(
        func=run_emr_job,
        run_time=run_time,
        raw_context=context,
    )


@DBOS.workflow()
async def run_emr_job(
    run_time: datetime, raw_context: dict[str, Any]
) -> JobRunStateType:
    context: JobContext = JobContext(**raw_context)
    session = aioboto3.Session()
    async with session.resource(
        "emr-serverless", region_name=settings.aws_region
    ) as emr_client:
        app_id = await get_or_create_application(emr_client, context=context)

        await start_application_if_needed(emr_client, app_id=app_id)
        await wait_for_app_started(emr_client, app_id=app_id)

        job_id = await start_job(emr_client, context=context, app_id=app_id)

        result: JobRunStateType = await wait_for_job(
            emr_client, app_id=app_id, job_id=job_id
        )

        await stop_application(emr_client, app_id)

    return result

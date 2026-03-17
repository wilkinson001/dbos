from dbos import DBOS
from types_aiobotocore_emr_serverless.client import EMRServerlessClient
from types_aiobotocore_emr_serverless.literals import (
    ApplicationStateType,
    JobRunStateType,
)
from types_aiobotocore_emr_serverless.type_defs import (
    ApplicationTypeDef,
    GetApplicationResponseTypeDef,
    GetJobRunResponseTypeDef,
    ListApplicationsResponseTypeDef,
    StartJobRunResponseTypeDef,
)

from models.job import JobContext

TERMINAL_STATES = {"SUCCESS", "FAILED", "CANCELLED"}


@DBOS.step()
async def get_or_create_application(
    emr_client: EMRServerlessClient, context: JobContext
) -> str:
    apps: ListApplicationsResponseTypeDef = await emr_client.list_applications()

    for app in apps["applications"]:
        if app.get("name") == context.app_name:
            return app["id"]

    # Create if not exists
    response = await emr_client.create_application(
        name=context.app_name,
        releaseLabel=context.release_label,
        type=context.job_type,
        clientToken=f"{DBOS.workflow_id}:{DBOS.step_id}",
    )
    return response["applicationId"]


@DBOS.step()
async def start_application_if_needed(emr_client: EMRServerlessClient, app_id: str):
    response: GetApplicationResponseTypeDef = await emr_client.get_application(
        applicationId=app_id
    )
    app: ApplicationTypeDef = response["application"]

    if app["state"] == "STARTED":
        return

    if app["state"] in ["CREATED", "STOPPED"]:
        await emr_client.start_application(applicationId=app_id)


@DBOS.step()
async def wait_for_app_started(emr_client: EMRServerlessClient, app_id: str) -> None:
    while True:
        app: GetApplicationResponseTypeDef = await emr_client.get_application(
            applicationId=app_id
        )
        state: ApplicationStateType = app["application"]["state"]

        if state == "STARTED":
            return

        DBOS.sleep(5)


@DBOS.step()
async def start_job(
    emr_client: EMRServerlessClient, context: JobContext, app_id: str
) -> str:
    response: StartJobRunResponseTypeDef = await emr_client.start_job_run(
        applicationId=app_id,
        clientToken=f"{DBOS.workflow_id}:{DBOS.step_id}",
        **context.job_params.model_dump(),
    )
    return response["jobRunId"]


@DBOS.step()
async def wait_for_job(
    emr_client: EMRServerlessClient, app_id: str, job_id: str, poll_interval=10
) -> JobRunStateType:
    while True:
        job: GetJobRunResponseTypeDef = await emr_client.get_job_run(
            applicationId=app_id, jobRunId=job_id
        )
        state = job["jobRun"]["state"]
        if state in TERMINAL_STATES:
            return state

        DBOS.sleep(poll_interval)


@DBOS.step()
async def stop_application(emr_client: EMRServerlessClient, application_id: str):
    await emr_client.stop_application(applicationId=application_id)

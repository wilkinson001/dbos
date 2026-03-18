from dbos import ScheduleInput
from workflows.common import run_emr_job
from models.job import JobContext, JobParams


BRONZE: ScheduleInput = ScheduleInput(
    schedule_name="defend_bronze",
    workflow_fn=run_emr_job,
    schedule="0/5 * * * *",
    context=JobContext(
        app_name="defend_bronze",
        release_label="emr-7.10.0",
        job_type="SPARK",
        job_params=JobParams(executionRoleArn=""),
    ).model_dump(),
)

from dbos import DBOS

from common.workflows import run_workflow
from models.job import JobContext, JobParams


def bronze():
    DBOS.create_schedule(
        schedule_name="defend_bronze",
        workflow_fn=run_workflow,
        schedule="* * * * *",
        context=JobContext(
            app_name="defend_bronze",
            release_label="emr-7.10.0",
            job_type="SPARK",
            job_params=JobParams(executionRoleArn=""),
        ).model_dump(),
    )

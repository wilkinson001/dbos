from typing import Optional
from pydantic import BaseModel
from types_aiobotocore_emr_serverless.type_defs import (
    ConfigurationOverridesUnionTypeDef,
    JobDriverUnionTypeDef,
)


class JobParams(BaseModel):
    executionRoleArn: str
    jobDriver: Optional[JobDriverUnionTypeDef] = None
    configurationOverrides: ConfigurationOverridesUnionTypeDef = {}


class JobContext(BaseModel):
    app_name: str
    release_label: str
    job_type: str
    job_params: JobParams

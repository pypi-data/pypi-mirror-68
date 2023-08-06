import datetime

from marshmallow import (Schema, ValidationError, fields, post_load, pre_dump,
                         pre_load, validate, validates_schema)
from qiskit.providers import JobStatus
from qiskit.qobj import QasmQobj as Qobj
from qiskit.result import Result


def _qiskit_model_validator(klass):
    def validator(val):
        try:
            klass.from_dict(val)
            return True
        except:
            return False

    return validator


class GetJobsQuerySchema(Schema):
    limit = fields.Integer(
        default=10,
        required=True,
        validate=validate.Range(min=1, max=500))

    skip = fields.Integer(
        default=0,
        required=True,
        validate=validate.Range(min=0))

    status = fields.List(fields.Str(
        required=False,
        validate=validate.OneOf([item.name for item in JobStatus])))

    date_start = fields.DateTime(format="iso")
    date_end = fields.DateTime(format="iso")

    @validates_schema
    def validate_dtimes(self, data, **kwargs):
        start = data.get("start_dtime")
        end = data.get("end_dtime")

        if start and end and end <= start:
            raise ValidationError("end_dtime must be greater than start_dtime")


class JobSchema(Schema):
    job_id = fields.Str(required=True)

    date_submit = fields.DateTime(required=True, format="iso")
    date_start = fields.DateTime(format="iso")
    date_end = fields.DateTime(format="iso")

    qobj = fields.Mapping(
        required=True,
        validate=_qiskit_model_validator(Qobj))

    status = fields.Str(
        required=True,
        validate=validate.OneOf([item.name for item in JobStatus]))

    result = fields.Mapping(
        required=False,
        validate=_qiskit_model_validator(Result))

    error = fields.Str()
    run_params = fields.Mapping()


class BackendStatusSchema(Schema):
    operational = fields.Boolean(required=True)
    pending_jobs = fields.Integer(required=True)

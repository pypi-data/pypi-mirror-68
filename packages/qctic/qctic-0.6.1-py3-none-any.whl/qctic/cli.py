import asyncio
import datetime
import inspect
import json
import logging
import random
import sys

import tornado.web
from qiskit import Aer, execute
from qiskit.assembler import disassemble
from qiskit.providers import JobStatus
from qiskit.qobj import QasmQobj as Qobj

from qctic.backend import (QCticQasmSimulator, QCticStatevectorSimulator,
                           QCticUnitarySimulator)

_MAX_WAIT_SECS = 10

_logger = logging.getLogger(__name__)


def _init_logging():
    try:
        import coloredlogs
        coloredlogs.install(level=logging.DEBUG)
    except ImportError:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)


def _inspect_execute_params(aer_backend):
    sig_execute = inspect.signature(execute)
    sig_backend_run = inspect.signature(aer_backend.run)
    params_execute = list(sig_execute.parameters.keys())
    params_backend_run = list(sig_backend_run.parameters.keys())

    return params_execute + params_backend_run


def _get_aer_backend(backend_name):
    simulators = {
        QCticQasmSimulator.NAME: "qasm_simulator",
        QCticStatevectorSimulator.NAME: "statevector_simulator",
        QCticUnitarySimulator.NAME: "unitary_simulator"
    }

    if backend_name not in simulators:
        raise Exception("Unknown backend: {}".format(backend_name))

    return Aer.get_backend(simulators[backend_name])


async def _run_job(job_store, job_id):
    _logger.debug("Starting task for job: %s", job_id)
    wait_secs = round(random.uniform(0, _MAX_WAIT_SECS), 1)
    _logger.debug("Waiting %s s. for job: %s", wait_secs, job_id)
    await asyncio.sleep(wait_secs)
    _logger.info("Running job: %s", job_id)

    job_data = job_store[job_id]

    job_data.update({
        "status": JobStatus.RUNNING.name,
        "date_start": datetime.datetime.utcnow().isoformat()
    })

    qobj = Qobj.from_dict(job_data["qobj"])
    circuits, run_config, user_qobj_header = disassemble(qobj)
    aer_backend = _get_aer_backend(user_qobj_header.get("backend_name"))

    execute_kwargs = {}
    execute_kwargs.update(run_config)
    execute_kwargs.update(job_data.get("run_params", {}))

    execute_kwargs = {
        key: val for key, val in execute_kwargs.items()
        if key in _inspect_execute_params(aer_backend)
    }

    aer_job = execute(circuits, aer_backend, **execute_kwargs)
    aer_job_result = aer_job.result()

    _logger.info("Job finished: %s", job_id)

    job_data.update({
        "status": JobStatus.DONE.name,
        "date_end": datetime.datetime.utcnow().isoformat(),
        "result": aer_job_result.to_dict()
    })


class JobsHandler(tornado.web.RequestHandler):
    def initialize(self, job_store):
        self.job_store = job_store

    def get(self):
        data = json.dumps([item for item in self.job_store.values()])
        self.write(data)

    def post(self):
        job_data = json.loads(self.request.body)
        job_id = job_data["job_id"]
        job_data.update({"status": JobStatus.QUEUED.name})
        self.job_store[job_id] = job_data
        asyncio.ensure_future(_run_job(self.job_store, job_id))


class JobHandler(tornado.web.RequestHandler):
    def initialize(self, job_store):
        self.job_store = job_store

    def get(self, job_id):
        data = json.dumps(self.job_store.get(job_id, None))
        self.write(data)


def build_app():
    job_store = {}

    return tornado.web.Application([
        (
            r"/jobs\/?",
            JobsHandler,
            dict(job_store=job_store)
        ),
        (
            r"/jobs/(?P<job_id>[^\/]+)\/?",
            JobHandler,
            dict(job_store=job_store)
        )
    ])


def run_local_server():
    try:
        _init_logging()
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 9090
        app = build_app()
        app.listen(port)
        _logger.info("Listening on port %s", port)
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except:
        _logger.error("Error on API server", exc_info=True)
    finally:
        loop.close()

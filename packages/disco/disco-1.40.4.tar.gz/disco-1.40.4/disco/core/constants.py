"""
Constants and Enum used by the sdk
"""
import enum
import pathlib

REST_API_SUFFIX = '/api/v1'
DEFAULT_BASE_URL = 'https://app.dis.co'
DISCO_CONFIG_PATH = pathlib.Path.home() / '.disco_py'
ENV_VAR_BASE_URL_NAME = 'DISCO_BASE_URL'
ENV_VAR_EMAIL_NAME = 'DISCO_EMAIL'
ENV_VAR_PASSWORD_NAME = 'DISCO_PASSWORD'
ENV_VAR_DISABLE_PROGRESS_BAR = 'DISCO_DISABLE_PROGRESS_BAR'

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR


class JobStatus(enum.Enum):
    """Job statuses"""
    created = 'Created'
    queued = 'Queued'
    running = 'Running'
    stopping = 'Stopping'
    stopped = 'Stopped'
    failed = 'Failed'
    success = 'Success'


JOB_TERMINAL_STATES = {JobStatus.stopping, JobStatus.stopped, JobStatus.failed, JobStatus.success}


class TaskStatus(enum.Enum):
    """Task statuses"""
    created = 'Created'
    queued = 'Queued'
    running = 'Running'
    stopped = 'Stopped'
    success = 'Success'
    failed = 'Failed'


class ClusterType(enum.Enum):
    """Cluster types"""
    AWS = 'aws'
    Azure = 'azure'
    GCP = 'gcp'
    Packet = 'packet'
    OnPremise = 'onPremise'

class InstanceCost(enum.Enum):
    """Instance cost types"""
    lowCost = 'lowCost'
    guaranteed = 'guaranteed'

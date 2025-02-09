from enum import Enum


class RequestStatus(Enum):
    SUCCESS = 0,
    FAILURE_DO_NOT_RETRY = 1,
    FAILURE_RETRY_SUGGESTED = 2
    FAILURE_RETRIES_EXHAUSTED = 3
    OPERATION_FAILED_BUT_NO_LONGER_REQUIRED = 4

    def is_permanent_failure(self):
        return self.value in [RequestStatus.FAILURE_RETRIES_EXHAUSTED, RequestStatus.FAILURE_DO_NOT_RETRY]
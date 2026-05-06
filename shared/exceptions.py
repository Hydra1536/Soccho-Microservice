class SocchoException(Exception):
    pass

class IdempotencyError(SocchoException):
    """Transaction idempotency key already used."""
    status_code = 409


class IdempotencyKeyExists(IdempotencyError):
    """Transaction idempotency key already used."""
    status_code = 409


class FriendNotFound(SocchoException):
    status_code = 404


class InvalidOTP(SocchoException):
    status_code = 400


class CircuitOpen(SocchoException):
    status_code = 503


class OptimisticLockError(SocchoException):
    status_code = 409


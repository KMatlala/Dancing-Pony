from datetime import timedelta

MAX_FAILED_ATTEMPTS = 3
BLOCK_TIME = timedelta(minutes=15)

failed_attempts = {}

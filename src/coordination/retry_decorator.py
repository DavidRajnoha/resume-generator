import functools

MAX_RETRIES = 3

def retry(max_retries=MAX_RETRIES, retry_message: str = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"[{func.__name__}] Attempt {attempt}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[{func.__name__}] Error on attempt {attempt}: {e}")
                    if attempt == max_retries:
                        raise
                    if retry_message:
                        print(retry_message)
        return wrapper
    return decorator
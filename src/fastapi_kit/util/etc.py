import time
from functools import wraps


def str2bool(v):
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise NotImplementedError


def timeit(prefix: str = ""):
    from fastapi_kit.log import get_logger

    logger = get_logger()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            module_name = prefix or f"{func.__name__}, "

            logger.info(f"{module_name}time elapsed {elapsed_time:.3f} sec")
            return result

        return wrapper

    return decorator

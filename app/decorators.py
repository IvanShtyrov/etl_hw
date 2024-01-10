import time
import functools

def logger(func):
    """Логирует время выполнения функции."""
    @functools.wraps(func)
    def wrapper_logger(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__!r} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper_logger

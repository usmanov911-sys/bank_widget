import datetime
import functools


def log(filename=None):
    """
    Декоратор для записи логов выполнения функций.

    Args:
        filename (str): Если указан, логи будут записаны в этот файл.
                         Иначе вывод будет в консоль.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            func_name = f"{func.__name__}"
            message_start = f"[{timestamp}] {func_name} started"
            if filename is not None:
                with open(filename, mode="a", encoding="utf-8") as file:
                    print(message_start, file=file)
            else:
                print(message_start)

            try:
                result = func(*args, **kwargs)

                message_end = f"[{timestamp}] {func_name} ok"

            except Exception as e:
                error_type = type(e).__name__
                inputs = f"(args={args}, kwargs={kwargs})"
                message_end = f"[{timestamp}] {func_name} error: {error_type}. Inputs: {inputs}"
                raise

            finally:
                if filename is not None:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        print(message_end, file=file)
                else:
                    print(message_end)

            return result

        return wrapper

    return decorator

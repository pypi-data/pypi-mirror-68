"""
    Timeit decorator.
    This decorator will run n_times a function and output the execution times.

    More info about decorators at: https://develop.villoro.com/post/decorators

    It uses 'perf_counter' instead of 'time' since it has more precission
"""

import functools
from time import perf_counter


def time_human(x):
    """ Gets time as human readable """

    # Round time
    x = round(x, 2)

    for number, unit in [(60, "s"), (60, "min"), (24, "h"), (365, "days")]:
        if abs(x) < number:
            return f"{x:.2f} {unit}"
        x /= number
    return f"{x:.2f} years"


def timeit(func):
    """
        Decorator that prints the execution time of a function. Example:

        from time import sleep

        @timeit
        def sleep_one_sec():
            sleep(1)
    """

    @functools.wraps(func)
    def timed(*args, **kwa):
        """ Prints the execution time of the decorated function """
        time0 = perf_counter()
        result = func(*args, **kwa)
        total_time = time_human(perf_counter() - time0)

        print(f"timeit: '{func.__name__}' in {total_time}")

        return result

    return timed


def timeit_out(func):
    """
        Decorator that returns both the execution time of a function and the result.

        Returns:
            result: output of the original function
            time:   total time elapsed

        Example:
            from time import sleep

            @timeit_out
            def sleep_one_sec():
                sleep(1)

            sleep_one_sec()
            out: None, 1
    """

    @functools.wraps(func)
    def timed(*args, **kwa):
        """ Calculate the execution time of the decorated function """
        time0 = perf_counter()
        result = func(*args, **kwa)
        total_time = perf_counter() - time0

        return result, total_time

    return timed


def stimeit(output_func=print):
    """
        Decorator that displays the execution time of a function.
        Allows to use custom output functions (like print, log.info...)

        Example:

        from time import sleep

        @stimeit(log.info)
        def sleep_one_sec():
            sleep(1)
    """

    def timeit_decorator(func):
        """ Decorator to time the execution of a function """

        @functools.wraps(func)
        def timed_execution(*args, **kwa):
            """ Prints the execution time of the decorated function """
            time0 = perf_counter()
            result = func(*args, **kwa)
            total_time = time_human(perf_counter() - time0)

            output_func(f"stimeit: '{func.__name__}' in {total_time}")

            return result

        return timed_execution

    return timeit_decorator


def mesure(func, *args, n_iterations=10, **kwargs):
    """ Allows to time a function n times """

    out = []
    for _ in range(n_iterations):
        time0 = perf_counter()
        func(*args, **kwargs)
        out.append(perf_counter() - time0)

    return out

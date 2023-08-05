from functools import wraps
import time

def logger(file_path):
    """log your function"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            stime = time.time()
            res = func(*args, **kwargs)
            etime = time.time()
            using_time = etime - stime
            print('using time: ', using_time)
            with open(file_path, 'a+') as f:
                f.write('Run func: {} using time {}s, with the parameters:\n\
                    {}, {}. \n\n'.format(func.__name__, using_time, args, kwargs))
            return res
        return wrapper
    return decorator



def memo(func):
    """cache the args"""
    cache = {} # 要缓存的数据
    @wraps(func)
    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        res = func(*args, **kwargs)
        cache[args] = res # 缓存f(*args))
        return res
    return wrapper



def omit_exception(*omit_args):
    """
    Simple decorator that intercepts connection
    errors and ignores these if settings specify this.
    """
    assert len(omit_args) == 1, "omit_exception decorator just recive one parameter!"
    if isinstance(omit_args[0], int):
        handle = lambda *args, **kwargs: omit_args[0]
    elif callable(omit_args[0]):
        handle = omit_args[0]
    else:
        raise TypeError("omit_parameter must be either a callable or an integer!")
    # assert callable(handle), "parameter 'method' must be a callable!"

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"there is an error '{e}'. in func:{func.__name__} with args:{args, kwargs}")
                return handle(*args, **kwargs)

                
        return wrapper
    return decorator


def retry(tries=3, delay=1):
    """Retry calling the decorated function using an exponential backoff.
    tries: if error happened try it again with 'tries' times;
    delay: error happened, try it after 'delay' seconds.
    重试三次，直到结束
    """
    def deco_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal tries
            while tries > 0:
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as e:
                    msg = f"'{e}', Retrying in {delay} seconds..."
                    print(msg)
                    time.sleep(delay)
                tries -= 1
        return wrapper  
    return deco_retry



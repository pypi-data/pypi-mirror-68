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









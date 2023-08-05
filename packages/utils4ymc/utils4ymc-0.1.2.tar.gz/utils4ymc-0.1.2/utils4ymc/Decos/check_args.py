from inspect import signature
from functools import wraps

def type_assert(*ty_args, **ty_kwargs):
    def decorator(func):
        sig = signature(func) # 取出函数func的参数
        bdtypes = sig.bind_partial(*ty_args, **ty_kwargs).arguments # 建立部分func的参形到要绑定的参数的映射
        @wraps(func)
        def wrapper(*args, **kwargs):
            for name, obj in sig.bind(*args, **kwargs).arguments.items(): # 建立部分func的形参到func输入的实参的映射
                if name in bdtypes:
                    if not isinstance(obj, bdtypes[name]):
                        raise TypeError('"%s" must be "%s"' % (name, bdtypes[name]) )
            return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    @type_assert(int, str, list)
    def test_f(a, b, c):
        print(a, b, c)

    test_f(1, 'ab', [1,2,3])
    test_f(1, 123, [1,2,3])


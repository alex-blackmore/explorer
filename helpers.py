import info

def cache(function):
    def wrapper(*args, **kwargs):
        if "output" in kwargs and kwargs["output"] == True:
            return function(*args, **kwargs)
        if (function.__name__, args) in info.cache:
            return info.cache[(function.__name__, args)]
        result = function(*args, **kwargs)
        info.cache[(function.__name__, args)] = result
        return result
    return wrapper
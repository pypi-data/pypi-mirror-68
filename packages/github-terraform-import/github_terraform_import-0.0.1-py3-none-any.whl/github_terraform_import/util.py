import os
import json

CACHE_DIR = os.path.join(os.getcwd(), ".cache")


def cache(cache_id):
    """Use the decorator over any function that returns a dictionary or json object

    If a cache file doesn't exist, creates a cache file for the result and stores result.
    If a cache file does exist, returns the cached result.

    Appends parameter values to the cache file name if the function takes a parameter.
    """
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    def decorator(loader):
        def _cache(*args, **kwargs):
            cache_file = os.path.join(CACHE_DIR, cache_id)
            cache_file += "/" if len(args[1:]) > 0 else ""
            cache_file += "/".join((str(arg) for arg in args[1:]))
            cache_file += ".json"

            cache_folder = os.path.dirname(cache_file)
            if not os.path.exists(cache_folder):
                os.makedirs(cache_folder)

            if os.path.exists(cache_file):
                with open(cache_file) as file:
                    return json.load(file)
            else:
                data = loader(*args, **kwargs)
                with open(cache_file, "w") as file:
                    json.dump(data, file)
                return data

        return _cache

    return decorator


def convert_type_to_method(type_):
    return "".join(
        ["_" + i.lower() if i.isupper() else i for i in type_.__name__]
    ).lstrip("_")

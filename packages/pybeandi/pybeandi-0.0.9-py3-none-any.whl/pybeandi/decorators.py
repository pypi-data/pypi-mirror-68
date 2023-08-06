from typing import Set, Callable, Dict

from pybeandi.model import GeneralBeanRef
from pybeandi.util import camel_case_to_snake_case


def bean(bean_id: str = None,
         profiles: Set[str] = None,
         profile_func: Callable[[Set[str]], bool] = lambda profs: True,
         **depends_on: Dict[str, GeneralBeanRef]):
    def wrapper(cls):
        cls._bean_meta = {
            'depends_on': depends_on,
            'profile_func':
                profile_func if profiles is None
                else lambda profs: profs >= profiles
        }

        if bean_id is not None:
            cls._bean_meta['id'] = bean_id
        else:
            cls._bean_meta['id'] = camel_case_to_snake_case(cls.__name__)

        return cls

    return wrapper


def after_init(**depends_on: Dict[str, GeneralBeanRef]):
    def wrapper(func):
        if not hasattr(func, '_bean_meta'):
            func._bean_meta = {}
        func._bean_meta['depends_on'] = depends_on

        return func

    return wrapper

from typing import Set, Callable, Dict

from pybeandi.model import UserGeneralBeanRef, id_ref
from pybeandi.util import camel_case_to_snake_case


def bean(bean_id: str = None,
         profiles: Set[str] = None,
         profile_func: Callable[[Set[str]], bool] = lambda profs: True,
         **depends_on: Dict[str, UserGeneralBeanRef]):
    def wrapper(cls):
        dependencies = {arg_name: (id_ref(arg_ref) if type(arg_ref) is str else arg_ref)
                        for (arg_name, arg_ref) in depends_on.items()}

        cls._bean_meta = {
            'depends_on': dependencies,
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


def after_init(**depends_on: Dict[str, UserGeneralBeanRef]):
    def wrapper(func):
        dependencies = {arg_name: (id_ref(arg_ref) if type(arg_ref) is str else arg_ref)
                        for (arg_name, arg_ref) in depends_on.items()}

        if not hasattr(func, '_bean_meta'):
            func._bean_meta = {}
        func._bean_meta['depends_on'] = dependencies

        return func

    return wrapper

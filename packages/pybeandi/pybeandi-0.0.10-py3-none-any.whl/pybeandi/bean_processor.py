from abc import ABC
from typing import Dict

from pybeandi.beans_list import BeansList
from pybeandi.model import BeanDef
from pybeandi.util import all_callable_of_object


class BeanPostProcessor(ABC):
    def post_init(self, beans: BeansList, bean_defs: Dict[str, BeanDef]):
        """
        Function that will called after context initialization
        (__init__ methods of all beans called already)
        (all beans and bean_defs filtered by profile_func)
        :param beans: BeansList object
        :param bean_defs: list of BeanDefs
        """
        pass


class AfterInitBeanPostProcessor(BeanPostProcessor):
    def post_init(self, beans: BeansList, bean_defs: Dict[str, BeanDef]):
        for bean in beans.values():
            for after_init_func in filter(
                    lambda func: '_bean_meta' in dir(func),
                    all_callable_of_object(bean)):
                beans_to_insert = {arg_name: beans[arg_bean_ref]
                                   for (arg_name, arg_bean_ref)
                                   in after_init_func._bean_meta['depends_on'].items()}
                after_init_func(**beans_to_insert)

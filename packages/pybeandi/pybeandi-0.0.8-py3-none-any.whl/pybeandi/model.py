import abc
from typing import Dict, Callable, Any, Set, Union, Type


class BeanRef:
    ref: Union[str, Type]

    def __init__(self, ref: Union[str, Type]):
        self.ref = ref


class SetBeanRef(BeanRef):
    ref: Type

    def __init__(self, ref: Type):
        super().__init__(ref)


# Type that represents any of way to identify a bean
GeneralBeanRef = Union[str, Type, BeanRef, SetBeanRef]


class BeanDef:
    def __init__(self,
                 bean_id: str,
                 bean_cls: Type,
                 factory_func: Callable[..., Any],
                 dependencies: Dict[str, BeanRef],
                 profile_func: Callable[[Set[str]], bool]):
        self.bean_cls = bean_cls
        self.profile_func = profile_func
        self.dependencies = dependencies
        self.factory_func = factory_func
        self.bean_id = bean_id


class CloseableBean(abc.ABC):
    @abc.abstractmethod
    def close_bean(self):
        pass

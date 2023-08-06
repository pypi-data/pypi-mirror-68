import abc
from dataclasses import dataclass
from typing import Dict, Callable, Any, Set, Union


class IdBeanRef:

    def __init__(self, bean_id: str):
        self.bean_id = bean_id


class WildcardBeanRef:

    def __init__(self, wildcard: str):
        self.wildcard = wildcard


class RegexBeanRef:

    def __init__(self, regex: str):
        self.regex = regex


# Aliases
id_ref = IdBeanRef
wildcard_ref = WildcardBeanRef
regex_ref = RegexBeanRef

GeneralBeanRef = Union[IdBeanRef, WildcardBeanRef, RegexBeanRef]
UserGeneralBeanRef = Union[str, GeneralBeanRef]


@dataclass
class BeanDef:
    bean_id: str
    factory_func: Callable[..., Any]
    dependencies: Dict[str, GeneralBeanRef]
    profile_func: Callable[[Set[str]], bool]


class CloseableBean(abc.ABC):
    @abc.abstractmethod
    def close_bean(self):
        pass

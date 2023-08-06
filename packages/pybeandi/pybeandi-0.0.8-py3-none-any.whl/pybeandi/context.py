import inspect
from types import ModuleType
from typing import Dict, Any, Callable, Type, Set, List

import yaml

from pybeandi.bean_processor import BeanPostProcessor, AfterInitBeanPostProcessor
from pybeandi.beans_list import BeansList
from pybeandi.errors import ContextInitError
from pybeandi.model import BeanDef, BeanRef, SetBeanRef, GeneralBeanRef, CloseableBean
from pybeandi.util import setup_yaml_env_vars


class BeanContext:
    bean_defs: List[BeanDef]
    beans: BeansList
    profiles: Set[str]
    bpps: List[BeanPostProcessor]

    closed: bool = False

    def __init__(self, bean_defs: List[BeanDef], profiles: Set[str], bpps: List[BeanPostProcessor]):
        self._bean_defs: List[BeanDef] = bean_defs
        self._beans: BeansList = BeansList()
        self._profiles = profiles
        self._bpps: List[BeanPostProcessor] = bpps

    @property
    def beans(self):
        return self._beans

    @property
    def profiles(self):
        return self._profiles

    def init(self) -> None:
        """
        Initialize context using bean definitions provided earlier
        @raise ContextInitError: is context incorrect
        """
        self._bean_defs = [bean_def for bean_def in self._bean_defs
                           if bean_def.profile_func(self.profiles)]

        bean_ids = [bean_def.bean_id for bean_def in self._bean_defs]
        duplicate_ids = set([x for x in bean_ids if bean_ids.count(x) > 1])
        if len(duplicate_ids) > 0:
            raise ContextInitError(f'Multiple beans with same id exist: {", ".join(duplicate_ids)}')

        while any((bean_def.bean_id not in self.beans for bean_def in self._bean_defs)):
            # Get all uninitialized beans
            to_init: List[BeanDef] = list(filter(
                lambda bean_def: bean_def.bean_id not in self.beans,
                self._bean_defs))

            # Remove beans with unsatisfied unary dependencies
            to_init = [bean_def for bean_def in to_init
                       if all((dep_def in self.beans
                               for dep_def in bean_def.dependencies.values()
                               if type(dep_def) is BeanRef))]
            # Remove beans with unsatisfied set dependencies
            to_init = [bean_def for bean_def in to_init
                       if all((self._all_beans_of_class_ready(dep_def.ref)
                               for dep_def in bean_def.dependencies.values()
                               if type(dep_def) is SetBeanRef))]

            if len(to_init) == 0:
                raise ContextInitError(f'Circular or missing dependency was founded')

            for bean_def in to_init:
                bean = bean_def.factory_func(**{arg_name: self.beans[arg_bean_ref]
                                                for (arg_name, arg_bean_ref)
                                                in bean_def.dependencies.items()})
                self.beans._add_as_bean(bean_def.bean_id, bean)

        for bean_processor in self._bpps:
            bean_processor.post_init(self.beans, self._bean_defs)

    def close(self):
        for closeable_bean in filter(
                lambda bean: isinstance(bean, CloseableBean),
                self.beans.values()):
            closeable_bean.close_bean()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        self.close()

    def _all_beans_of_class_ready(self, cls: Type) -> bool:
        return all((dep_cls_def.bean_id in self.beans for dep_cls_def in self._bean_defs
                    if dep_cls_def.bean_cls is cls))


class BeanContextBuilder:
    def __init__(self):
        self.bean_defs: List[BeanDef] = []
        self.profiles = set()
        self.bpps: List[BeanPostProcessor] = [
            AfterInitBeanPostProcessor()
        ]

    def init(self) -> BeanContext:
        ctx = BeanContext(self.bean_defs, self.profiles, self.bpps)
        ctx.init()
        return ctx

    def load_yaml(self, file_path: str) -> None:
        """
        Load configuration from specified file
        @param file_path: YAML config file
        """

        loader = setup_yaml_env_vars(yaml.SafeLoader)

        with open(file_path, 'r', encoding='utf-8') as file:
            conf_raw = yaml.load(file, loader)
            if 'pybeandi' not in conf_raw:
                return
            conf = conf_raw['pybeandi']

            if 'profiles' in conf and 'active' in conf['profiles']:
                for profile in conf['profiles']['active']:
                    self.profiles.add(profile)
            if 'beans' in conf:
                for bean in conf['beans'].items():
                    bean_id, bean_obj = bean
                    self.add_as_bean(bean_id, bean_obj)

    def import_module(self, module: ModuleType):
        """
        Imports all declared beans from module
        :param module: module with beans (usually module is import <module_name> object)
        """
        for name, member in inspect.getmembers(
                module,
                lambda m: (inspect.isclass(m) or callable(m)) and '_bean_meta' in vars(m)):
            self.register_bean_by_class(member)

    def register_bean(self,
                      bean_id: str,
                      bean_cls: Type,
                      factory_func: Callable[..., Any],
                      dependencies: Dict[str, GeneralBeanRef],
                      profile_func: Callable[[Set[str]], bool] = lambda profs: True) -> None:
        """
        Register bean to be created at init phase
        @param bean_id: id of registered bean
        @param bean_cls: class of bean
        @param factory_func: function or class that returns object of bean
        @param dependencies: dictionary of names of factory_func arg to reference to bean
        @param profile_func: function that returns do context need to create bean
        """
        dependencies = {dep_id: (dep_ref if isinstance(dep_ref, BeanRef) else BeanRef(dep_ref))
                        for (dep_id, dep_ref) in dependencies.items()}
        self.bean_defs.append(BeanDef(bean_id, bean_cls, factory_func, dependencies, profile_func))

    def register_bean_by_class(self, cls: Type) -> None:
        """
        Register bean to be created at init phase by class
        Class must be decorated by @bean first!
        @param cls: class of bean
        """
        self.register_bean(
            cls._bean_meta['id'],
            cls,
            cls,
            cls._bean_meta['depends_on'],
            cls._bean_meta['profile_func']
        )

    def add_as_bean(self, bean_id: str, bean_obj: Any):
        self.register_bean(bean_id, type(bean_obj), lambda: bean_obj, {})

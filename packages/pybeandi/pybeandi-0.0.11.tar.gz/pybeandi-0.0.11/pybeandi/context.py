import fnmatch
import inspect
import re
from types import ModuleType
from typing import Dict, Any, Callable, Type, Set, List

import yaml

from pybeandi.bean_processor import BeanPostProcessor, AfterInitBeanPostProcessor
from pybeandi.beans_list import BeansList
from pybeandi.config import Configuration
from pybeandi.errors import ContextInitError
from pybeandi.model import BeanDef, CloseableBean, IdBeanRef, WildcardBeanRef, RegexBeanRef, id_ref, UserGeneralBeanRef
from pybeandi.util import setup_yaml_env_vars


class BeanContext:
    bean_defs: Dict[str, BeanDef]
    beans: BeansList
    profiles: Set[str]
    bpps: List[BeanPostProcessor]

    closed: bool = False

    def __init__(self, bean_defs: Dict[str, BeanDef], profiles: Set[str], bpps: List[BeanPostProcessor]):
        self._bean_defs: Dict[str, BeanDef] = bean_defs
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
        self._bean_defs = {bean_id: bean_def for (bean_id, bean_def) in self._bean_defs.items()
                           if bean_def.profile_func(self.profiles)}

        while any(bean_id not in self.beans for bean_id in self._bean_defs):
            # Get all uninitialized beans
            to_init: List[BeanDef] = [bean_def for (bean_id, bean_def) in self._bean_defs.items()
                                      if bean_id not in self.beans]

            to_init = self._filter_by_unary_dependencies(to_init)
            to_init = self._filter_by_wildcard_dependencies(to_init)
            to_init = self._filter_by_regex_dependencies(to_init)

            if len(to_init) == 0:
                raise ContextInitError(f'Circular or missing dependency was founded')

            for bean_def in to_init:
                beans_to_insert = {arg_name: self.beans[arg_bean_ref]
                                   for (arg_name, arg_bean_ref)
                                   in bean_def.dependencies.items()}
                bean = bean_def.factory_func(**beans_to_insert)
                self.beans._add_as_bean(bean_def.bean_id, bean)

        for bean_processor in self._bpps:
            bean_processor.post_init(self.beans, self._bean_defs)

    def _filter_by_unary_dependencies(self, to_init: List[BeanDef]):
        return [bean_def for bean_def in to_init if all(
            dep_ref.bean_id in self.beans
            for dep_ref in bean_def.dependencies.values()
            if type(dep_ref) is IdBeanRef)]

    def _filter_by_wildcard_dependencies(self, to_init: List[BeanDef]):
        return [bean_def for bean_def in to_init if all(
            all(bean_id in self.beans
                for bean_id
                in fnmatch.filter(self._bean_defs.keys(), dep_ref.wildcard))
            for dep_ref
            in bean_def.dependencies.values()
            if type(dep_ref) is WildcardBeanRef)]

    def _filter_by_regex_dependencies(self, to_init: List[BeanDef]):
        return [bean_def for bean_def in to_init if all(
            all(bean_id in self.beans
                for bean_id
                in (bean_id
                    for bean_id
                    in self._bean_defs.keys()
                    if re.match(dep_ref.regex, bean_id)))
            for dep_ref
            in bean_def.dependencies.values()
            if type(dep_ref) is RegexBeanRef)]

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


class BeanContextBuilder:
    def __init__(self):
        self._scanned: Set = set()
        self.bean_defs: List[BeanDef] = []
        self.profiles = set()
        self.bpps: List[BeanPostProcessor] = [
            AfterInitBeanPostProcessor()
        ]

    def init(self) -> BeanContext:
        # Check id duplication
        bean_defs = [bean_def for bean_def in self.bean_defs
                     if bean_def.profile_func(self.profiles)]

        bean_ids = [bean_def.bean_id for bean_def in bean_defs]
        duplicate_ids = set([x for x in bean_ids if bean_ids.count(x) > 1])
        if len(duplicate_ids) > 0:
            raise ContextInitError(f'Multiple beans with same id exist: {", ".join(duplicate_ids)}')

        bean_defs = {bean_def.bean_id: bean_def for bean_def in bean_defs}

        ctx = BeanContext(bean_defs, self.profiles, self.bpps)
        ctx.init()
        return ctx

    def load_config(self, config: Configuration):
        if config.profiles is not None:
            if not all(profile in self.profiles for profile in config.profiles):
                return
        if config.beans is not None:
            for bean_id, bean_obj in config.beans.items():
                self.add_as_bean(bean_id, bean_obj)

    def load_yaml(self, file_path: str) -> None:
        """
        Load configuration from specified file
        @param file_path: YAML config file
        """

        loader = setup_yaml_env_vars(yaml.SafeLoader)

        with open(file_path, 'r', encoding='utf-8') as file:
            for yaml_raw in yaml.load_all(file, loader):
                if 'pybeandi' not in yaml_raw:
                    return
                config_raw = yaml_raw['pybeandi']

                config = Configuration.from_dict(config_raw)
                self.load_config(config)

    def import_module(self, module: ModuleType):
        """
        Imports all declared beans from module
        :param module: module with beans (usually module is import <module_name> object)
        """
        for name, member in inspect.getmembers(
                module,
                lambda m: (inspect.isclass(m) or callable(m)) and '_bean_meta' in dir(m)):
            if member in self._scanned:
                continue
            else:
                self._scanned.add(member)
            self.register_bean_by_class(member)

    def register_bean(self,
                      bean_id: str,
                      factory_func: Callable[..., Any],
                      dependencies: Dict[str, UserGeneralBeanRef],
                      profile_func: Callable[[Set[str]], bool] = lambda profs: True) -> None:
        """
        Register bean to be created at init phase
        @param bean_id: id of registered bean
        @param factory_func: function or class that returns object of bean
        @param dependencies: dictionary of names of factory_func arg to reference to bean
        @param profile_func: function that returns do context need to create bean
        """
        dependencies = {arg_name: (id_ref(arg_ref) if type(arg_ref) is str else arg_ref)
                        for (arg_name, arg_ref) in dependencies.items()}

        self.bean_defs.append(BeanDef(bean_id, factory_func, dependencies, profile_func))

    def register_bean_by_class(self, cls: Type) -> None:
        """
        Register bean to be created at init phase by class
        Class must be decorated by @bean first!
        @param cls: class of bean
        """
        self.register_bean(
            cls._bean_meta['id'],
            cls,
            cls._bean_meta['depends_on'],
            cls._bean_meta['profile_func']
        )

    def add_as_bean(self, bean_id: str, bean_obj: Any):
        self.register_bean(bean_id, lambda: bean_obj, {})

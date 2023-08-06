import inspect
from typing import Any, Type, Set, Dict, Union

from pybeandi.errors import NoSuchBeanError, MultipleBeanInstancesError, BeanIdAlreadyExistsError
from pybeandi.model import SetBeanRef, BeanRef, GeneralBeanRef


class BeansList:
    """
    Readonly dictionary-like object to access beans
    """

    def __init__(self, beans=None):
        if beans is None:
            beans = {}
        self._beans = beans

    def get_beans_set(self, bean_ref: SetBeanRef) -> Set[Any]:
        """
        Return set of beans with :bean_ref.ref: class or its subclass
        :param bean_ref: Bean reference instance
        :return: set of beans
        """
        return set(self.get_beans_set_by_class(bean_ref.ref).values())

    def get_beans_set_by_class(self, cls: Type) -> Dict[str, Any]:
        """
        Return dictionary of {bean id : bean object} with :cls: class or its subclass
        :param cls: class or superclass of beans
        :return: dictionary of {bean id : bean object}
        """
        return {bean_id: bean for (bean_id, bean) in self._beans.items() if issubclass(type(bean), cls)}

    def get_bean_by_id(self, bean_id: str) -> Any:
        """
        Return bean from context by its id
        @param bean_id: id of bean
        @return: bean
        @raise NoSuchBeanError: if such bean does not exist
        """
        if bean_id not in self._beans:
            raise NoSuchBeanError(f'Bean with id \'{bean_id}\' does not exist')
        return self._beans[bean_id]

    def get_bean_by_class(self, cls: Type) -> Any:
        """
        Return bean from context by its class
        @param cls: class of bean
        @return: bean
        @raise NoSuchBeanError: if such bean does not exist
        @raise MultipleBeanInstancesError: if more than one beans exist that satisfied given reference
        (for example multiple instances of class or it subclasses)
        """
        beans = self.get_beans_set_by_class(cls)
        if len(beans) == 0:
            raise NoSuchBeanError(f'Bean of class \'{cls.__name__}\' does not exist')
        elif len(beans) > 1:
            raise MultipleBeanInstancesError(f'There are more than one instances of class \'{cls.__name__}\': '
                                             f'{", ".join(beans.keys())}')
        return list(beans.values())[0]

    def _add_as_bean(self, bean_id: str, obj: Any) -> None:
        """
        Register obj as bean
        @param bean_id: id of new bean
        @param obj: object to register as a bean
        """
        if bean_id in self._beans:
            raise BeanIdAlreadyExistsError(f'Bean with id \'{bean_id}\' already exists')
        self._beans[bean_id] = obj

    def values(self):
        return self._beans.values()

    def ids(self):
        return self._beans.keys()

    def items(self):
        return self._beans.items()

    def __contains__(self, bean_ref: GeneralBeanRef):
        """
        Checks do bean exists by its reference
        @param bean_ref: reference
        @return: do bean exists
        """

        try:
            self[bean_ref]
        except NoSuchBeanError:
            return False
        except MultipleBeanInstancesError:
            return True
        return True

    def __getitem__(self, bean_ref: GeneralBeanRef) -> Union[Any, Set[Any]]:
        """
        General method that returns beans by any type of reference (id, class, BeanRef instance)
        :param bean_ref: id, class or BeanRef instance
        :return: bean or set of beans, depends on :bean_ref:
        """
        if type(bean_ref) is str or inspect.isclass(bean_ref):
            bean_ref = BeanRef(bean_ref)

        if type(bean_ref) is BeanRef:
            if type(bean_ref.ref) is str:
                return self.get_bean_by_id(bean_ref.ref)
            if inspect.isclass(bean_ref.ref):
                return self.get_bean_by_class(bean_ref.ref)
        if type(bean_ref) is SetBeanRef:
            return self.get_beans_set(bean_ref)
        raise ValueError('Provided bean reference is illegal (check its type)')

    def __len__(self):
        return len(self._beans)

    def __iter__(self):
        return iter(self._beans)

    def __str__(self):
        return str(self._beans)

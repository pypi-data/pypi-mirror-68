class BeanFindingError(RuntimeError):
    pass


class NoSuchBeanError(BeanFindingError):
    pass


class MultipleBeanInstancesError(BeanFindingError):
    pass


class BeanIdAlreadyExistsError(RuntimeError):
    pass


class ContextInitError(RuntimeError):
    pass

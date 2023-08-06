from pybeandi.decorators import bean, after_init
from pybeandi.model import id_ref, wildcard_ref, regex_ref


@bean(bean_id='bean_with_inject', profiles={'class_based'},
      id_num_1=id_ref('1'),
      wildcard_nums=wildcard_ref('[123]'),
      regex_nums=regex_ref(r'^[1-3]$'))
class ClassInjectBean:
    def __init__(self, id_num_1, wildcard_nums, regex_nums, default_none=None):
        assert id_num_1 == 1
        assert wildcard_nums == regex_nums == {1, 2, 3}
        assert default_none is None

        self.default_none = default_none
        self.regex_nums = regex_nums
        self.wildcard_nums = wildcard_nums
        self.id_num_1 = id_num_1

    @after_init(
        id_num_1=id_ref('1'),
        wildcard_nums=wildcard_ref('[123]'),
        regex_nums=regex_ref(r'^[1-3]$'))
    def after_init(self, id_num_1, wildcard_nums, regex_nums, default_none=None):
        assert self.id_num_1 == id_num_1
        assert self.wildcard_nums == wildcard_nums
        assert self.regex_nums == regex_nums
        assert self.default_none == default_none is None


@bean(bean_id='bean_with_inject', profiles={'func_based'},
      id_num_1=id_ref('1'),
      wildcard_nums=wildcard_ref('[123]'),
      regex_nums=regex_ref(r'^[1-3]$'))
def func_inject_bean(id_num_1, wildcard_nums, regex_nums, default_none=None):
    assert id_num_1 == 1
    assert wildcard_nums == regex_nums == {1, 2, 3}
    assert default_none is None

    return 'func'

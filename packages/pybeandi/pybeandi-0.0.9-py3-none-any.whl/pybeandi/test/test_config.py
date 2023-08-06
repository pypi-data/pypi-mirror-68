import sys

import pytest

from pybeandi.config import Configuration
from pybeandi.context import BeanContextBuilder
from pybeandi.errors import ContextInitError


CONFIG_1 = Configuration(['profile1'], {'message': 'Message from profile1'})
CONFIG_2 = Configuration(['profile2'], {'message': 'Message from profile2'})


def test_ctx_config_without_profile(ctx_builder: BeanContextBuilder):
    ctx_builder.load_config(CONFIG_1)
    ctx_builder.load_config(CONFIG_2)
    with ctx_builder.init() as ctx:
        assert 'message' not in ctx.beans


def test_ctx_config_with_profile1(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('profile1')
    ctx_builder.load_config(CONFIG_1)
    ctx_builder.load_config(CONFIG_2)
    with ctx_builder.init() as ctx:
        assert 'message' in ctx.beans
        assert ctx.beans['message'] == 'Message from profile1'


def test_ctx_config_with_both_profiles(ctx_builder: BeanContextBuilder):
    ctx_builder.profiles.add('profile1')
    ctx_builder.profiles.add('profile2')
    ctx_builder.load_config(CONFIG_1)
    ctx_builder.load_config(CONFIG_2)
    with pytest.raises(ContextInitError):
        with ctx_builder.init() as ctx:
            pass

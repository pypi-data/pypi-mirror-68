from aleksis.core.templatetags.data_helpers import get_dict


def test_get_dict_object():
    class _Foo(object):
        bar = 12

    assert _Foo.bar == get_dict(_Foo, "bar")


def test_get_dict_dict():
    _foo = {"bar": 12}

    assert _foo["bar"] == get_dict(_foo, "bar")


def test_get_dict_list():
    _foo = [10, 11, 12]

    assert _foo[2] == get_dict(_foo, 2)


def test_get_dict_invalid():
    _foo = 12

    assert get_dict(_foo, "bar") is None

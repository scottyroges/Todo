from app.utils.attrdict import AttrDict


class MockClass(object):
    def __init__(self):
        self.prop = "prop"


def test_attrdict():
    mock = MockClass()
    obj = AttrDict({
        "attr_num": 1,
        "attr_str": "test",
        "attr_boolean": True,
        "attr_class": mock,
        "attr_dict": {
            "prop": "prop"
        },
        "attr_list": [1]
    })
    assert obj.attr_num == 1
    assert obj.attr_str == "test"
    assert obj.attr_boolean is True
    assert obj.attr_class == mock
    assert obj.attr_class.prop == "prop"
    assert obj.attr_dict["prop"] == "prop"
    assert obj.attr_list[0] == 1


def test_attrdict_attr_dne():
    obj = AttrDict({
        "attr_1": 1
    })
    assert obj.attr_2 is None


def test_attrdict_attr_dne():
    obj = AttrDict({
        "attr_1": 1
    })
    assert obj.attr_2 is None


def test_attrdict_set_attr():
    obj = AttrDict({
        "attr_1": 1
    })
    obj.attr_2 = 2
    assert obj.attr_2 == 2


def test_empty_dict():
    obj = AttrDict({})
    assert obj is not None


def test_nested_dict():
    obj = AttrDict({
        "nest": AttrDict({
            "prop1": 1
        })
    })
    assert obj.nest is not None
    assert obj.nest.prop1 == 1
    assert obj.nest.prop2 is None

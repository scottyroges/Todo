from app.utils.helper_methods import to_camel_case


class TestCamelCase(object):
    def test_camel_case(self):
        assert to_camel_case("test_case") == "testCase"

    def test_camel_case_multi(self):
        assert to_camel_case("test_case_again") == "testCaseAgain"

    def test_camel_case_single(self):
        assert to_camel_case("test") == "test"

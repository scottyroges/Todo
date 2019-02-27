from unittest.mock import patch, mock_open

from app.config import file_project_path, Config


def test_file_project_path(mocker):
    mocker.patch("os.path.abspath", return_value="/root/project/config.json")
    assert file_project_path("test.txt") == "/root/project/test.txt"
    assert file_project_path("nest/test.txt") == "/root/project/nest/test.txt"


# def test_config_get():
#     fake_file = '{"prop1":"prop"}'
#
#     with patch("builtins.open", mock_open(read_data=fake_file)):
#         config = Config()
#         assert config.get("prop1") == "prop"
#
#
# def test_config_no_config():
#     fake_file = '{"prop1":"prop"}'
#
#     with patch("builtins.open", mock_open(read_data=fake_file)):
#         config = Config()
#         assert config.get("prop2") is None

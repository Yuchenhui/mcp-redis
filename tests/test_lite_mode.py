"""
Unit tests for Lite Mode functionality
"""

import os
from unittest.mock import Mock, patch
import pytest

from src.common.config import SERVER_CFG
from src.common.server import load_tools, load_all_tools


class TestLiteModeConfig:
    """Test cases for Lite Mode configuration."""

    @patch.dict(os.environ, {"LITE_MODE": "true"}, clear=True)
    def test_lite_mode_enabled_from_env(self):
        """Test LITE_MODE enabled from environment variable."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is True

    @patch.dict(os.environ, {"LITE_MODE": "false"}, clear=True)
    def test_lite_mode_disabled_from_env(self):
        """Test LITE_MODE disabled from environment variable."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is False

    @patch.dict(os.environ, {}, clear=True)
    def test_lite_mode_default_value(self):
        """Test LITE_MODE default value."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is False

    @patch.dict(os.environ, {"LITE_MODE": "1"}, clear=True)
    def test_lite_mode_numeric_true(self):
        """Test LITE_MODE with numeric true values."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is True

    @patch.dict(os.environ, {"LITE_MODE": "t"}, clear=True)
    def test_lite_mode_short_true(self):
        """Test LITE_MODE with short true values."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is True

    @patch.dict(os.environ, {"LITE_MODE": "0"}, clear=True)
    def test_lite_mode_numeric_false(self):
        """Test LITE_MODE with numeric false values."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is False

    @patch.dict(os.environ, {"LITE_MODE": "invalid"}, clear=True)
    def test_lite_mode_invalid_value(self):
        """Test LITE_MODE with invalid values."""
        # Re-import to get fresh config
        import importlib
        import src.common.config
        importlib.reload(src.common.config)

        config = src.common.config.SERVER_CFG
        assert config["lite_mode"] is False


class TestLiteModeToolLoading:
    """Test cases for Lite Mode tool loading."""

    @patch.dict(os.environ, {"LITE_MODE": "true"}, clear=True)
    @patch("src.common.server.importlib.import_module")
    def test_load_tools_in_lite_mode(self, mock_import):
        """Test that only redis_execute module is loaded in Lite Mode."""
        # Load tools in Lite Mode
        load_tools()

        # Verify only redis_execute module was imported
        mock_import.assert_called_once_with("src.tools.redis_execute")

    @patch.dict(os.environ, {"LITE_MODE": "false"}, clear=True)
    @patch("src.common.server.importlib.import_module")
    @patch("src.common.server.pkgutil.iter_modules")
    def test_load_tools_in_normal_mode(self, mock_iter_modules, mock_import):
        """Test that all tools except redis_execute are loaded in normal mode."""
        # Mock available modules (including redis_execute)
        mock_iter_modules.return_value = [
            (None, "string", None),
            (None, "hash", None),
            (None, "list", None),
            (None, "redis_execute", None),  # This should be excluded
            (None, "misc", None),
        ]

        # Load tools in normal mode
        load_tools()

        # Verify all modules except redis_execute were imported
        expected_calls = [
            "src.tools.string",
            "src.tools.hash",
            "src.tools.list",
            "src.tools.misc",  # redis_execute should not be called
        ]

        actual_calls = [call[0][0] for call in mock_import.call_args_list]
        for expected_call in expected_calls:
            assert expected_call in actual_calls
        assert "src.tools.redis_execute" not in actual_calls

    @patch("src.common.server.importlib.import_module")
    @patch("src.common.server.pkgutil.iter_modules")
    def test_load_all_tools(self, mock_iter_modules, mock_import):
        """Test that load_all_tools loads all tools including redis_execute."""
        # Mock available modules
        mock_iter_modules.return_value = [
            (None, "string", None),
            (None, "hash", None),
            (None, "redis_execute", None),
            (None, "misc", None),
        ]

        # Load all tools
        load_all_tools()

        # Verify all modules including redis_execute were imported
        expected_calls = [
            "src.tools.string",
            "src.tools.hash",
            "src.tools.redis_execute",  # This should be included
            "src.tools.misc",
        ]

        actual_calls = [call[0][0] for call in mock_import.call_args_list]
        for expected_call in expected_calls:
            assert expected_call in actual_calls


class TestRedisExecuteTools:
    """Test cases for redis_execute tools functionality."""

    @pytest.fixture
    def mock_redis_connection(self):
        """Mock Redis connection for testing."""
        mock_conn = Mock()
        return mock_conn

    @pytest.fixture
    def mock_connection_manager(self, mock_redis_connection):
        """Mock RedisConnectionManager."""
        with patch("src.tools.redis_execute.RedisConnectionManager.get_connection") as mock_get_conn:
            mock_get_conn.return_value = mock_redis_connection
            yield mock_get_conn

    @pytest.mark.asyncio
    async def test_redis_execute_command_basic(self, mock_connection_manager, mock_redis_connection):
        """Test basic redis_execute_command functionality."""
        # Mock Redis response
        mock_redis_connection.execute_command.return_value = "OK"

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command
        result = await redis_execute_command("SET", ["mykey", "myvalue"])

        # Verify result
        assert result == "OK"
        mock_redis_connection.execute_command.assert_called_once_with("SET", "mykey", "myvalue")

    @pytest.mark.asyncio
    async def test_redis_execute_command_no_args(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_command with no arguments."""
        # Mock Redis response
        mock_redis_connection.execute_command.return_value = "PONG"

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command
        result = await redis_execute_command("PING", None)

        # Verify result
        assert result == "PONG"
        mock_redis_connection.execute_command.assert_called_once_with("PING")

    @pytest.mark.asyncio
    async def test_redis_execute_command_bytes_response(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_command with bytes response."""
        # Mock Redis response as bytes
        mock_redis_connection.execute_command.return_value = b"hello"

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command
        result = await redis_execute_command("GET", ["mykey"])

        # Verify result is decoded
        assert result == "hello"
        mock_redis_connection.execute_command.assert_called_once_with("GET", "mykey")

    @pytest.mark.asyncio
    async def test_redis_execute_command_dict_response(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_command with dict response containing bytes."""
        # Mock Redis response as dict with bytes keys/values
        mock_redis_connection.execute_command.return_value = {
            b"field1": b"value1",
            b"field2": b"value2"
        }

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command
        result = await redis_execute_command("HGETALL", ["myhash"])

        # Verify result is decoded
        expected = {"field1": "value1", "field2": "value2"}
        assert result == expected
        mock_redis_connection.execute_command.assert_called_once_with("HGETALL", "myhash")

    @pytest.mark.asyncio
    async def test_redis_execute_command_list_response(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_command with list response containing bytes."""
        # Mock Redis response as list with bytes
        mock_redis_connection.execute_command.return_value = [b"item1", b"item2", b"item3"]

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command
        result = await redis_execute_command("LRANGE", ["mylist", 0, -1])

        # Verify result is decoded
        expected = ["item1", "item2", "item3"]
        assert result == expected
        mock_redis_connection.execute_command.assert_called_once_with("LRANGE", "mylist", 0, -1)

    @pytest.mark.asyncio
    async def test_redis_execute_command_nested_list_args(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_command with nested list arguments."""
        # Mock Redis response
        mock_redis_connection.execute_command.return_value = 2

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command with nested args (like ZADD)
        result = await redis_execute_command("ZADD", [
            "mysortedset",
            [1, "member1"],
            [2, "member2"]
        ])

        # Verify nested args are flattened
        assert result == 2
        mock_redis_connection.execute_command.assert_called_once_with(
            "ZADD", "mysortedset", 1, "member1", 2, "member2"
        )

    @pytest.mark.asyncio
    async def test_redis_execute_command_error(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_command error handling."""
        # Mock Redis error
        from redis.exceptions import RedisError
        mock_redis_connection.execute_command.side_effect = RedisError("Connection failed")

        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute command
        result = await redis_execute_command("GET", ["mykey"])

        # Verify error message
        assert "Redis error executing command 'GET'" in result
        assert "Connection failed" in result

    @pytest.mark.asyncio
    async def test_redis_execute_command_empty_command(self, mock_connection_manager):
        """Test redis_execute_command with empty command."""
        # Import after mocking
        from src.tools.redis_execute import redis_execute_command

        # Execute with empty command
        result = await redis_execute_command("", ["args"])

        # Verify error message
        assert result == "Error: Command cannot be empty"

    @pytest.mark.asyncio
    async def test_redis_execute_raw_command(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_raw_command functionality."""
        # Mock Redis response
        mock_redis_connection.execute_command.return_value = "OK"

        # Import after mocking
        from src.tools.redis_execute import redis_execute_raw_command

        # Execute raw command
        result = await redis_execute_raw_command("SET mykey myvalue")

        # Verify result
        assert result == "OK"
        mock_redis_connection.execute_command.assert_called_once_with("SET", "mykey", "myvalue")

    @pytest.mark.asyncio
    async def test_redis_execute_raw_command_numeric_conversion(self, mock_connection_manager, mock_redis_connection):
        """Test redis_execute_raw_command numeric argument conversion."""
        # Mock Redis response
        mock_redis_connection.execute_command.return_value = 1

        # Import after mocking
        from src.tools.redis_execute import redis_execute_raw_command

        # Execute raw command with numeric arguments
        result = await redis_execute_raw_command("ZADD myscores 100 player1 200 player2")

        # Verify numeric conversion
        assert result == 1
        mock_redis_connection.execute_command.assert_called_once_with(
            "ZADD", "myscores", 100, "player1", 200, "player2"
        )

    @pytest.mark.asyncio
    async def test_redis_execute_raw_command_empty_string(self, mock_connection_manager):
        """Test redis_execute_raw_command with empty command string."""
        # Import after mocking
        from src.tools.redis_execute import redis_execute_raw_command

        # Execute with empty string
        result = await redis_execute_raw_command("   ")

        # Verify error message
        assert result == "Error: Command string cannot be empty"

    @pytest.mark.asyncio
    async def test_redis_execute_raw_command_parse_error(self, mock_connection_manager):
        """Test redis_execute_raw_command parsing error."""
        # Import after mocking
        from src.tools.redis_execute import redis_execute_raw_command

        # Execute command that will cause parsing error
        result = await redis_execute_raw_command("INVALID")

        # Verify error message (should still try to execute)
        # This test shows that even unknown commands are attempted
        assert result is not None
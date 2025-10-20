[根目录](../../CLAUDE.md) > **tests**

# Tests 模块 - 测试套件

## 模块职责

Tests 模块提供完整的测试套件，包括单元测试、集成测试和工具测试，确保 Redis MCP Server 的功能正确性和稳定性。

## 入口与启动

### 测试配置 (`conftest.py`)
测试套件的核心配置文件，提供所有测试需要的 fixtures：
```python
@pytest.fixture
def mock_redis_connection_manager():
    """Mock the RedisConnectionManager to return a mock Redis connection."""

@pytest.fixture
def redis_config():
    """Sample Redis configuration for testing."""

@pytest.fixture(autouse=True)
def reset_connection_manager():
    """Reset the RedisConnectionManager singleton before each test."""
```

### 测试运行方式
```bash
# 运行所有测试
uv run pytest

# 运行特定类型测试
uv run pytest -m unit
uv run pytest -m integration

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

## 对外接口

### 测试标记系统
- **unit**: 单元测试，测试单个函数或类
- **integration**: 集成测试，测试组件间交互
- **slow**: 运行时间较长的测试

### 核心测试组件

#### 主应用测试 (`test_main.py`)
- `RedisMCPServer` 类测试
- CLI 参数解析测试
- 启动日志验证测试

#### 连接管理测试 (`test_connection.py`)
- Redis 连接建立测试
- 连接池管理测试
- SSL/TLS 连接测试
- 集群模式连接测试

#### 配置管理测试 (`test_config.py`)
- Redis URI 解析测试
- 环境变量配置测试
- CLI 参数覆盖测试
- 配置优先级测试

#### 工具测试 (`tools/test_*.py`)
每个工具模块都有对应的测试文件：
- `test_string.py`: 字符串操作测试
- `test_hash.py`: 哈希操作测试
- `test_list.py`: 列表操作测试
- `test_set.py`: 集合操作测试
- `test_sorted_set.py`: 有序集合操作测试
- `test_stream.py`: 流操作测试
- `test_json.py`: JSON 操作测试
- `test_pub_sub.py`: 发布订阅测试
- `test_redis_query_engine.py`: 向量搜索测试
- `test_server_management.py`: 服务器管理测试

#### 集成测试 (`test_integration.py`)
- 端到端 MCP 协议测试
- 多工具协作测试
- 实际 Redis 连接测试

## 关键依赖与配置

### 测试依赖
```python
# 测试框架
import pytest
import pytest_asyncio
import pytest_mock

# Mock 工具
from unittest.mock import Mock, patch

# Redis 相关
import redis
from redis.exceptions import ConnectionError, RedisError, TimeoutError

# 测试工具
from click.testing import CliRunner
```

### 测试配置要求
- **最低覆盖率**: 80%
- **测试路径**: `tests/` 目录
- **测试发现**: `test_*.py` 文件模式
- **异步支持**: pytest-asyncio

## 数据模型

### Mock 数据模型
```python
@pytest.fixture
def sample_vector():
    """Sample vector for testing vector operations."""
    return [0.1, 0.2, 0.3, 0.4, 0.5]

@pytest.fixture
def sample_json_data():
    """Sample JSON data for testing."""
    return {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "swimming"],
    }
```

### 错误场景模型
```python
@pytest.fixture
def redis_error_scenarios():
    """Common Redis error scenarios for testing."""
    return {
        "connection_error": ConnectionError("Connection refused"),
        "timeout_error": TimeoutError("Operation timed out"),
        "generic_error": RedisError("Generic Redis error"),
        "auth_error": RedisError("NOAUTH Authentication required"),
    }
```

## 测试与质量

### 测试策略
1. **隔离性**: 每个测试都重置连接管理器
2. **Mock 使用**: 使用 mock 对象避免真实 Redis 依赖
3. **错误覆盖**: 测试所有重要的错误场景
4. **异步支持**: 正确测试异步工具函数

### 质量保证
- **代码覆盖率**: 使用 pytest-cov 生成覆盖率报告
- **类型检查**: mypy 静态类型检查
- **代码风格**: black 自动格式化
- **代码质量**: ruff 代码质量检查

### CI/CD 集成
- GitHub Actions 自动运行测试
- 覆盖率报告自动生成
- 多 Python 版本测试支持

## 常见问题 (FAQ)

### Q: 如何测试需要真实 Redis 连接的功能？
A: 使用 `@pytest.mark.integration` 标记，并在 CI 环境中运行 Redis 服务。

### Q: 如何处理异步测试？
A: 使用 `pytest-asyncio` 插件，测试函数使用 `async def` 声明。

### Q: Mock Redis 连接的最佳实践？
A: 使用 `mock_redis_connection_manager` fixture，确保每个测试都有干净的 mock 环境。

### Q: 如何测试向量搜索功能？
A: 使用 `mock_numpy_array` 和 `mock_numpy_frombuffer` fixtures 模拟 numpy 操作。

## 相关文件清单

| 文件 | 测试范围 | 主要测试内容 |
|------|----------|-------------|
| `conftest.py` | 全局配置 | Fixtures, 测试标记, 配置 |
| `test_main.py` | 主应用 | RedisMCPServer, CLI, 启动流程 |
| `test_server.py` | MCP服务器 | 工具加载, 服务器初始化 |
| `test_connection.py` | 连接管理 | Redis连接, SSL, 集群模式 |
| `test_config.py` | 配置管理 | URI解析, 环境变量, 参数优先级 |
| `test_logging_utils.py` | 日志工具 | 日志配置, 输出格式 |
| `test_integration.py` | 集成测试 | 端到端测试, 多工具协作 |
| `tools/test_*.py` | 工具测试 | 各个Redis操作的单元测试 |

## 测试统计

### 当前测试覆盖
- **总测试文件**: 17 个
- **测试标记**: unit, integration, slow
- **Mock 覆盖**: 完整的 Redis 操作 mock
- **异步测试**: 支持完整的异步测试

### 覆盖率要求
- **最低覆盖率**: 80%
- **重点覆盖**: 工具函数、连接管理、配置解析
- **覆盖率工具**: pytest-cov

## 变更记录 (Changelog)

### 2025-10-20 15:14:26 - 初始化测试模块文档
- 创建 tests 模块文档
- 分析测试结构和策略
- 文档化测试配置和fixtures
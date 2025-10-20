# Redis MCP Server - 项目总览

## 项目愿景

Redis MCP Server 是一个为 AI 智能体应用设计的自然语言接口，旨在通过 MCP (Model Context Protocol) 客户端高效管理和搜索 Redis 数据。它使 AI 驱动的工作流能够与 Redis 中的结构化和非结构化数据进行交互。

## 架构总览

### 技术栈
- **语言**: Python 3.10+
- **框架**: FastMCP (Model Context Protocol)
- **数据库**: Redis (支持单实例和集群模式)
- **主要依赖**: redis, numpy, click, dotenv

### 核心架构
- **服务层**: 基于 FastMCP 的异步 MCP 服务器
- **连接管理**: 单例模式的 Redis 连接管理器，支持 SSL/TLS 和集群
- **工具模块**: 按数据类型分组的 Redis 操作工具集
- **配置系统**: 灵活的配置管理，支持环境变量和命令行参数

### 模块结构图

```mermaid
graph TD
    A["(根) Redis MCP Server"] --> B["src"];
    A --> C["tests"];

    B --> D["common"];
    B --> E["tools"];
    B --> F["main.py"];
    B --> G["version.py"];

    D --> H["server.py<br/>MCP服务器核心"];
    D --> I["config.py<br/>配置管理"];
    D --> J["connection.py<br/>Redis连接管理"];
    D --> K["logging_utils.py<br/>日志工具"];

    E --> L["string.py<br/>字符串操作"];
    E --> M["hash.py<br/>哈希操作"];
    E --> N["list.py<br/>列表操作"];
    E --> O["set.py<br/>集合操作"];
    E --> P["sorted_set.py<br/>有序集合操作"];
    E --> Q["stream.py<br/>流操作"];
    E --> R["json.py<br/>JSON操作"];
    E --> S["pub_sub.py<br/>发布订阅"];
    E --> T["redis_query_engine.py<br/>向量搜索"];
    E --> U["server_management.py<br/>服务器管理"];
    E --> V["misc.py<br/>杂项操作"];
    E --> AA["redis_execute.py<br/>通用命令工具"];

    C --> W["test_*.py<br/>单元测试"];
    C --> X["tools/test_*.py<br/>工具测试"];
    C --> Y["conftest.py<br/>测试配置"];

    click H "./src/common/CLAUDE.md" "查看 common 模块文档"
    click L "./src/tools/CLAUDE.md" "查看 tools 模块文档"
    click W "./tests/CLAUDE.md" "查看 tests 模块文档"
```

## 模块索引

| 模块路径 | 职责描述 | 主要功能 |
|---------|----------|----------|
| `src/main.py` | 应用入口点 | CLI 接口，服务器启动 |
| `src/common/` | 核心基础设施 | MCP服务器、连接管理、配置、日志 |
| `src/tools/` | Redis 操作工具集 | 按数据类型分组的 Redis 操作 |
| `tests/` | 测试套件 | 单元测试和集成测试 |

## 运行与开发

### 安装和运行
```bash
# 从 PyPI 安装
pip install redis-mcp-server
redis-mcp-server --url redis://localhost:6379/0

# 开发模式
git clone https://github.com/redis/mcp-redis.git
cd mcp-redis
uv venv
source .venv/bin/activate
uv sync
uv run redis-mcp-server --help
```

### 配置方式
1. **命令行参数**: `--host`, `--port`, `--password`, `--ssl` 等
2. **环境变量**: `REDIS_HOST`, `REDIS_PORT`, `REDIS_PWD` 等
3. **Redis URI**: `redis://user:pass@host:port/db` 或 `rediss://` (SSL)

### Lite Mode 配置
Lite Mode 是一个轻量级运行模式，当启用时只保留通用的 Redis 命令执行工具，让 LLM 可以根据需求灵活调用任何 Redis 接口。

**环境变量配置**:
```bash
# 默认模式（完整功能集）
LITE_MODE=false

# Lite 模式（仅通用命令工具）
LITE_MODE=true
```

**Lite Mode 特性**:
- ✅ 默认关闭 (`LITE_MODE=false`)
- ✅ 启用时屏蔽所有内置工具（11个数据类型工具）
- ✅ 仅保留通用 Redis 命令执行工具
- ✅ 支持执行任意 Redis 命令
- ✅ 需要重启服务生效

**可用工具对比**:
| 模式 | 可用工具数量 | 工具类型 |
|------|-------------|----------|
| 正常模式 | 11+ | 按数据类型分组的专用工具 |
| Lite Mode | 2 | 通用命令执行工具 |

**Lite Mode 使用示例**:
```bash
# 启动 Lite Mode
export LITE_MODE=true
redis-mcp-server --url redis://localhost:6379/0

# 在 Lite Mode 中执行任意 Redis 命令
redis_execute_command("SET", ["mykey", "myvalue"])
redis_execute_command("HGETALL", ["myhash"])
redis_execute_command("ZADD", ["myscores", 100, "player1"])
redis_execute_raw_command("JSON.SET mydoc . '{\"name\": \"test\"}'")
```

### 开发工具
- **代码格式化**: black
- **类型检查**: mypy
- **代码质量**: ruff, bandit
- **测试**: pytest, pytest-cov, pytest-asyncio
- **安全检查**: safety

## 测试策略

### 测试分层
- **单元测试**: 测试各个工具函数和核心逻辑
- **集成测试**: 测试 Redis 连接和 MCP 协议集成
- **Mock 测试**: 使用 mock 对象模拟 Redis 连接

### 测试命令
```bash
# 运行所有测试
uv run pytest

# 运行特定测试类型
uv run pytest -m unit
uv run pytest -m integration

# 生成覆盖率报告
uv run pytest --cov=src --cov-report=html
```

### 测试覆盖率要求
- 最低覆盖率: 80%
- 重点覆盖: 工具函数、连接管理、配置解析

## 编码规范

### 代码风格
- 遵循 PEP 8 标准
- 使用 black 进行自动格式化
- 使用 ruff 进行代码质量检查
- 使用 mypy 进行静态类型检查

### 错误处理
- 所有 Redis 操作都要捕获 `RedisError`
- 提供清晰的错误消息
- 使用适当的日志级别

### 异步编程
- 所有 MCP 工具都是异步函数
- 使用 `async/await` 语法
- 正确处理异步异常

## AI 使用指引

### 项目特点
- 这是一个 MCP (Model Context Protocol) 服务器
- 为 AI 智能体提供 Redis 数据操作能力
- 支持自然语言查询和数据操作

### 关键设计模式
- **工具注册**: 使用 `@mcp.tool()` 装饰器注册工具
- **连接管理**: 单例模式管理 Redis 连接
- **配置优先级**: CLI 参数 > 环境变量 > 默认值

### 常见开发任务
1. **添加新的 Redis 工具**: 在 `src/tools/` 目录创建新模块
2. **修改连接逻辑**: 更新 `src/common/connection.py`
3. **添加配置选项**: 修改 `src/common/config.py`
4. **更新测试**: 在 `tests/` 目录添加对应测试
5. **Lite Mode 开发**: 通用命令工具位于 `src/tools/redis_execute.py`

### 集成场景
- **Claude Desktop**: 作为 MCP 服务器集成
- **OpenAI Agents SDK**: 提供 Redis 数据访问能力
- **VS Code Copilot**: 通过 MCP 协议集成
- **自定义 AI 应用**: 通过 stdio 接口集成

## 变更记录 (Changelog)

### 2025-10-20 15:14:26 - 初始化文档
- 创建根级 CLAUDE.md 文档
- 分析项目架构和模块结构
- 生成模块结构图和索引
- 创建各模块的详细文档

### 2025-10-20 15:20:00 - Lite Mode 功能添加
- 添加 LITE_MODE 环境变量支持
- 实现动态工具过滤机制
- 创建通用 Redis 命令执行工具
- 更新文档和使用说明

### 项目版本信息
- 当前版本: 0.3.4
- Python 要求: >=3.10
- MCP 协议版本: 1.9.4+
# LiteMode 优化执行计划

## 任务概述
对 MCP Redis 工具进行优化，增加 liteMode 环境变量功能

## 需求背景
- 添加 `liteMode` 环境变量，默认 `false`
- liteMode=true 时：屏蔽所有内置工具，仅保留通用 Redis 命令执行工具
- liteMode 切换需要重启服务
- 采用方案A：提供通用 Redis 命令执行工具
- 不需要安全控制机制

## 技术方案
采用"方案 1：动态工具过滤"
- 在服务器启动时检查 `liteMode` 环境变量
- 根据 liteMode 值决定注册哪些工具
- 保留一个通用的 `redis_execute_command` 工具

## 实施步骤

### 步骤 1: 创建通用 Redis 命令执行工具
**文件**: `src/tools/redis_execute.py`
**目标**: 实现可执行任意 Redis 命令的通用工具

### 步骤 2: 修改工具注册逻辑
**文件**: `src/main.py`
**目标**: 根据 liteMode 环境变量条件注册工具

### 步骤 3: 更新配置管理
**文件**: `src/common/config.py`
**目标**: 添加 LITE_MODE 配置项

### 步骤 4: 更新文档
**文件**: `CLAUDE.md`
**目标**: 添加 liteMode 功能说明

### 步骤 5: 添加测试用例
**文件**: `tests/test_lite_mode.py`
**目标**: 确保 liteMode 功能正确性

## 文件修改清单
- **新增**: `src/tools/redis_execute.py`
- **修改**: `src/main.py`, `src/common/config.py`
- **新增测试**: `tests/test_lite_mode.py`
- **更新文档**: `CLAUDE.md`

## 预期结果
- LITE_MODE=false: 所有工具可用
- LITE_MODE=true: 仅通用工具可用
- 兼容性: 默认行为不变

---
创建时间: 2025-10-20 15:20:00
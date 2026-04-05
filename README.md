# 一、项目简介

**Win Dialog Handler** 是一个 Windows 桌面对话框交互工具，基于 Python 开发，通过文件通信方式实现对 Windows 窗口的自动化操作。

**核心功能：**

| 功能 | 说明 |
|------|------|
| 获取对话框内容 | 识别并提取指定 Windows 窗口内的文本内容 |
| 获取命令提示符内容 | 读取 CMD 窗口中显示的所有文本 |
| 关闭对话框 | 按标题和序号关闭目标窗口 |
| 点击按钮 | 自动点击窗口中的指定按钮（确定/取消等） |
| 向命令提示符发送内容 | 向 CMD 窗口输入命令或文本 |
| 列出所有窗口 | 枚举桌面上的所有可见窗口标题 |

# 二、系统需求

| 项目 | 要求 |
|------|------|
| 操作系统 | Windows 10 或更高版本 |
| Python 版本 | Python 3.6+ |

**依赖包：**

```bash
pip install pywinauto uiautomation clipboard
```

| 依赖 | 用途 |
|------|------|
| `pywinauto` | Windows UI 自动化核心库 |
| `uiautomation` | UI Automation 接口支持（用于 CMD 操作） |
| `clipboard` | 剪贴板操作（用于读取 CMD 内容） |

# 三、快速开始

### 3.1 启动程序

```bash
python.exe main.py .\win_dialog_handler.txt
```

### 3.2 工作原理

程序以守护进程方式持续运行，工作流程如下：

```
┌─────────────┐     写入请求      ┌──────────────────────┐
│   用户/程序   │ ──────────────> │  win_dialog_handler  │
│             │                  │       .txt           │
│             │  <────────────── │                      │
│             │     读取响应      │                      │
└─────────────┘                  └──────────────────────┘
                                          ▲
                                          │ 每 3 秒轮询
                                          │
                                  ┌────────┴────────┐
                                  │    main.py       │
                                  │  (后台持续运行)    │
                                  └─────────────────┘
```

- **轮询间隔**：每 3 秒检查一次文件变化
- **通信格式**：JSON 格式，以 `ask: ` / `answer: ` 前缀区分请求和响应
- **编码要求**：UTF-8

# 四、API 参考

### 通信协议

**请求格式：**

```
ask: {"method": "方法名", "参数1": "值1", ...}
```

**响应格式：**

```
answer: {"result": true/false, "data": ..., "message": "错误信息"}
```

---

### 4.1 get_dialog — 获取对话框内容

获取指定标题窗口中的所有文本内容，同时返回桌面上所有窗口标题列表。

**请求：**
```json
ask: {"method": "get_dialog", "title": "新建文本文档.txt - 记事本"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 目标窗口的完整标题 |

**响应：**
```json
answer: {"result": true, "data": {"titles": ["win_dialog_handler - main.py", "新建文本文档.txt - 记事本"], "content": ["123123\r\nasdasd"]}, "message": ""}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| `result` | boolean | 是否找到匹配的窗口 |
| `data.titles` | string[] | 桌面上所有窗口的标题列表 |
| `data.content` | string[] | 匹配标题窗口的子控件文本内容 |
| `message` | string | 错误信息，成功时为空 |

---

### 4.2 get_cmd_content — 获取命令提示符内容

读取指定 CMD 窗口的显示文本（通过 Ctrl+A 全选 + Ctrl+C 复制实现）。

**请求：**
```json
ask: {"method": "get_cmd_content", "index": 0}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index` | integer | 是 | CMD 窗口序号（从 0 开始）|

**响应：**
```json
answer: {"result": true, "data": "Microsoft Windows [版本 10.0.19045.5131]\r\nC:\\Users\\xxx>", "message": ""}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| `result` | boolean | 是否成功获取 |
| `data` | string | CMD 窗口文本内容（换行符转义为 `\n`）|
| `message` | string | 错误信息 |

---

### 4.3 close_windows — 关闭窗口

关闭指定的窗口。

**请求：**
```json
ask: {"method": "close_windows", "index": 0, "title": "新建文本文档.txt - 记事本"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 要关闭的窗口标题 |
| `index` | integer | 是 | 同标题窗口的序号（从 0 开始）|

**响应：**
```json
answer: {"result": true, "message": ""}
```

---

### 4.4 click_button — 点击窗口按钮

点击目标窗口中指定文案的按钮（双击触发）。

**请求：**
```json
ask: {"method": "click_button", "index": 0, "title": "abc", "but": "确定"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 窗口标题 |
| `but` | string | 是 | 按钮文案（如："确定"、"取消"、"是"、"否"）|
| `index` | integer | 是 | 同标题窗口的序号（从 0 开始）|

**响应：**
```json
answer: {"result": true, "message": ""}
```

---

### 4.5 send_cmd_content — 向命令提示符发送内容

向指定 CMD 窗口发送按键输入（使用 `SendKeys` 实现）。

**请求：**
```json
ask: {"method": "send_cmd_content", "index": 0, "content": "echo hello\r"}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `index` | integer | 是 | CMD 窗口序号（从 0 开始）|
| `content` | string | 是 | 要发送的内容（末尾加 `\r` 可模拟回车执行）|

**响应：**
```json
answer: {"result": true, "message": ""}
```

> **提示**：在 `content` 末尾添加 `\r` 可模拟按下回车键执行命令。例如 `"dir\r"` 会立即执行 dir 命令。

---

### 4.6 list_window — 列出所有窗口标题

枚举当前桌面上所有可见窗口的标题。

**请求：**
```json
ask: {"method": "list_window"}
```

**参数：** 无

**响应：**
```json
answer: {"result": true, "data": ["win_dialog_handler - main.py", "新建文本文档.txt - 记事本"], "message": ""}
```

| 返回字段 | 类型 | 说明 |
|----------|------|------|
| `result` | boolean | 是否成功获取 |
| `data` | string[] | 所有窗口标题列表 |
| `message` | string | 错误信息 |

---

# 五、使用示例

### 示例 1：获取记事本内容

```python
# 步骤 1: 打开记事本并输入一些文字

# 步骤 2: 发送请求
write_request('{"method": "get_dialog", "title": "新建文本文档.txt - 记事本"}')

# 步骤 3: 读取响应
# answer: {"result": true, "data": {"titles": [...], "content": ["记事本中的文字内容"]}, "message": ""}
```

### 示例 2：自动化命令行操作

```python
# 1. 列出窗口，确认 CMD 已打开
write_request('{"method": "list_window"}')

# 2. 发送命令（\r 表示回车执行）
write_request('{"method": "send_cmd_content", "index": 0, "content": "dir\r"}')

# 3. 等待命令执行后，读取结果
import time; time.sleep(2)
write_request('{"method": "get_cmd_content", "index": 0}')
# answer: {"result": true, "data": "目录中的文件列表..."}
```

### 示例 3：自动处理弹窗

```python
# 1. 列出所有窗口，找到弹窗标题
write_request('{"method": "list_window"}')

# 2. 点击弹窗中的"确定"按钮
write_request('{"method": "click_button", "title": "弹窗标题", "but": "确定", "index": 0}')
# answer: {"result": true}
```

# 六、项目结构

```
win_dialog_handler/
├── main.py                 # 主程序（核心逻辑）
├── win_dialog_handler.txt  # 通信文件（请求/响应交互）
├── LICENSE.txt             # Mulan PSL v2 许可证
└── README.md               # 项目文档
```

| 文件 | 说明 |
|------|------|
| `main.py` | 主程序，包含 6 个 API 方法的实现及文件监听循环 |
| `win_dialog_handler.txt` | 通信文件，程序以此文件为媒介接收请求和返回结果 |

# 七、注意事项

1. **仅支持 Windows** — 本工具基于 `pywinauto` 和 `uiautomation`，仅可在 Windows 上运行
2. **管理员权限** — 部分系统级窗口的操作可能需要管理员权限
3. **文件编码** — 通信文件必须使用 UTF-8 编码
4. **标题精确匹配** — `title` 参数需与窗口标题完全一致（区分大小写）
5. **多同标题窗口** — 当存在多个相同标题的窗口时，用 `index`（从 0 开始）进行区分
6. **轮询延迟** — 默认每 3 秒检查一次文件变更，高频场景下会有延迟
7. **错误检查** — 务必检查返回值中的 `result` 字段判断操作是否成功
8. **CMD 操作前提** — `get_cmd_content` 和 `send_cmd_content` 依赖于 UIAutomation 的 `DocumentControl(SearchDepth=3, Name="Text Area")` 定位，需要 CMD 窗口处于正常状态

# 八、常见问题

**Q: 如何集成到自己的 Python 项目中？**
A: 通过文件读写实现进程间通信。写入 `ask:` 请求到 `win_dialog_handler.txt`，然后轮询读取 `answer:` 响应即可。

**Q: 如何知道正确的窗口标题？**
A: 先调用 `list_window` 方法获取所有窗口标题列表，从中选取目标标题。

**Q: 发送命令后为什么没有反应？**
A: 确保 `content` 字符串末尾包含 `\r` 回车字符，用于模拟按回车键执行命令。

**Q: 如何排查操作失败的原因？**
A: 查看 `message` 字段获取详细错误信息；也可直接查看控制台输出的异常堆栈。

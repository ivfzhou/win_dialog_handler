# 说明

获取Windows桌面对话框内容，和关闭对话框。

运行 `python.exe main.py .\win_dialog_handler.txt` 启动，读写文件 `win_dialog_handler_conversation.txt` 获取结果和发送操作请求。

# 例子

### 1. 获取记事本内容

1. 向文件 win_dialog_handler.txt 中最后一行写入一行数据：  
    `ask: {"method": "get_dialog", "title": "新建文本文档.txt - 记事本"}`  
    title 为对话框标题。
2. 向文件 win_dialog_handler.txt 中读取最后一行数据，结果如下：  
    `answer: {"data": { "titles": ["win_dialog_handler - main.py", "新建文本文档.txt - 记事本"], "content": ["123123\r\nasdasd"]}, "result": true}`  
    数据中 titles 是获取到的所有对话框标题，  
    与 ask 中 title 相同的对话框的内容在 content 中，  
    result 表示是否找到到请求的标题的对话框。

### 2. 获取命令提示符内容

1. 向文件 win_dialog_handler.txt 中最后一行写入一行数据：  
    `ask: {"method": "get_cmd_content", "index": 1}`  
    index 表示命令提示符次序，桌面可能有多个命令提示符。
2. 向文件 win_dialog_handler.txt 中读取最后一行数据，结果如下：  
    `answer: {"result": true, "data": "Microsoft Windows [版本 10.0.19045.5131]\r\\n(c) Microsoft Corporation。保留所有权利。\r\\n\r\\nC:\\Users\\xxx>"}`  
    data 表示命令提示符中的内容，  
    result 表示是否成功获取到。

### 3. 关闭对话框

1. 向文件 win_dialog_handler.txt 中最后一行写入一行数据：  
    `ask: {"method": "close_windows", "index": 0, "title": "新建文本文档.txt - 记事本"}`  
    title 是要关闭的对话框的标题，  
    index 是对话框的次序，同标题对话框可能有多个。
2. 向文件 win_dialog_handler.txt 中读取最后一行数据，结果如下：  
    `answer: {"result": true}`  
    result 表示是否成功关闭。

### 4. 点击对话框确认按钮

1. 向文件 win_dialog_handler.txt 中最后一行写入一行数据：  
    `ask: {"method": "click_button", "index": 0, "title": "abc", "but": "确定"}`  
    but 是点击按钮的文案，  
    title 是对话框的标题，  
    index 是对话框的次序。
2. 向文件 win_dialog_handler.txt 中读取最后一行数据，结果如下：  
    `answer: {"result": true}`  
    result 表示是否成功点击。

### 5. 向命令提示符中写入内容

1. 向文件 win_dialog_handler.txt 中最后一行写入一行数据：  
    `ask: {"method": "send_cmd_content", "index": 1, "content": "echo 'ok'\r"}`  
    content 是要写入命令提示符的内容，  
    index 是命令提示符的次序。
2. 向文件 win_dialog_handler.txt 中读取最后一行数据，结果如下：  
    `answer: {"result": true}`  
    result 表示是否成功写入。

### 6. 获取所有桌面对话框标题

1. 向文件 win_dialog_handler.txt 中最后一行写入一行数据：  
    `ask: {"method": "list_window"}`  
    content 是要写入命令提示符的内容，  
    index 是命令提示符的次序。
2. 向文件 win_dialog_handler.txt 中读取最后一行数据，结果如下：  
    `answer: {"result": true, "data": ["win_dialog_handler - main.py", "新建文本文档.txt - 记事本"]}`  
    所有标题都在 data 中，  
    result 表示是否成功获取。

# DITA Stylizer

一个用于自动格式化DITA/XML文档中中英文间距的Python工具。

## 功能特性

- 🔧 自动在中文与英文/数字之间添加空格
- 📁 支持单文件或批量处理目录
- 🔄 递归处理子目录
- 📝 支持多种编码格式（UTF-8、GBK等）
- 🎯 专门针对DITA/XML文档优化
- 📊 详细的处理日志

## 支持的文件格式

- `.xml`
- `.dita`
- `.XML`
- `.DITA`

## 安装

### 环境要求

- Python 3.6+
- beautifulsoup4

### 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 运行演示

```bash
# 查看功能演示
python "dita_xml stylizer.py"

# 或使用make命令
make demo
```

### 基本用法

```bash
# 处理单个文件
python "dita_xml stylizer.py" -i example.xml

# 处理整个目录
python "dita_xml stylizer.py" -i /path/to/directory

# 递归处理子目录
python "dita_xml stylizer.py" -i /path/to/directory -r
```

### 高级选项

```bash
# 指定文件编码
python "dita_xml stylizer.py" -i example.xml -e gbk

# 设置日志级别
python "dita_xml stylizer.py" -i example.xml --log-level DEBUG
```

### 使用Makefile (推荐)

```bash
# 安装依赖
make install

# 运行测试
make test

# 运行演示
make demo

# 代码风格检查
make lint
```

### 参数说明

- `-i, --input`: 输入文件或目录路径（必需）
- `-e, --encoding`: 文件编码，默认为utf-8
- `-r, --recursive`: 递归处理子目录
- `--log-level`: 日志级别（DEBUG, INFO, WARNING, ERROR）

## 示例

### 处理前
```xml
<p>这是一个Python程序，版本号是3.8。</p>
```

### 处理后
```xml
<p>这是一个 Python 程序，版本号是 3.8。</p>
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 更新日志

### v1.0.0
- 初始版本发布
- 支持中英文间距自动格式化
- 支持批量处理和递归处理
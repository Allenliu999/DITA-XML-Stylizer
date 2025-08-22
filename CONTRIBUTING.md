# 贡献指南

感谢你对 DITA Stylizer 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果你发现了bug或有功能建议，请：

1. 检查 [Issues](https://github.com/Allenliu999/dita-stylizer/issues) 确认问题未被报告
2. 创建新的Issue，包含：
   - 清晰的标题和描述
   - 重现步骤（如果是bug）
   - 期望的行为
   - 实际的行为
   - 环境信息（Python版本、操作系统等）

### 提交代码

1. Fork 这个仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 代码规范

- 遵循 PEP 8 Python 代码风格
- 添加适当的注释和文档字符串
- 确保代码通过现有的测试
- 为新功能添加测试用例

### 测试

在提交代码前，请确保：

```bash
# 运行基本测试
python "dita_xml stylizer.py" -i examples/sample.xml

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/Allenliu999/dita-stylizer.git
cd dita-stylizer
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行示例：
```bash
python "dita_xml stylizer.py" -i examples/sample.xml
```

## 许可证

通过贡献代码，你同意你的贡献将在 MIT 许可证下授权。
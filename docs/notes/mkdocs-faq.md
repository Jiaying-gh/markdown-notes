# MkDocs FAQ

## 基本操作

**Q: 如何直接显示 Markdown 语法而不被渲染？**

A: 使用反引号（`` ` ``，Esc 键下方）包裹内容即可。

- 单行语法：用一个反引号包裹，如 `` `**粗体**` `` 会显示为 `**粗体**` 而不是粗体。
- 多行语法：用三个反引号包裹。

**Q: MkDocs 修改后不自动刷新怎么办？**

A: 将依赖包 `click` 的版本降级到 8.2.1 即可解决：

```
pip install click==8.2.1
```

**Q: 路径中包含空格时如何处理？**

A: 用引号包裹路径，防止路径中的空格导致解析错误。

## 写作语法

**Q: 为什么 `note` 提示框没有生效？**

A: 检查 `!!!note` 中 `note` 与感叹号之间是否有空格。Admonition 的正确格式要求：`!!!` 后紧跟 `note`，**中间不能有空格**。

**Q: Reference-style 图片链接不显示？**

A: Reference-style 的图片链接不能紧挨着 alt text 所在行。链接定义必须放在最后或其他独立位置。

**Q: Definition List 中多个 term 无法正确显示？**

A: 两个 term 之间需要加空行。例如：

```markdown
term1
: definition 1

term2
: definition 2
```

**Q: Emoji 显示不出来或显示过大怎么办？**

A: 需要加载 emoji 扩展。在 `mkdocs.yml` 中配置 `pymdownx.emoji` 扩展并指定 Twemoji 作为图源。

## 注释

**Q: 如何在 Markdown 中添加不被渲染的注释？**

A: 使用 HTML 注释语法 `<!-- 注释内容 -->`，注释内容不会出现在最终页面上。快捷键为 `Ctrl + /`。

## 项目结构

**Q: `extra_css` 文件应该放在哪里？**

A: 存放 `extra_css` 文件的一级文件夹必须在 `docs` 目录下，否则 MkDocs 无法引用。例如 `docs/styles/custom.css` 是有效的，而 `styles/custom.css`（与 docs 同级）则无法被引用。

## 概念理解

**Q: Python、pip 和 MkDocs 之间是什么关系？**

A: 可以类比为：

- **Python** 是操作系统（运行环境）
- **pip** 是应用商店（包管理工具）
- **MkDocs** 是安装在系统上的应用（基于 Python 的文档工具）

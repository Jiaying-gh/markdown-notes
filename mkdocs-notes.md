## Tips
- 运行时，所在路径应与yml文件在同一层级
- docs文件夹下的所有md文件都会被渲染，除非该md文件的文件名前面是点。如".installation.md"
- index.md与README.md同时存在时，mkdocs使用index.md
- yml文件中的nav元素没有规定页面顺序的话，md文件按字母顺序排列
- nav中规定的页面名优先级最高
- nav中md文件的真实路径必须在docs_dir元素定义的路径下。
- section只是一个容器，不能关联到具体的md文件作为页面。
- 如果不懂项目的原理，遇到问题时，AI 在网上就搜不到解决方法。只能自己根据理解的项目原理解决。但AI的推理能力可以解决吗？
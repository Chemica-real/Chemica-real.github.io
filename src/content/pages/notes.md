# 学科笔记

这里是学科笔记的入口。你可以直接写 Markdown，也可以把不同学科拆成更多页面。

## LaTeX 公式示例

行内公式示例：$E = mc^2$，以及 $\nabla \cdot \mathbf{E} = \rho / \varepsilon_0$。

块级公式示例：

$$
\int_{-\infty}^{+\infty} e^{-x^2}\,dx = \sqrt{\pi}
$$

## Python 代码块

```python
from pathlib import Path

def read_notes(root: Path) -> list[str]:
    return sorted(path.stem for path in root.glob("*.md"))

print(read_notes(Path("src/content/pages")))
```

## C++ 代码块

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> data = {1, 2, 3, 4};
    for (int value : data) {
        std::cout << value * value << '\n';
    }
    return 0;
}
```

## 表格示例

| 分类 | 内容 | 状态 |
| --- | --- | --- |
| 数学 | 公式、题解、推导 | 待补充 |
| 编程 | Python、C++、算法 | 待补充 |
| 化学 | 实验、概念、笔记 | 待补充 |

> 之后你可以把这一页拆成课程索引，再从这里链接到更细的章节。

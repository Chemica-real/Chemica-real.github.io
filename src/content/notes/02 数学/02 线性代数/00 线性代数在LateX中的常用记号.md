# 线性代数在LateX中的常用记号

## 基础集合、数域

$$\mathbb{R}^n$$

> "bb" stands for "blackboard bold"
---

## 向量表示

$$\vec{a}=
\begin{pmatrix}
a_1 \\ a_2 \\ a_3
\end{pmatrix}, \quad
\vec{b}=(b_1, b_2, b_3)$$

零向量：$\vec{0}$

> 粗体亦可使用：```\pmb{}```（不改变斜体）(poor man's bold)
---

## 矩阵

### 矩阵的表示
圆括号 ```pmatrix``` (**p**arenthesis)：
$ A=\begin{pmatrix}
1 & 2 \\
3 & 4
\end{pmatrix}$

方括号 ```bmatrix``` (**b**racket)：
$ B=\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}$

大矩阵省略号：
$\begin{bmatrix}
a_{11} & \dots & a_{1n}\\
\vdots & \ddots & \vdots\\
a_{m1} & \dots & a_{mn}
\end{bmatrix}$

### 矩阵常用运算符号

| 含义 | LateX              |
| --- |--------------------|
| 矩阵转置 | $A^\mathrm{T}$     |
| 逆矩阵 | $A^{-1}$           |
| 伴随矩阵 | $A^*$              |
| 矩阵秩 | $\mathrm{rank}(A)$ |
| 迹 | $\mathrm{tr}(A)$   |

> "rm" stands for "Roman math"

---

## 行列式 ```vmatrix```
> "v" stands for "**v**ertical"

$\begin{vmatrix}
1 & 2 \\
3 & 4
\end{vmatrix}$

---

## 线性空间、子空间、维数

$\mathrm{span}\{\pmb{\alpha}_1, \pmb{\alpha}_2\}, \; \dim V, \; \ker A, \mathrm{Im}\,A$

---

## 正交

$\pmb{x} \perp \pmb{y}, \; V^\perp$

## 方程组

线性方程组：
$\begin{cases}
a_{11}x_1 + a_{12}x_2 = b_1 \\
a_{21}x_1 + a_{22}x_2 = b_2
\end{cases}$

---

## 等价、相似、合同

相似：$A \sim B$  
全等：$A \cong B$  
合同：$A \simeq B$

---

## 希腊字母

常用字母：$\alpha, \beta, \gamma, \lambda, \mu, \xi, \eta$  
加粗：$\pmb{\alpha}$
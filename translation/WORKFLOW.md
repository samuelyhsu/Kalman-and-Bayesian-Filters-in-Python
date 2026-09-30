# 翻译流程说明

本文档面向执行翻译的工具或人员（翻译服务、大模型、人工译者均可）。目标：把仓库中的 md 与 ipynb 的**正文文字**译成中文，另存为 `basename_cn.*`，代码与输出一律不变。

## 1. 目录与文件

| 路径 | 作用 |
|---|---|
| `translation/nb_translate.py` | 提取、校验、回填脚本（仅依赖 Python 3 标准库和 git） |
| `translation/src/*.txt` | 待译原文。每个源文件一个 txt，由脚本生成，**不要手改** |
| `translation/tr/*.txt` | 译文。文件名与 `src/` 中对应文件**完全相同**，由译者产出 |
| `*_cn.ipynb` / `*_cn.md` | 回填生成的最终文件，与原文件同目录 |

txt 文件名规则：仓库相对路径中的 `/` 换成 `__`，再加 `.txt`。例如 `Supporting_Notebooks/Taylor-Series.ipynb` 对应 `Supporting_Notebooks__Taylor-Series.ipynb.txt`。

## 2. 文本格式

一个 txt 由若干单元组成，每个单元以独占一行的标记开头，后面是该单元的原文：

```text
=====CELL 12=====
这里是单元 12 的正文（可多行）
=====CELL 15=====
这里是单元 15 的正文
```

- 数字是 notebook 中单元的序号，**译文必须保留同样的标记和序号**，顺序不限。
- md 文件只有一个单元 `=====CELL 0=====`，内容是整个文件。
- 译文里**缺失的单元会保留英文原文**，所以可以分批翻译。
- 不要在标记行上增删空格或字符，标记行不能翻译。

## 3. 哪些要翻译，哪些绝不能改

要翻译：标题、正文、列表、表格文字、图注、习题与解答文字、HTML 标签之间的可见文字（如 `<b>GitHub</b>` 中的 GitHub 之外的说明、`<center><h1>` 内的标题）。

必须原样保留（脚本的 `check` 会检查其中前四项）：

1. **LaTeX 公式**：`$...$`、`$$...$$` 内的所有内容，包括 `\mathbf`、`\bar` 等命令。公式里的英文下标如 `\mathtt{posterior}` 也不翻译。
2. **代码围栏** 和缩进代码块：三个反引号包起来的内容、4 空格缩进的命令与代码，包括其中的注释。
3. **URL**：`http(s)://...` 不改。
4. **美元符号数量**：译文中 `$` 的个数必须与原文一致。
5. **HTML 标签与属性**：`<img src=...>`、`<a href=...>`、`<style>` 等。只翻译标签之间的文字。
6. 行内代码 `` `x = 1` ``、函数名、变量名、库名（NumPy、FilterPy、Jupyter 等）、文件名（如 `book_plots`、`02-Discrete-Bayes.ipynb`）。
7. 参考文献条目（作者、论文标题、期刊名）保留英文；`## References` 之类的标题可以翻译。
8. 引用读者评价或他人原话的英文段落可保留英文，译文可在后面括注。
9. 许可证声明（CC BY / CC BY-NC-SA / MIT 文本）保留英文原文；可在其后追加一句中文说明译文为改编作品。

**不要做的事**：不要改代码里的注释；不要增删单元；不要合并或拆分单元；不要改链接地址（脚本会自动处理，见第 6 节）；不要修正原文的拼写或错误，除非破坏了 Markdown 语法，且必须在交付说明里列出。

## 4. 术语表

全书请统一使用下列译法（首次出现可括注英文）：

| English | 中文 |
|---|---|
| Kalman filter | 卡尔曼滤波器（泛指方法时可用“卡尔曼滤波”） |
| Bayesian filter | 贝叶斯滤波器 |
| g-h filter / alpha-beta filter | g-h 滤波器 / α-β 滤波器 |
| discrete Bayes filter | 离散贝叶斯滤波器 |
| state / state estimate | 状态 / 状态估计 |
| hidden / observable | 隐藏的 / 可观测的 |
| measurement | 测量值（动作用“测量”） |
| sensor noise / process noise | 传感器噪声 / 过程噪声 |
| process model / system model | 过程模型 / 系统模型 |
| prior / posterior | 先验 / 后验 |
| likelihood | 似然 |
| belief | 置信度（讲“信念”语境时用“信念”） |
| prediction (predict step) | 预测（预测步骤） |
| update (update step) | 更新（更新步骤） |
| residual | 残差 |
| innovation | 新息 |
| Kalman gain | 卡尔曼增益 |
| covariance / covariance matrix | 协方差 / 协方差矩阵 |
| variance / standard deviation | 方差 / 标准差 |
| Gaussian | 高斯分布（形容词用“高斯的”） |
| multivariate / univariate | 多元 / 一元 |
| probability density function (PDF) | 概率密度函数 (PDF) |
| expected value | 期望值 |
| convolution / kernel | 卷积 / 卷积核 |
| epoch | 历元 |
| system propagation | 系统传播 |
| ringing | 振铃 |
| lag error | 滞后误差 |
| unscented Kalman filter (UKF) | 无迹卡尔曼滤波器 (UKF) |
| extended Kalman filter (EKF) | 扩展卡尔曼滤波器 (EKF) |
| particle filter | 粒子滤波器 |
| smoothing / smoother | 平滑 / 平滑器 |
| adaptive filtering | 自适应滤波 |
| sigma points | sigma 点 |
| Jacobian | 雅可比矩阵 |
| Monte Carlo | 蒙特卡洛 |
| resampling | 重采样 |
| ensemble Kalman filter | 集合卡尔曼滤波器 |
| H infinity filter | H 无穷滤波器 |
| least squares | 最小二乘 |
| sensor fusion | 传感器融合 |
| Table of Contents | 目录 |

行文风格：作者用第一人称、口语化、偶尔幽默；译文保持第一人称，用自然的书面中文，不要逐词硬译。数字、单位、物理量保持与原文一致。

## 5. 执行步骤

在仓库根目录运行（Windows 与 Linux 相同）。

1. 查看进度：`python translation/nb_translate.py status`，输出 `文件 已译单元/总单元`。`src/` 已经生成；若原文有变动，先 `python translation/nb_translate.py extract` 重新生成。
2. 选一个文件，把 `translation/src/<名>.txt` 交给翻译工具，按第 3、4 节的规则翻译，把结果保存为 `translation/tr/<同名>.txt`。
3. 校验：`python translation/nb_translate.py check <源文件路径>`。输出 `errors=0` 才算通过。`untranslated_cells` 是尚未翻译的单元数。
4. 回填：`python translation/nb_translate.py build <源文件路径>`，生成同目录的 `basename_cn.ipynb`。
5. 对最终文件做抽查：用 Jupyter 打开 `_cn.ipynb`，确认公式渲染、代码单元未变。

例（第 2 章）：

```text
python translation/nb_translate.py check 02-Discrete-Bayes.ipynb
python translation/nb_translate.py build 02-Discrete-Bayes.ipynb
```

大文件建议分批：一次交给工具 10～20 个单元，分别保存，最后把各批合并为一个 `tr/*.txt`。单元之间不要重复序号。

### 待译清单（截至本文档生成时）

第 2–14 章、`Appendix-E-Ensemble-Kalman-Filters.ipynb`、`Appendix-G-Designing-Nonlinear-Kalman-Filters.ipynb` 尚未翻译。其余文件已翻译，其中 `00-Preface`、`Appendix-A`、`Appendix-B`、三个 `animations/*`、`animations/Gaussians_Animations`、`animations/particle_animate` 和 `experiments/Untitled0` 有少量单元未译（多为纯 HTML 图片标签、参考文献、邮箱、标题类单元，属有意保留）。用 `status` 查看最新数字。

## 6. 回填脚本做了什么

- 只替换 markdown（及 nbformat 3 的 heading）单元的文字；代码单元、输出、元数据、图片附件不动。未翻译的 ipynb 直接复制。
- 输出 JSON 缩进为 1 个空格、保留非 ASCII 字符，与 Jupyter 默认格式一致。
- 相对链接（`](./xx.ipynb)`、`href="./xx.ipynb"`）若目标文件存在，则自动改为指向 `xx_cn.ipynb`；`http(s)` 链接和不存在的目标保持原样。所以**译文里的链接仍按原文写**。
- 没有任何可译文字的 notebook，`build` 会原样复制为 `_cn` 副本。

## 7. 校验规则（`check`）

对每个已翻译的单元，比较译文与原文的：`$` 个数、代码围栏个数、URL、LaTeX 命令和完整公式（均保留重复次数）。任一项不同即报错并返回非零退出码。公式比较允许因译文语序调整而改变出现顺序，并忽略行尾空白；不会忽略矩阵行分隔符、数字或公式内部文字的变化。URL 提取区分 Markdown 的闭合括号与地址内部成对的括号。

这些检查不能保证译文语义正确或所有结构完整，仍需抽查最终 notebook。校验器回归测试：`python -m unittest discover -s translation -p test_nb_translate.py`。

已知的正当差异：原文 URL 本身有 Markdown 语法错误时，译者可以修正，这会触发 `urls changed`。遇到这种情况请在交付说明中写明，并在 `tr` 文件中保留修正。

已修正的原文 Markdown 瑕疵：第 5 章 CELL 14 的函数名以反引号开头、单引号结尾，译文将其规范为行内代码 `np.cov`。

## 8. 许可与署名

- README 声明文字内容为 CC BY 4.0；`00-Preface` 的页脚声明为 CC BY-NC-SA 4.0；代码为 MIT。
- 译文是改编作品：必须保留原作者（Roger R. Labbe）署名、许可证链接和来源链接，并注明已作修改。已翻译的 `README_cn.md` 与 `00-Preface_cn.ipynb` 里各有一句中文说明，可作为模板。
- 若公开分发，请遵守 NC-SA 的“非商业、相同方式共享”条款。

## 9. 给翻译工具的提示词模板

```text
你是技术书籍译者。下面是《Kalman and Bayesian Filters in Python》一章的 markdown 单元，
格式为 =====CELL n===== 标记行后跟原文。请译成简体中文，要求：
1. 保留每个 =====CELL n===== 标记行及序号，不增删单元。
2. LaTeX 公式、代码与代码围栏、行内代码、URL、HTML 标签与属性、文件名、变量名原样保留，$ 符号个数不变。
3. 术语按给定术语表统一。
4. 保持作者第一人称、口语化的语气，译文自然流畅。
5. 只输出译文，不要解释。
```

提交前请运行 `check`，并把 `errors` 不为 0 的单元逐个修回。

=====CELL 0=====
# [Python 中的卡尔曼滤波与贝叶斯滤波](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python)


卡尔曼滤波与贝叶斯滤波的入门教材。所有代码均使用 Python 编写，本书本身使用 Jupyter Notebook 写成，因此你可以在浏览器中运行并修改代码。还有什么学习方式比这更好呢？


**"Kalman and Bayesian Filters in Python" looks amazing! ... your book is just what I needed** - Allen Downey, Professor and O'Reilly author.

**Thanks for all your work on publishing your introductory text on Kalman Filtering, as well as the Python Kalman Filtering libraries. We’ve been using it internally to teach some key state estimation concepts to folks and it’s been a huge help.** - Sam Rodkey, SpaceX

（以上两段为读者评价原文，保留英文。）

点击下方的 binder 或 Azure 徽章即可在线阅读：


[![Binder](http://mybinder.org/badge.svg)](https://beta.mybinder.org/v2/gh/rlabbe/Kalman-and-Bayesian-Filters-in-Python/master)


![alt tag](https://raw.githubusercontent.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python/master/animations/05_dog_track.gif)

什么是卡尔曼滤波与贝叶斯滤波？
-----

传感器是有噪声的。世界上充满了我们想要测量和跟踪的数据与事件，但我们不能指望传感器给出完美的信息。我车里的 GPS 会报告海拔高度，每次我经过道路上的同一个位置，它报告的海拔都略有不同。我的厨房秤对同一个物体称两次，读数也会不同。

在简单的情形下，解决办法显而易见。如果秤的读数略有差异，我可以多读几次取平均值，或者换一个更准确的秤。但如果传感器噪声非常大，或者环境使数据采集变得困难，又该怎么办呢？我们可能要跟踪一架低空飞行的飞机，可能想为无人机创建自动驾驶仪，或者想确保我们的农用拖拉机播种了整块田地。我从事计算机视觉工作，需要在图像中跟踪运动物体，而计算机视觉算法给出的结果噪声很大、并不可靠。

本书将教你如何解决这类滤波问题。我会用到许多不同的算法，但它们都基于贝叶斯概率。简单来说，贝叶斯概率是根据过去的信息来判断什么情况可能为真。

如果我问你我的车此刻的朝向是多少，你会毫无头绪。你更愿意在 1° 到 360° 之间挑一个数，而猜中的概率只有 360 分之一。现在假设我告诉你，2 秒钟之前它的朝向是 243°。2 秒内我的车不可能转很大的弯，所以你可以做出准确得多的预测。你是在利用过去的信息，更准确地推断现在或未来的信息。

世界也是有噪声的。这个预测帮助你做出更好的估计，但它同样受噪声影响。我可能刚刚为了躲一只狗而刹车，或者绕开了一个坑洼。强风和路面结冰是影响我的车行驶路径的外部因素。在控制领域的文献中我们把这称为噪声，尽管你可能并不这样看待它。

贝叶斯概率还有更多内容，但你已经抓住了主要思想：知识是不确定的，我们根据证据的强度来调整自己的信念。卡尔曼滤波与贝叶斯滤波把我们对系统行为的有噪声、有限的了解，与有噪声、有限的传感器读数融合起来，得到对系统状态的最佳估计。我们的原则是绝不丢弃信息。

假设我们正在跟踪一个物体，传感器报告它突然改变了方向。它真的转向了，还是数据有噪声？这要视情况而定。如果这是一架喷气式战斗机，我们会非常倾向于相信它做了突然机动的报告。如果这是直线轨道上的一列货运火车，我们就会对这个报告打折扣。我们还会根据传感器的精度进一步修正自己的信念。我们的信念取决于过去、取决于我们对被跟踪系统的了解，也取决于传感器的特性。

卡尔曼滤波由鲁道夫·埃米尔·卡尔曼（Rudolf Emil Kálmán）发明，用来以数学上最优的方式解决这类问题。它最初用于阿波罗登月任务，此后被应用于极其广泛的领域。飞机上有卡尔曼滤波器，潜艇上有，巡航导弹上也有。华尔街用它们来跟踪市场。它们被用于机器人、物联网（IoT）传感器和实验室仪器。化工厂用它们来控制和监测反应。它们被用于医学成像，以及消除心电信号中的噪声。只要涉及传感器和/或时间序列数据，通常就会用到卡尔曼滤波器或与之相近的滤波器。

写作动机
-----

写这本书的动机，源于我想要一份对卡尔曼滤波的温和入门。我是一名软件工程师，在航空电子领域工作了近二十年，因此一直与卡尔曼滤波“擦肩而过”，却从未亲自实现过。当我转向用计算机视觉解决跟踪问题时，这个需求变得迫切起来。这个领域有一些经典教材，例如 Grewal 和 Andrews 出色的 *Kalman Filtering*。但如果你没有所需的背景知识，坐下来读其中许多书是一种令人沮丧的体验。通常前几章会飞快地掠过好几年的本科数学，轻描淡写地让你去参考伊藤（Itō）微积分之类主题的教科书，并用寥寥几段话呈现整整一学期的统计学内容。它们是高年级本科课程的好教材，也是研究人员和专业人士的宝贵参考书，但对于更随意的读者来说，读起来确实十分艰难。符号不加解释地引入，不同的书对同一个概念使用不同的术语和变量，而且这些书几乎没有例子或习题解答。我常常发现自己能看懂一个定义的文字、理解其中的数学，却不知道它描述的是什么现实世界现象。“可这到底是什么*意思*？”是我反复出现的念头。

然而，当我终于开始理解卡尔曼滤波时，我意识到其背后的概念相当直白。只要有几条简单的概率规则，再加上一些关于我们如何在日常生活中整合零散知识来解释事件的直觉，卡尔曼滤波的核心概念就是可以理解的。卡尔曼滤波以难学著称，但剥去大量形式化的术语之后，这门学问及其数学之美在我面前清晰地展现出来，我爱上了这个主题。

当我开始理解数学和理论之后，更多的困难又出现了。书或论文的作者陈述某个事实，并给出一张图作为证明。可惜，为什么这个陈述成立我并不清楚，画出那张图的方法也不明显。或者我会想：“如果 R=0，这还成立吗？”又或者作者给出的伪代码层次太高，以至于实现方式并不明显。有些书提供 Matlab 代码，但我没有那个昂贵软件包的许可证。最后，许多书在每章末尾都给出许多有用的习题。如果你想自己实现卡尔曼滤波器，这些习题是你需要理解的，但这些习题没有答案。如果你是在课堂上使用这本书，也许还说得过去，但对自学的读者来说这糟透了。我讨厌作者对我隐瞒信息，大概是为了避免课堂上的学生“作弊”。

在我看来，这一切都没有必要。当然，如果你是在为飞机或导弹设计卡尔曼滤波器，就必须彻底掌握典型卡尔曼滤波教材中的所有数学和主题。我只是想跟踪屏幕上的一幅图像，或者为一个 Arduino 项目写点代码。我想知道书中的图是怎么画出来的，并选择与作者不同的参数。我想运行仿真。我想向信号中注入更多噪声，看看滤波器表现如何。在日常代码中使用卡尔曼滤波器的机会成千上万，而这个相当直白的主题却成了火箭科学家和学者的专属领地。

我写这本书就是为了满足所有这些需求。如果你为波音编写导航计算机程序，或者为雷神设计雷达，这本书不适合你。去佐治亚理工学院、华盛顿大学之类的地方攻读高级学位吧，因为你会需要它。本书面向业余爱好者、好奇的人，以及需要对数据进行滤波或平滑的在职工程师。

本书是交互式的。虽然你可以把它当作静态内容在线阅读，但我强烈建议你按其本来的用法使用它。它是用 Jupyter Notebook 写成的，使我能把文字、数学、Python 以及 Python 的输出整合在一处。本书中的每一张图、每一份数据都是由 Python 生成的，而这些 Python 代码就在 notebook 里供你使用。想把某个参数的值加倍？点击 Python 单元格，修改参数值，然后点击“Run”。书中就会出现新的图或打印输出。

本书有习题，同时也有答案。我信任你。如果你只是需要一个答案，尽管去读答案。如果你想把这些知识内化，请在读答案之前先尝试自己实现这道习题。

本书配有支持库，用于计算统计量、绘制与滤波器相关的各种图形，以及实现我们涉及的各种滤波器。这里必须给出一个强烈的提醒：大部分代码是出于教学目的编写的。我很少选择最高效的方案（它往往会掩盖代码的意图），而且在书的前半部分我没有考虑数值稳定性。理解这一点很重要——飞机上的卡尔曼滤波器经过精心设计和实现以保证数值稳定，而朴素的实现在很多情况下并不稳定。如果你认真对待卡尔曼滤波，这本书不会是你需要的最后一本书。我的目的是向你介绍这些概念和数学，并让你达到能够读懂那些教科书的程度。

最后，本书是免费的。学习卡尔曼滤波所需书籍的费用，即便对像我这样的硅谷工程师来说也有些难以承受；我无法相信它们对于经济不景气地区的人，或者经济拮据的学生来说是负担得起的。我从 Python 这样的自由软件，以及 Allen B. Downey 那样的免费书籍（见[这里](http://www.greenteapress.com/)）中获益良多。是时候回报了。所以，本书是免费的，托管在免费的服务器上，并且只使用 IPython 和 MathJax 等免费开源的软件来制作。


## 在线阅读

本书是一组 Jupyter Notebook，这是一个基于浏览器的交互式系统，允许你在浏览器中把文字、Python 和数学结合在一起。有多种在线阅读方式，列举如下。

### binder

binder 在线提供交互式 notebook，因此你无需下载本书或安装 Jupyter，就可以在浏览器中运行和修改代码。

[![Binder](http://mybinder.org/badge.svg)](https://beta.mybinder.org/v2/gh/rlabbe/Kalman-and-Bayesian-Filters-in-Python/master)


### nbviewer

网站 http://nbviewer.org 提供一个 Jupyter Notebook 服务器，可以渲染存放在 github（或其他地方）的 notebook。渲染是在你加载本书时实时进行的。你可以使用[*这个 nbviewer 链接*](http://nbviewer.ipython.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/table_of_contents.ipynb)通过 nbviewer 访问我的书。如果你今天读了我的书，而我明天做了修改，那么明天你再回来就会看到这一改动。notebook 是静态渲染的——你可以阅读，但不能修改或运行代码。

nbviewer 似乎会比已提交的版本滞后几天，所以你读到的可能不是最新内容。


### GitHub

GitHub 能够直接渲染 notebook。查看 notebook 最快的方式就是点击上面的文件。不过，它对数学公式的渲染是错误的，如果你不只是随便翻翻本书，我不建议使用这种方式。


PDF 版本
-----

本书的 PDF 版本可在[这里](https://drive.google.com/file/d/0By_SW19c1BfhSVFzNHc0SjduNzg/view?usp=sharing&resourcekey=0-41olC9ht9xE3wQe2zHZ45A)获取。

（注：原 README 此处的链接 Markdown 语法有误，漏写了左括号，翻译时已修正。）

PDF 通常会落后于 github 上的内容，因为我不会在每次小改动后都更新它。


## 下载并运行本书

不过，本书的本意是交互式的，我建议以这种形式使用它。设置起来稍微费点事，但值得。如果你在电脑上安装 IPython 和一些支持库，然后克隆本书，你就能自己运行书中所有的代码。你可以做实验，观察滤波器对不同数据的反应，观察不同的滤波器对相同数据的反应，等等。我发现这种即时反馈既至关重要又令人振奋。你不必去猜“如果……会怎样”。试一试就知道了！

可以在命令行中运行下面的命令，从 GitHub 下载本书及其支持软件：

    git clone --depth=1 https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python.git
    pip install filterpy

IPython 生态系统的安装说明可以在安装附录中找到，见[这里](http://nbviewer.ipython.org/github/rlabbe/Kalman-and-Bayesian-Filters-in-Python/blob/master/Appendix-A-Installation.ipynb)。

软件安装完成后，你可以进入安装目录，并用下面的命令行指令运行 Jupyter notebook

    jupyter notebook

这会打开一个浏览器窗口，显示基础目录的内容。本书按章节组织，每一章包含在一个 IPython Notebook 中（这些 notebook 文件的扩展名为 .ipynb）。例如，要阅读第 2 章，请点击文件 *02-Discrete-Bayes.ipynb*。有时会有一些辅助 notebook，用于生成章节中展示的动画之类的东西。这些并不是给最终用户阅读的，但如果你好奇某个动画是怎么制作的，当然可以去看看。你可以在名为 *Supporting_Notebooks* 的文件夹中找到这些 notebook。

诚然，这是一个有些繁琐的读书界面；我是在追随其他几个把 Jupyter Notebook 重新用于生成整本书的项目。我觉得这点小小的不便换来了巨大的回报——你不必在读书时另外下载一套代码库并在 IDE 中运行，所有的代码和文字都在同一个地方。如果你想修改代码，可以这样做并立即看到改动的效果。如果你发现了 bug，可以修复它并推送回我的仓库，让全世界的人都受益。而且，你永远不会遇到传统书籍中我经常遇到的问题——书和代码彼此不同步，让你抓耳挠腮，不知道该相信哪一个。


配套软件
-----

[![Latest Version](http://img.shields.io/pypi/v/filterpy.svg)](http://pypi.python.org/pypi/filterpy)

我写了一个开源的贝叶斯滤波 Python 库，名为 **FilterPy**。我已经把这个项目发布在 Python 包索引 PyPi 上。要从 PyPi 安装，请在命令行中执行

    pip install filterpy

如果你没有 pip，可以按照这里的说明操作：https://pip.pypa.io/en/latest/installing.html。

本书中用到的所有滤波器，以及书中没有的其他滤波器，都在我的 Python 库 FilterPy 中实现，可在[这里](https://github.com/rlabbe/filterpy)获取。阅读本书并不需要下载或安装它，但你很可能会想用这个库来编写自己的滤波器。它包括卡尔曼滤波器、渐消记忆（Fading Memory）滤波器、H 无穷滤波器、扩展和无迹滤波器、最小二乘滤波器等等。它还包括一些辅助例程，用于简化某些滤波器所用矩阵的设计，以及基于卡尔曼滤波的平滑器等其他代码。


FilterPy 托管在 github 上，地址是 (https://github.com/rlabbe/filterpy)。如果你想要最新的开发版本，就需要从 github 获取一份副本，并按照你的 Python 安装的说明把它加入 Python 搜索路径。这可能让你面对一些不稳定性，因为你得到的可能不是经过测试的发布版，但作为回报，你还会得到用于测试该库的所有测试脚本。你可以查看这些脚本，从中看到许多不在 Jupyter Notebook 环境中编写和运行滤波器的例子。

在 Conda 环境中运行本书的另一种方式
----
如果你安装了 conda 或 miniconda，可以通过下面的命令创建环境

    conda env update -f environment.yml

并使用

    conda activate kf_bf

以及

    conda deactivate kf_bf

来激活和停用该环境。


问题或疑问
------

如果你有意见，可以在 GitHub 上提交 issue，这样所有人都能连同我的回复一起看到。请不要只把它当作报告 bug 的渠道。此外，我还创建了一个 gitter 聊天室，用于更随意的讨论。[![Join the chat at https://gitter.im/rlabbe/Kalman-and-Bayesian-Filters-in-Python](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rlabbe/Kalman-and-Bayesian-Filters-in-Python?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


许可证
-----
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Kalman and Bayesian Filters in Python</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python" property="cc:attributionName" rel="cc:attributionURL">Roger R. Labbe</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

（本文件是 Roger R. Labbe 所著 *Kalman and Bayesian Filters in Python* 的中文翻译，依据 CC BY 4.0 许可发布；译文为改编作品，原作者未审阅或背书。）

All software in this book, software that supports this book (such as in the the code directory) or used in the generation of the book (in the pdf directory) that is contained in this repository is licensed under the following MIT license:

The MIT License (MIT)

Copyright (c) 2015 Roger R. Labbe Jr

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.TION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

联系方式
-----

rlabbejr at gmail.com

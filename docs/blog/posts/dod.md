---
date: 2025-04-17
comments: true
categories:
    - 编程
tags: note
---

# 封装的分叉路
&emsp;&emsp;当有主观能动性地去看CppCon近年的视频后，我发现是时候提升下C++口味了。结合在实际编程中的经验，谈谈在实践中用面向对象遇到的问题，以及换一条路子到面向数据编程，于是有了这篇笔记。
<!-- more -->

# 从封装开始说起
&emsp;&emsp;还记得我有次参加研究生面试的速记员，面试官问过一个最简单而又最困难的问题：“什么是面向对象？”。坐在一边的我觉得这个问题没什么难度，甚至觉得拿来面试研究生有些不合适。直到我最近写代码时看到这样一个例子:

```c++
class D3d12Device
{
    public:
        void init()
        {
            init_debug_layer();
            init_removal_handler();
            init_d3d12_factory();
            init_d3d12_device();
        }
    protected:
        void init_debug_layer();
        void init_removal_handler();
        void init_d3d12_device();
        void init_d3d12_factory();
    private:
        ...
};

// free-function init
void init(D3d12Device& device)
{
    device.init_debug_layer();
    device.init_removal_handler();
    device.init_d3d12_factory();
    device.init_d3d12_device();
}
```
&emsp;&emsp;这是个D3D12中关于初始化的相关代码，因为每一个函数都包含了一段特有的逻辑，通常我会把他们拆分到不同函数中，最后用init函数来做流程式的初始化。类似的案例在这个视频[^1]中也有提及。那么，这样做够面向对象吗？另一种做法是把init做法提到类外部，构造成一个free-function（当然protected的方法就要放到public域中）。那么这两种init哪一种更好呢？Effective C++条款23：Prefer non-member non-friend functions to member functions。此章节中也有类似的案例，得到的结果是free function更优。给出的一个逻辑是：面向对象将数据与成员函数绑定，越少的数据被访问，意味着数据有更大的封装性，也意味着改变数据引起的改动越少。当前案例中，init成员函数虽然没有显式地去访问成员变量，但是他也拥有访问成员变量的权限，而free function的init自然无法访问到被封装的对象。从数据可见的角度上来说确实如书本所言。

```c++
class CmdSys
{
    public:
        ID3D12GraphicsCommandList* get_cmdlist();
        /* push cmdlist, execute queue, flush queue, wait queue ...*/
    private:
        ComPtr<D3D12Queue> queue_;
};
```
&emsp;&emsp;第二个案例是我在封装时遇到的不得不改的变封装程度的案例。众所周知，D3D12中存在cmdlist提交命令到cmdqueue这样的基础逻辑。那么作为一个涉足D3D12没那么深刻的我而言，cmdlist是需要在各种类或接口中存在的；而cmdqueue，作为一个接受并执行命令的抽象体，一般不需要与具体d3d12对象交互，所以我就基于这种想法，将cmdqueue只有在类内可见，也不提的get方法。在这个类中，对外提供cmdlist，每一帧的命令操作。所有事情都非常顺利，我也觉得封装地不错，直到我开始创建swapchain。swapchain创建过程中需要cmdqueue作为参数传入到d3d12 api函数中。在这种情况下，公开queue的get方法显得不够那么封装，用友元类似开了后门。总而言之，我对cmdqueue的封装在这里显得捉襟见肘。

&emsp;&emsp;上面两个案例，第一个是为了说明面向对象其实并没有那么简单，有很多理解是违反直觉的。第二个案例是为了说明，封装在遇到新需求挑战时，实际上很有可能会打破最初的设计。到此，我遇到的问题解决的方案是设计友元类工厂，起码只有在创建的时候能访问到cmdqueue, 如果后续继续遇到其他特殊情况，那就得开始考虑重构的事情了。岔开提一句，面向对象要求程序员拥有丰富的领域知识和经验，为什么还会有35岁危机呢？大概是很多岗位压根不需要设计，肯加班就行？

### 面向数据编程
&emsp;&emsp;单论我上面提到的问题，面向数据设计(DOD)确实可以解决，因为DOD的一条原则就是数据不需要“封装",数据是公开的。那么我就不需要为cmdqueue的可见性花费太多精力。引入新的方案不能管中窥豹，于是我搜集网上的资料[^2][^3][^4]。书籍[^4]我认为是不错的入门书籍，浅显易懂，虽然在数据表示方面似乎不是C++的风味。
&emsp;&emsp;DOD是一种新的编程方式，它解放了数据与成员函数间的强绑定，不在意数据的可见性，更加在乎数据的组织方式，其次是关注数据的transform。关于更多的概念和优势可以见书籍，我不再班门弄斧。但是有些原则我记录在下方，供你我参考：

1. 分离数据与代码，数据就是数据，它存在于结构体中，用一般性的数据结构表达数据存在形式。
2. 代码或者说transform把输入映射到输出。

我未探知的DOD领域：

3. 不可变性、数据的展示形式、多线程、数据的历史可追溯性

### 总结
&emsp;&emsp;dod的权威性的概念并没有明确定义，不同的人也有不同的见解。封装可以把数据确定在一个类中，避免在程序中传来传去，提升可维护性。但是当我看到一个类中有一堆get/set简单方法时，封装薄薄的一层，不免显得过于掩耳盗铃。诚然dod在代码简洁，性能方面存在很大优势，但是它不考虑封装，那么追踪状态变化会是一个非常困难的问题。DOD在游戏行业名声挺大，我也想看看现实中用DOD作为生产开发的游戏代码，涨一涨姿势。

## 引用
[^1]: [Free your functions! - Klaus Iglberger -Meeting C++ 2017]( https://www.bilibili.com/video/BV1Li4y1t7uT/?share_source=copy_web&vd_source=26276ecdb1451e2bc36bdfba65f6dd14)
[^2]: [CppCon 2014: Mike Acton "Data-Oriented Design and C++"](https://www.bilibili.com/video/BV1VR4y1v7Z9/?share_source=copy_web&vd_source=26276ecdb1451e2bc36bdfba65f6dd14)
[^3]: [CppCon 2018: Stoyan Nikolov “OOP Is Dead, Long Live Data-oriented Design](https://www.bilibili.com/video/BV1MY411Y7tX/?share_source=copy_web&vd_source=26276ecdb1451e2bc36bdfba65f6dd14)
[^4]: [Data-Oriented Programming](https://book.douban.com/subject/35810366/)
---
date: 2024-11-30
comments: true
categories:
    - Unreal Engine
tags: note
draft: true
---

# The Road To UE
本文记录了学习UE的经历，走过一些弯路，总结出一条易于上手的过程，在此记录。
<!-- more -->


## 学习过程
1. 经历一个简单的项目，跟着抄，对UE的环境有个理解
2. 参考Lyra逻辑和功能。改造简单项目，让他符合实际良好的工程实践


### 参考材料
##### 初识UE
* [命名规则](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine)
* [InsideUE Gameplay](https://zhuanlan.zhihu.com/p/22833151)
* [上手项目](https://www.bilibili.com/video/BV1iEybYbE9p/?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click&vd_source=b7c2138ea8aa033f5b5f8039de77f0d4)

##### Lyra
* [解析系列](https://unrealdirective.com/articles/modular-game-features-what-you-need-to-know)


##### Game Features相关
* [使用教程](https://unrealdirective.com/articles/modular-game-features-what-you-need-to-know)
* [使用方法及其常见问题的解决办法](https://www.bilibili.com/opus/666746385154965521)

#### ModularGameplay相关
* [IGameFrameworkInitStateInterface](https://www.bilibili.com/opus/786865299100008497)

## 回顾

### 数据化哪些内容？为此Lyra做了什么？
&emsp;&emsp;在游戏开发过程中，数据的"权力"通常把握在策划的手中。策划同学需要去调整数据，来实现一些玩法，调整游戏数值等等。学习Lyra的过程中，它又做了哪些这方面的事情，又有哪些出彩的地方呢？


### ModularGameplay为何引入
&emsp;&emsp;UE5本身已经提供了Actor-ActorComponent来方便开发者做Gameplay开发，那为何还要再引入ModularGameplay插件呢？
简单回答：弥补功能上的缺失。ModularGameplay提供了一些功能来方便开发者做自己的开发。目前我看到的一些优点在于：提供组件初始化优化，Actor与组件辅助函数。

&emsp;&emsp;组件间初始化问题通常出现在几个组件间有依赖关系的情况。这一点在Lyra的HeroCompopnent和LyraPawnExtensionComponent两个类上表现明显。
ModularGameplay提供了IGameFrameworkInitStateInterfaces来增强组件在BeginPlay阶段的状态依赖关系。也就是通过一个发生在BeginPlay阶段的状态机模型，继承接口的组件会在同步修改状态，在状态切换的过程中，开发者可以去实现一些逻辑功能。

&emsp;&emsp;Actor与组件辅助函数。






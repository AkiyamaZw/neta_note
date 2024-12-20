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

### Experience数据化哪些内容？为此Lyra做了什么？
&emsp;&emsp;在游戏开发过程中，数据的"权力"通常把握在策划的手中。策划同学需要去调整数据，来实现一些玩法，调整游戏数值等等。Experience数据化了什么内容？

&emsp;&emsp;Experience中包含了几个方面的数据。在输入方面，引用InputConfig数据。InputConfig中有一些输入行为和GameplayTag。在角色方面，它指定了Pawn的默认蓝图。最后一个就是指定需要加载的Gameplay Feature。

&emsp;&emsp;Experience持有数据，游戏中的逻辑就是对Experience数据的加载和对象逻辑初始化（颇有DOD面向数据编程的味道）。加载Experience发生在GameMode对象InitGame函数中，整个加载的过程配合GameState的ExperienceManagerComponent来实现。而对象逻辑初始化则基本上发生在Experience加载完成后的事件回调中OnExperienceLoad中。回调函数创建了Pawn,配置了Pawn的InputConfig。基本上是对应数据内容。

|阶段|类名|作用|
|---|---|---|
|加载阶段|ExperienceManagerComponent|加载Assets,加载输入数据，加载Features|
|加载完成|GameMode| 创建Pawn |
|加载完成|ExperienceExtensionComponent|加载数据...|
|加载完成|HeroComponent|设定输入...|

&emsp;&emsp;注意在Experience加载完成之前也会创建Pawn，但是由于没有会发现没有Pawn类型（神奇的Lyra在WorldSetting中没有设定默认的Pawn类型），也没办法生成Pawn。也就是说具体的Pawn相关逻辑都延后到Experience加载完成后。







---
draft: true
date: 2024-01-22
categories:
    - CG
tags: note
---

# 图形学基础

图形学初学者最关心的一个问题便是如何在屏幕上画出一个点。用更加严谨的说法是: **将三维空间中的点(物体)映射到屏幕的像素上**。这个过程包括了线性代数的知识，也包含了对光栅化过程的理解。其中，坐标变换将3维坐标转化为投影空间中的一个点(属于\[-1, 1]^3), 而光栅化将投影空间的光栅化过程将投影空间坐标映射为屏幕空间中的像素点。对两个过程中的细节实现的理解，对初学者而言比较重要。

<!-- more -->
## 坐标变换&#x20;

所谓的坐标变换，一言以蔽之即：将一个坐标系中的点通过变换矩阵转化为另一个坐标系中的点, 做坐标系变换的初衷是：一方面我们需要直观的世界坐标，另一方面，世界需要有观察者视角(相机)。两者的相关数据我们都想要，那么坐标系变换在所难免。

如果把3D坐标上的点转换为像素的过程类比为一次拍照过程，我们能够联想到下面的流程来实现:

1.  将所有人安排到指定地点，摆好pos (Model Transform)
2.  找个完美的位置放置相机，对准人群（View Transform)
3.  按下快门，把相机看到的保存到一张相片中(Projection Transform & Viewport Transform)

模型变换(Model Transform), 即将模型的从模型空间转换到世界空间。模型空间通常是建模者规定的坐标系。将模型加载到游戏中，模型需要具备世界坐标相关属性，通过Model Transform来实现。

视角变换(View Transform), 即定义了从世界坐标到观察空间的变换。这里约定俗成的作风便是，将观察者定义在观察空间的原点，观察者看向-Z方向，以+Y方向为向上方向。视角变换的矩阵计算是通过将世界空间中的相机位移到世界空间原点，且坐标轴对齐的矩阵转置来实现的。通过获得视角变换，我们可以将变换施加到其他3D空间坐标点上，得到的结果即在观察空间中的坐标。又因为只要相机和其他物体坐标相对位置没有变化，在不同坐标系下也依然不会有变化。

投影变换(Projection Transform), 定义了从相机空间到“标准视体积”(canonical view volume, 即一个取值范围在\[-1, 1]^3之间的一个空间立方体)。该过程定义了相机空间中能被“看”到的范围，并且将这个范围压缩到一个规范化的范围之间。这一步主要进行的操作有2步，第一位移，第二缩放。位移是把定义的canoical view volume移动到相机空间坐标原点，缩放是将整个volume的大小压成一个立方体。上述描述的做法其实是类*正交投影*的处理方式，人类视觉上是一种叫作透视投影的一种投影变换方式。透视投影的volume被称作视锥体，具备近大远小的视觉特点。透视投影可以通过变形“正交投影”来实现，若记正交投影矩阵为 $M_{oth}$, 记透视投影到正交投影的变换矩阵为$M_{pes2oth}$ ，则透视投影的可以记为$M_{pes} = M_{oth} * M_{pes2oth}$。更多具体的计算见虎书*Chapter.7 Viewing*。

## 光栅化
光栅化的过程可以看作是对于canonical view volumn中可绘制点映射到屏幕空间上. 所谓屏幕空间，即一个2D的像素空间。

### 走样与反走样
这个过程是对3D可绘制点的一次采样，使得被采样的点能够显示在电子屏幕上。采样的过程和算法会影响最终呈现的效果。
用数字图像处理学科的逻辑来说，采样容易出现走样，比如锯齿。对于走样，通常的反走样技术的逻辑是先模糊，后采样。先做模糊的出发点是降低图片中高频部分，也即一些像素值剧烈变化的点，这些点通常是物体的边缘。做一次模糊后，边缘的分界面变化不会过大，宏观看上去也就相对不会有"毛刺"出现.


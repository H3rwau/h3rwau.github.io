# 为什么要学习linux

无论是从个人的职业发展角度，还是从公司招聘候选人的角度来看，扎实的基础知识是很多人的诉求

### 打开 Linux 操作系统这扇门，你才是合格的软件工程师

根据 2018 年 W3Techs 的数据统计，对于服务器端，Unix-Like OS 占的比例近 70%，其中 Linux 可以称得上是中流砥柱。随着移动互联网的发展，客户端基本上以 Android 和 iOS 为主。Android 是基于 Linux 内核的，因而客户端也进入了 Linux 阵营。可以说，**在编程世界中，Linux 就是主流，不会 Linux 你就会格格不入。**

那些火得不行的技术，什么云计算、虚拟化、容器、大数据、人工智能，几乎都是基于 Linux 技术的。那些牛得不行的系统，团购、电商、打车、快递，都是部署在服务端，也几乎都是基于 Linux 技术的。

所以说，如果你想进大公司，想学新技术，Linux 一定是一道绕不过去的坎。只有进入 Linux 操作系统这扇门，你才能成为合格的软件工程师。

### 研究 Linux 内核代码，你能学到数据结构与设计模式的落地实践

Linux 最大的优点就是开源。作为程序员，有了代码，啥都好办了。只要有足够的耐心，我们就可以一层一层看下去，看内核调度函数，看内存分配过程。理论理解起来不容易，但是一行行的“if-else”却不会产生歧义。

在 Linux 内核里，你会看到数据结构和算法的经典使用案例；你甚至还会看到并发情况下的保护这种复杂场景；在实践中遇到问题的时候，你可以直接参考内核中的实现。

例如，平时看起来最简单的文件操作，通过阅读 Linux 代码，你能学到从应用层、系统调用层、进程文件操作抽象层、虚拟文件系统层、具体文件系统层、缓存层、设备 I/O 层的完美分层机制，尤其是虚拟文件系统对于接入多种类型文件系统的抽象设计，在很多复杂的系统里面，这个思想都能用得上。

再如，当你写代码的时候，大部分情况下都可以使用现成的数据结构和算法库，但是有些场景对于内存的使用需要限制到很小，对于搜索的时间需要限制到很小的时候，我们需要定制化一些数据结构，这个时候内核里面这些实现就很有参考意义了。

### 了解 Linux 操作系统生态，能让你事半功倍地学会新技术

Linux 是一个生态，里面丰富多彩。很多大牛都是基于 Linux 来开发各种各样的软件。可以这么说，只要你能想象到的技术领域，几乎都能在里面找到 Linux 的身影。

数据库 MySQL、PostgreSQL，消息队列 RabbitMQ、Kafka，大数据 Hadoop、Spark，虚拟化 KVM、Openvswitch，容器 Kubernetes、Docker，这些软件都会默认提供 Linux 下的安装、使用、运维手册，都会默认先适配 Linux。

因此，在 Linux 环境下，很容易能够找到现成的工具，这不仅会让你的工作事半功倍，还能让你有亲密接触大牛思想的机会，这对于你个人的技术进步和职业发展都非常有益。

操作系统是干什么的呢？我们都知道，一台物理机上有很多硬件，最重要的就是 CPU、内存、硬盘、网络。同时，一台物理机上也要跑很多程序，这些资源应该给谁用呢？当然是大家轮着用，谁也别独占，谁也别饿着。为了完成资源分配这件事，操作系统承担了一个“大管家”的作用。它将硬件资源分配给不同的用户程序使用，并且在适当的时间将这些资源拿回来，再分配给其他的用户进程。

鉴于操作系统这个“大管家”的角色，我设计了一个故事，将各个知识点串起来，来帮助你理解和记忆.

假设，我们现在就是在做一家外包公司，我们的目标是把这家公司做上市。其中，操作系统就是这家外包公司的老板。我们把这家公司的发展阶段分为这样几个时期：

- 初创期：这个老板基于开放的营商环境（x86 体系结构），创办一家外包公司（系统的启动）。因为一开始没有其他员工，老板需要亲自接项目（实模式）。
- 发展期：公司慢慢做大，项目越接越多（保护模式、多进程），为了管理各个外包项目，建立了项目管理体系（进程管理）、会议室管理体系（内存管理）、文档资料管理系统（文件系统）、售前售后体系（输入输出设备管理）。
- 壮大期：公司越来越牛，开始促进内部项目的合作（进程间通信）和外部公司合作（网络通信）。
- 集团化：公司的业务越来越多，会成立多家子公司（虚拟化），或者鼓励内部创业（容器化），这个时候公司就变成了集团。大管家的调度能力不再局限于一家公司，而是集团公司（Linux 集群），从而成功上市（从单机操作系统到数据中心操作系统）。

<img src="https://static001.geekbang.org/resource/image/80/5d/80a4502300dfa51c8520001c013cee5d.jpeg" style="zoom:50%;" />
## 什么是原子变量

atomic是一个类模板，在我的认知中，更愿意把它看做是一个拓展封装类，封装一个原有的类型，并拓展新的api给用户，好比share_ptr之于原生指针，适配器queue之于容器deque。

atomic也是如此，当我们写下std::atomic<int>的时候，意味着将int拓展成原子类型，将int类型的++，--等都变成原子操作，同时拓展了诸如fetch_add，fetch_sub等原子加减方法供用户使用。

我们可以先对**原子变量**下一个初步的定义：==**即某些成员方法是原子操作的对象**==。



[原子操作](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=8&q=原子操作&zhida_source=entity)和高层（编程语言层级在C以上，姑且叫它高层）代码的实现并没有关系，**哪怕 ++i 或是 i++ 在高层只是一条单独的语句，当翻译成底层代码（[汇编](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=汇编&zhida_source=entity)）的时候，就需要更多指令来完成。**

![image-20241005153016083](D:\笔记gitpage\h3rwau.github.io\library\010-计算机八股\八股.assets\image-20241005153016083.png)

原子操作的定义：**即在高层代码的一个原子操作，不论在底层是怎么实现的，有多少条指令，在底层这些指令执行期间，都不会受到其它线程或者读写任务的干扰**。

## 原子操作底层实现

我自己对原子操作的定义是，其底层的诸多指令会[被捆绑](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=被捆绑&zhida_source=entity)在一起完成，不受其它线程影响，那么具体该怎么才能实现这种捆绑呢。

加锁，这是大家最容易想到的方法，也是最简单的方法。先不说底层汇编，在高层语言解决实际的业务问题，我们需要某段代码在同一个时间只允许一个进程/线程访问，也就是[临界区](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=临界区&zhida_source=entity)，一般会lock住mutex来进入临界区，完成业务后unlock mutex来退出临界区。

但是[互斥锁mutex](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=互斥锁mutex&zhida_source=entity)有个严重的问题，就是**效率不高**，如果有两个线程t1和t2，当t1拿到了互斥锁，t2也想要这个锁，发现这个锁已经被t1占有了，t2不会在t1身边徘徊等锁，而是直接陷入[阻塞态](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=阻塞态&zhida_source=entity)，直到t1释放了锁，t2才会被唤醒，进入到就绪队列等待调度，并再次去尝试获得锁。这将会消耗大量的资源在重复的“睡眠”，“等待”，“唤醒”的操作中。

其次，在保存和恢复上下文的过程中，还会存在cache失效的可能。

![image-20241005153212262](D:\笔记gitpage\h3rwau.github.io\library\010-计算机八股\八股.assets\image-20241005153212262.png)

**为什么需要内存序的根本原因，我们利用内存序可以限制cpu对指令执行顺序的重排程度，防止单线程指令的合理重排在多线程的环境下出现顺序上的错误。**

**volatile变量**的意义在于**每次读写都会从内存读或者写内存，解决的是编译器重排的问题。**

volatile只能保证涉及每个volatile变量的代码的相对顺序不会被编译器重排，至于volatile变量的代码和其他非volatile变量的代码之间的相对顺序并不保证，且无法保证cpu不会继续重排你的代码。

但是c++11的真正atomic操作，是有内存序参数的，用于避免cpu的重排，==**可以说atomic+内存序两者叠加才真正在lock-free（免锁）情况下实现了高层代码顺序和底层代码执行顺序的统一。**==

## 内存序的区分

要理解不同的内存序，不妨从几种硬件层面的内存模型来入手，会更好理解。

**内存一致性**模型（memory consistency model）用于描述多线程对共享存储器的访问行为，在不同的内存一致性模型里，多线程对共享存储器的访问行为有非常大的差别。

- [顺序存储](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=顺序存储&zhida_source=entity)模型（强定序模型）

- 完全存储定序（TSO）

  - x86 CPU 就是这种内存模型，为了提高效率，其在L1缓存之前加了一个store buffer，因此写数据指令执行时，会先把更新后的数据放到store buffer里后立刻返回执行下一条指令，store buffer的数据则会慢慢被写到L1 cache中，如果有多条写操作指令，会严格按照FIFO的次序执行。

    但无论是否FIFO，总之store buffer的存在已经导致MESI的同步被破坏，写指令立刻返回，后续的指令（比如读操作）可能在store buffer数据还没更新到所有cache和内存之前就执行，这就会出现store-load乱序。

- 部分存储定序（PSO）

- 宽松内存模型（RMO）



## **内存序就是高层对底层cpu内存模型的一种封装**。

==c++在执行atomic操作时，传入的不同内存序参数，就是在告诉你，它会模拟上述哪一种内存模型来处理代码执行顺序。==

memory的总体分类和内存序的对应：

- **memory_order_seq_cst:**
  这是所有atomic操作内存序参数的默认值，**语义上就是要求底层提供顺序一致性模型，不存在任何重排**，可以解决一切问题，但是效率**最低**。
- **memory_order_release/acquire/consume:**
  提供release、acquire或者consume, release语意的一致性保障
  它的语义是：我们允许cpu或者编译器做一定的指令乱序重排，但是由于tso, pso的存在，可能产生的store-load乱序store-store乱序导致问题，那么涉及到多核交互的时候，就需要手动使用release, acquire去避免这样的这个问题了。简单来说就是允许大部分写操作乱序（只要不影响代码正确性的话），对于**乱序影响正确性的那些部分，程序员自己使用对应的内存序代码来控制**。
- **memory_order_relaxed:**
  这种内存序对应的就是RMO，完全放开，让编译器和cpu自由搞，很容易出问题，除非你的代码是那种不论怎么重排都不影响正确性的逻辑，那么选择**这种内存序确实能提升最大性能**。

综上，**最实用的还是memory_order_release和memory_order_acquire这两种内存序，兼顾了效率和代码的正确性。**



- memory_order_release

如果用了这种内存序，**保证在本行代码之前，有任何写内存的操作，都是不能放到本行语句之后的。**

也就是可以**让程序员可保证一段代码的写顺序**。

假设我们还是希望a=1的执行在b=2之前（对于所有共享ab的线程来说都是一致的），可以这样实现。

```c++
//-将下面代码用release控制
int a = 0;
int b = 0;
void func1(){
    a = 1;
    b = 2;
}

//------------------------------分割线-----------------------------

int a = 0;
std::atomic<int> b(0);
void func1(){
    a = 1;
    b.store(2,std::memory_order_release);//-a的写操作不会重排到b的写操作之后
}
```

- memory_order_acquire

如果用这种内存序，保证**在本行代码之后，有任何读内存的操作，都不能放到本行语句之前。**

也就是可以让程序员可保证一段代码的读顺序。

对于线程2而言，我们无法保证cout<<a<<endl;会不会重排到while(b !=2);之前，所以可以这样修改代码

```c++
int a = 0;
int b = 0;
void func1(){
    a = 1;
    b = 2;
}
void func2(){
    while(b != 2);
    cout<<a<<endl;
}

//------------------------------分割线-----------------------------

int a = 0;
std::atomic<int> b(0);
void func1(){
    a = 1;
    b.store(2,std::memory_order_release);//-a的写操作不会重排到b的写操作之后
}
void func2(){
    while(b.load(std::memory_order_acquire) != 2);
    cout<<a<<endl;//-a的读操作不会重排到b的读操作之前
}
```

## c++内存屏障

那么内存屏障是什么，简单来说，就是我们希望上述的代码在逻辑上更纯粹，我们希望a和b就是纯纯的两个非原子int，而不是让b变成原子变量来保证执行顺序。

==内存屏障就可以想象成用一个**匿名的原子变量来保证执行顺序**，不需要让b变成原子变量了==，代码如下：

```c++
int a = 0;
int b = 0;
void func1(){
    a = 1;
    std::atomic_thread_fence(std::memory_order_release);
    b = 2;
}
void func2(){
    while(b != 2);
    std::atomic_thread_fence(std::memory_order_acquire);
    cout<<a<<endl;
}
//使用release屏障，相当于写操作a=1不会重排到b之后。
//使用acquire屏障，相当于读操作cout<<a不会重排while(b !=2)之前。
//和刚刚实现了一样的功能。
```

## 对于无锁编程的理解

lock-free不能简单理解成无锁，因为本身CAS就是一个[自旋锁](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=自旋锁&zhida_source=entity)的机制，我感觉无锁和有锁更像是互斥锁和自旋锁的区别，或者说悲观锁和[乐观锁](https://zhida.zhihu.com/search?content_id=207962093&content_type=Article&match_order=1&q=乐观锁&zhida_source=entity)的区别。

在执行 i++的时候，互斥锁觉得本线程在执行汇编的三条语句时，一定会被其它线程干扰，所以干脆在i++之前就加锁，自增后解锁，代码如下：

```c++
int i;
mutex m;
void func1(){
    lock_guard<mutex> lock(m);
    i++;
}
```

atomic则是利用CAS的机制，我先判断 i 是不是=旧值，如果=旧值说明没被其它线程干扰，于是 i 更新成new_value，这就有点乐观的意思了，因为atomic优先觉得本线程是没有被其它线程干扰的，大不了compare不成功，就不更新新的值呗。
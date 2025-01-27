## 参考答案

`new`和`malloc`在C++中都用于动态内存分配，但它们之间有几个关键的区别：

1. 语法层面：
   - `new`是C++的操作符，可以直接用来分配对象或数组。
   - `malloc`是一个函数，通常需要包含头文件`<cstdlib>`，并且只分配原始内存。
2. 类型安全：
   - `new`是类型安全的，它会根据分配的对象类型进行正确的内存分配和构造函数调用。
   - `malloc` 不是类型安全的，它只分配原始内存，不调用构造函数。返回类型是 `void*`，需要强制类型转换为具体的指针类型。
3. 构造与析构：
   - 使用 `new` 分配的对象在对象生命周期结束时需要使用 `delete` 来释放，`delete` 会自动调用对象的析构函数。
   - 使用 `malloc` 分配的内存需要使用 `free` 来释放，`free` 不会自动调用析构函数，因此如果分配的是对象数组，需要手动调用析构函数。
4. 异常安全性：
   - `new`在分配失败时会抛出`std::bad_alloc`异常。
   - `malloc`在分配失败时返回`NULL`指针。
5. 管理机制：
   - C++中的`new`和`delete`通常由编译器实现，可能包含一些额外的内存管理机制。
   - C语言的`malloc`和`free`由C标准库提供，与编译器无关。

总结来说，`new`和`malloc`都是动态内存分配的手段，但`new`提供了类型安全和构造/析构的自动化，而`malloc`则提供了更底层的内存分配方式，需要手动管理构造和析构。在C++中，推荐使用`new`来分配对象，以保持类型安全和自动化的资源管理。

## 背诵版：

- `new`是C++的操作符，由编译器实现，可以直接用来分配对象或数组，并且在分配失败会抛出`std::bad_alloc`异常。 

- new表达式工作步骤有三步

  ​		**1.调用operator new库函数，分配未类型化的空间，用来保存指定类型的一个对象**，而在operator new函数中，会调用malloc函数

  ​		**2.运行该类型的构造函数初始化对象**

  ​		**3.返回指向对象的指针**

- `malloc`是一个库函数，通常需要包含头文件`<cstdlib>`，**并且只分配原始内存，分配失败时会返回NULL**。

- `new`是类型安全的，它会根据分配的对象类型进行**正确的内存分配和构造函数调用**。
- `malloc` 不是类型安全的，它**只分配原始内存，不调用构造函数**。返回类型是 `void*`，需要强制类型转换为具体的指针类型。

- 使用 `new` 分配的对象在对象生命周期结束时需要使用 `delete` 来释放，`delete` 会自动调用对象的析构函数。
- 使用 `malloc` 分配的内存需要使用 `free` 来释放，`free` 不会自动调用析构函数，因此如果分配的是对象数组，需要手动调用析构函数。

总结来说，`new`和`malloc`都是动态内存分配的手段，但`new`**提供了类型安全和构造/析构的自动化**，而`malloc`则提供了更底层的内存分配方式，需要**手动管理构造和析构**。

placement_new **允许在已经分配的内存地址上构造对象**

### 2.new和delete表达式

​	1.new表达式工作步骤

​		**1.调用operator new库函数，分配未类型化的空间，用来保存指定类型的一个对象**

​		**2.运行该类型的构造函数初始化对象**

​		**3.返回指向对象的指针**

​	2.delete表达式工作步骤

​		**1.调用析构函数，回收对象中数据成员申请资源**

​		**2.调用operator delete的标准库函数释放该对象所用的内存**



1. **malloc的底层实现是怎样的？free是怎么回收内存的？**
   答：
    1、**当开辟的空间A小于128K的时候，malloc底层调用brk()函数**，
    **brk是将数据段的最高地址指针_edata往高地址推**，_edata+30K
    只是完成虚拟地址的分配，A这块内存现在还是没有物理页与之
    对应的，等到进程第一次读写A这块内存的时候，发送缺页中断，
    这个时候，内核才会分配给A这块内存对应的物理页。也就是说，
    **如果用malloc分配了A这块内容，然后从来不访问它，那么A对应
    的物理页是不会被分配的。**
        而**当开辟的空间大于128K的时候，利用mmap系统调用**，从堆
    和栈的中间也就是**文件映射区**分配一块虚拟内存。这样做主要是因为：
        brk分配的内存需要等到高地址内存释放以后才能释放（比如
    先申请A再申请B，所以B相对于A来说是高地址空间，所以在B释放
    之前，A是不可能释放的，因为只有一个_edata指针，这就是内存
    碎片产生的原因。而mmap分配的内存可以单独释放。
    2、free回收内存时首先要知道这块内存的地址多大，所以在malloc
    返回的地址的前一小段是存在空闲内存块的链表中，存储这一块有
    多大的信息。对使用mmap机制分配空间的malloc返回的地址free时，
    直接将其对应的虚拟内存和物理内存一起释放。而对brk机制分配
    空间的malloc返回的地址free时，并不会立刻释放，默认情况下，
    当最高地址空间的空闲内存超过128K时，执行内存紧缩操作(trim)
    .所以当free之后，发现最高地址空闲内存超过128K时，就会内存
    紧缩。

2. new/delete与malloc/free的区别与联系是什么？(面试常考)
   答：
    1、malloc开辟空间类型大小需手动计算，new是由编译器自己计算。
    2、malloc返回类型为void*,必须强转成对应类型指针，而new直接
    返回对应类型指针。
    3、malloc开辟内存时返回内存地址要检查判空，因为若它可能跟开
    辟失败会返回NULL；new则不用判断，因为内存分配失败时，它会抛
    出异常bac_alloc，可以使用异常机制。
    4、无论释放几个空间大小，free只传递指针，而多个对象时，delete
    需加[]，(分配的大小是数组空间大小).
    5、malloc/free函数只是开辟空间并释放，new/delete则不仅会开辟
    空间，并调用构造函数和析构函数进行初始化和清理。
    6、new/delete底层是基于malloc/free来实现的。
    7、因为new/delete是操作符，它调用operator new/operator delete，
    它们可以被重载，在标准库里它有8个重载版本；而malloc/free不可以
    重载。
    8、对于malloc分配内存后，若在使用过程中内存分配不够或太多，这时
    可以使用realloc函数对其进行扩充或者缩小，但是new分配好的内存不能
    这样被直观简单的改变。
    9、对于malloc申请内存的位置是在堆上分配内存的；但是new申请内存
    有一个抽象概念，它为自由存储区，它可以在堆上，也可以在静态存储
    区上分配，这主要取决于operator new实现细节，取决于它在哪里为对象
    分配空间。


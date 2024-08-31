# C++学习笔记——1.命名空间、const、以及malloc与new的区别

### 1、命名空间

 1. cout标准输出

    ```c++
    //cout,标准输出
    //<<,输出流运算符
    //“Hello world”,字符串常量
    //endl end of line '\n'
    cout << "Hello world" << endl;//<<，运算符重载
    operator<<(cout, "hello, world");
    cout.operator<<(endl);
    operator<<(cout, "hello, world1").operator<<(endl);
    ```

	2. 命名空间定义

    ```c++
    #include <iostream>
    using namespace std;
    namespace wd
    {
    //命令空间里面定义的变量、函数、结构体、类等等统称为实体
    int number = 10;
    void print()
    {
        cout << "void wd::print()" << endl;
    }
    }//end of namespace wd
    int main(int argc, char **argv)
    {
        cout << "number = " << wd::number << endl;//作用域限定符
        wd::print();
        return 0;
    }
    ```

3. using编译指令

   ```c++
   #include <iostream>
   using namespace std;//1、using编译指令,一次把std命名空间里面的实体全部引出来
   namespace wd
   {
   //命令空间里面定义的变量、函数、结构体、类等等统称为实体
   int number = 10;
   void print()
   {
       cout << "void wd::print()" << endl;
   }
   }//end of namespace wd
   //弊端:可能与std里面的实体冲突
   int cout()
   {
       return 0;
   }
   int main(int argc, char **argv)
   {
       cout << "number = " << wd::number << endl;//作用域限定符
       wd::print();
       cout();
       return 0;
   }
   ```

4. 作用域限定符

   ```c++
   #include <iostream>
   /* using namespace std;//1、using编译指令,一次把std命名空间里面的实体全部引出来 */
   namespace wd
   {
   //命令空间里面定义的变量、函数、结构体、类等等统称为实体
   int number = 10;
   void print()
   {
       std::cout << "void wd::print()" << std::endl;
   }
   }//end of namespace wd
   //2、作用域限定符
   //好处：即使我们自定义的函数与std命名空间里面的实体冲突也不要紧
   //坏处：写起来麻烦
   int cout(int x, int y)
   {
       std::cout << "int cout(int, int)" << std::endl;
       std::cout << "x = " << x << ", y = " << y << std::endl;
       return 0;
   }
   int main(int argc, char **argv)
   {
       std::cout << "number = " << wd::number << std::endl;//作用域限定符
       wd::print();
       cout(10, 30);
       return 0;
   }
   ```

5. using声明机制

   ```c++
   #include <iostream>
   using std::cout;//3、using声明机制,一次只引出一个实体
   using std::endl;//推荐使用using声明机制
   namespace wd
   {
   //命令空间里面定义的变量、函数、结构体、类等等统称为实体
   int number = 10;
   void print()
   {
       cout << "void wd::print()" << endl;
   }
   }//end of namespace wd
   #if 0
   int cout(int x, int y)
   {
       std::cout << "int cout(int, int)" << std::endl;
       std::cout << "x = " << x << ", y = " << y << std::endl;
       return 0;
   }
   #endif
   int main(int argc, char **argv)
   {
       cout << "number = " << wd::number << endl;//作用域限定符
       wd::print();
       /* cout(10, 30); */
       return 0;
   }
   ```

6. 命名空间可进行扩展

   ```c++
   #include <iostream>
   using std::cout;//3、using声明机制,一次只引出一个实体
   using std::endl;//推荐使用using声明机制
   //标准命名空间也是可以进行扩展的,不大安全：可能与std里面的实体冲突
   //标准命名空间里面的实体都是小写的
   namespace std
   {
   struct MyStruct
   {
       int a;
   };
   }//end of namespace std
   #if 0
   struct A
   {
       int a;
   };
   struct A
   {
       int b;
   };
   #endif
   //命名空间是可以进行扩展的
   //带命名空间的函数声明
   namespace wd
   {
   int var = 100;
   void print();
   }
   namespace hb
   {
   int number = 20;
   void show()
   {
       cout << "void hb::show()" << endl;
   }
   void display()
   {
       cout << "void hb::display()" << endl;
       wd::print();
   }
   }//end of namespace hb
   namespace wd
   {
   //命令空间里面定义的变量、函数、结构体、类等等统称为实体
   int number = 10;
   void print()
   {
       cout << "void wd::print()" << endl;
       hb::show();
   }
   }//end of namespace wd
   int main(int argc, char **argv)
   {
       cout << "number = " << wd::number << endl;//作用域限定符
       wd::print();
       return 0;
   }
   ```

7. 匿名命名空间和嵌套命名空间

   ```c++
   #include <stdio.h>
   #include <iostream>
   using std::cout;
   using std::endl;
   int number = 1;
   namespace wd
   {
   int number = 20;
   void print(int number)
   {
       cout << "形参number = " << number << endl;
       cout << "wd::number = " << wd::number << endl;
       cout << "全局number = " << ::number << endl;//匿名命名空间
       ::printf("hello,world\n");
       printf("hello,world\n");
   }
   //命名空间的嵌套
   //访问：类似于邮局寄信的地址的写法
   namespace ll
   {
   int number = 4000;
   void show()
   {
       cout << "void wd::ll::show()" << endl;
   }
   }//end of namespace ll
   }//end of namespace wd
   int main(int argc, char **argv)
   {
       int value = 300;
       wd::print(value);
       wd::ll::show();
       return 0;
   }
   ```

### 2、const，以及const和指针的搭配

//宏定义：发生时机在预处理阶段，只是进行简单的字符串替换

const常量是发生在编译时

//如果有bug，宏定义没有做类型检查，只能到运行时候才会发现

C++ 11标准中，为了**解决 const 关键字的双重语义问题**，保留了 const 表示“只读”的语义，而将“常量”的语义划分给了新添加的 constexpr 关键字。因此 C++11 标准中，建议将 const 和 constexpr 的功能区分开，**即凡是表达“只读”语义的场景都使用 const，表达“常量”语义的场景都使用 constexpr。**

原文链接：https://blog.csdn.net/wzz953200463/article/details/116176071

```c++
#include <iostream>

using std::cout;
using std::endl;

//宏定义：发生时机在预处理阶段，只是进行简单的字符串替换
//如果有bug，只能到运行时候才会发现
#define MAX 100

void test()
{
    //内置类型：char/short/int/float/double/long/void */bool
    const int number = 10 ;//const常量在定义的时候必须初始化
    /* number = 20;//赋值，error,常量不能进行赋值，作用：保护数据 */
    int const number1 = 200;
}

//函数指针            指针函数
//int (*pf)()         int*  func()
//数组指针            指针数组
//int (*pArray)[]     int *pArray[]
//
void test1()
{
    int value1 = 10;
    int *p1 = &value1;
    *p1 = 11;
    p1 = NULL;

    int value2 = 200;
    const int *p2 = &value2;//当const在*的左边的时候，const *,常量指针(pointer to const)
    cout << "*p2 = " << *p2 << endl;
    /* *p2 = 222;//error,不能修改指针所指变量的值 */
    /* cout << "*p2 = " << *p2 << endl; */
    p2 = &value1;//ok,指针本身(指向)是可以修改的
    cout << "*p2 = " << *p2 << endl;

    cout << endl;
    int value3 = 300;
    int const *p3 = &value3;//当const在*的左边的时候，const *,常量指针(pointer to const)
    cout << "*p3= " << *p3 << endl;
    /* *p3 = 222;//error,不能修改指针所指变量的值 */
    /* cout << "*p3= " << *p3 << endl; */
    p3 = &value1;//ok,指针本身(指向)是可以修改的
    cout << "*p3= " << *p3 << endl;

    cout << endl;
    int value4 = 400;
    int * const p4 = &value4;//当const在*的右边的时候，* const ,指针常量(const pointer)
    cout << "*p4 = " << *p4 << endl;
    *p4 = 444;//ok,能修改指针所指变量的值
    cout << "*p4 = " << *p4 << endl;
    /* p4 = &value1;//error,不能修改指针本身(指向) */
    /* cout << "*p4 = " << *p4 << endl; */

    cout << endl;
    int value5 = 500;
    const int * const p5 = &value5;//const指针常量
    cout << "*p5 = " << *p5 << endl;
    /* *p5 = 555;//error,不能修改指针所指变量的值 */
    /* cout << "*p5 = " << *p5 << endl; */
    /* p5 = &value1;//error,不能修改指针本身(指向) */
    /* cout << "*p5 = " << *p5 << endl; */
}
int main(int argc, char **argv)
{
    test1();
    return 0;
}
```

### 3、malloc和new的用法区别

```c++
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

using std::cout;
using std::endl;

//Q:什么是内存泄漏？内存越界？内存踩踏？野指针?
//
//Q:malloc底层实现是什么？
//
//面试题
//malloc/free与new/delete异同点？
//相同点：1、都是用来申请堆空间
//2、都要成对出现,否则会造成内存泄漏
//不同点：1、malloc/free是C语言库函数，new/delete是C++关键字
//2、malloc申请堆空间没有进行初始化，new在申请堆空间的时候进行初始化
void test()
{
    int *pInt = (int *)malloc(sizeof(int));//1、申请空间
    memset(pInt, 0, sizeof(int));//2、初始化(清零)
    *pInt = 10;//3、赋值
    printf("*pInt = %d\n", *pInt);
    printf("pInt = %p\n", pInt);
    printf("&pInt = %p\n", &pInt);

    free(pInt);//4、释放堆空间

    int *pArray = (int *)malloc(sizeof(int) * 10);
    memset(pArray, 0, sizeof(int) * 10);//2、初始化(清零)
    pArray[0] = 10;//3、赋值

    printf("pArray[0] = %d\n", pArray[0]);
    free(pArray);
}
void test1()
{
    int *pInt = new int(10);//1、申请空间，进行初始化和赋值
    cout << "*pInt = " << *pInt << endl;

    delete pInt;//2、释放堆空间

    int *pArray = new int[10]();
    cout << "*pArray[0] = " << pArray[0] << endl;

    delete [] pArray;//释放堆空间数组的时候，加上[]
}
int main(int argc, char **argv)
{
    test1();
    return 0;
}
```

### 4、引用的使用

```c++
#include <iostream>

using std::cout;
using std::endl;

//面试题
//Q：引用与指针有哪些异同点?
void test()
{
    int number = 10;
    int &ref = number;//引用是变量的别名,引用提出来的目的：就是为了减少指针的使用
    cout << "number = " << number << endl;
    cout << "ref = " << ref << endl;

    cout << endl << "修改ref后" << endl;
    int number1 = 200;
    ref = number1;//操作引用ref与操作变量本身number是一样的
    cout << "number = " << number << endl;
    cout << "number1 = " << number1 << endl;
    cout << "ref = " << ref << endl;
    cout << "&number = " << &number << endl;
    cout << "&number1 = " << &number1 << endl;
    cout << "&ref = " << &ref << endl;

    cout << endl << endl;
    //引用的底层实现就是一个指针，* const,指针常量
    /* int &ref1;//引用在定义的时候必须要进行初始化，本身是不能独立存在，必须要绑定到 */
              //到一个变量上，一经绑定就不能改变指向
}
//1、引用作为函数参数
#if 0
//实质：值传递=>进行复制
//当传递的变量类型是struct，类类型，函数开销比较大
void swap(int x, int y)//int x = a, int y = b
{
    int tmp = x;
    x = y;
    y = tmp;
}
#endif
//地址传递=>值传递
//使用指针直观性要差
void swap(int *px, int *py)//int *px = &a, int *py = &b;
{
    int tmp = *px;
    *px = *py;
    *py = tmp;
}
//引用传递:传递是变量本身
//优势：开销小，函数执行效率高，直观性好
void swap(int &x, int &y)//int &x = a, int &y = b;
{
    int tmp = x;
    x = y;
    y = tmp;
}
void test1()
{
    int a = 3, b = 6;
    cout << endl << "修改之前： " << endl;
    cout << "a = " << a << ", b = " << b << endl;
    cout << endl << "修改之后： " << endl;
    swap(a, b);
    cout << "a = " << a << ", b = " << b << endl;

}
//2、引用作为函数返回值
int func()
{
    int number = 10;
    return number;//执行return时候会有拷贝操作
}
//不要去返回局部变量的引用
int &func1()
{
    int number = 10;//局部变量
    return number;
}
//不要去返回堆空间的引用，除非有自动内存回收机制
int &getHeapData()
{
    int *pInt = new int(200);
    return *pInt;
}
//函数返回引用的前提：实体的生命周期一定要大于函数的生命周期，否则不要返回引用
int arr[10] = {1, 3, 5, 2, 9};
int &getIndex(int idx)
{
    return arr[idx];//idx越界的问题暂时不考虑
}
void test2()
{
    cout << "getIndex(0) = " << getIndex(0) << endl;
    getIndex(0) = 100;
    cout << "getIndex(0) = " << getIndex(0) << endl;
    cout << "arr[0] = " << arr[0] << endl;
}
void test3()
{
    int a = 3, b = 4;
    int c = a + getHeapData() + b;//内存泄漏
    cout << "c = " << c << endl;

    int &ref = getHeapData();
    cout << "ref = " << ref <<endl;

    delete &ref;
    ref = NULL;
}
int main(int argc, char **argv)
{
    test3();
    return 0;
}
```

### 5、C++强制类型转换

```c++
#include <stdlib.h>
#include <iostream>

using std::cout;
using std::endl;

void test()
{
    int iNumber = 10;
    float fNumber = 23.45;
    /* iNumber = (int)fNumber; */
    iNumber = int(fNumber);
    cout << "iNumber = " << iNumber << endl;
}
void test1()
{
    int iNumber = 10;
    float fNumber = 23.45;
    iNumber = static_cast<int>(fNumber);//C++强制转换
    cout << "iNumber = " << iNumber << endl;

    cout << endl << endl;
    //void *====>int *
    void *pret = malloc(sizeof(int));
    int *pInt = static_cast<int *>(pret);

    delete pInt;
}
void test2()
{
    const int number = 10;
    /* int *p1 = &number; */
    int *p2 = const_cast<int *>(&number);//去掉const
    *p2 = 100;//未定义行为
    cout << "*p2 = " << *p2 << endl;
    cout << "number = " << number << endl;
    cout << "p2 = " << p2 << endl;
    cout << "&number = " << &number << endl;

}
int main(int argc, char **argv)
{
    test2();
    return 0;
}
```

### 6、思考

1. const关键字与宏定义的区别是什么？
答：
    1、安全检查：宏定义只是字符替换，而const是在定义变量的时候
    用来修饰这个变量，所以宏不会检查代码错误，而const能够产生
    编译报错。
    2、编译器处理：宏定义是在预处理阶段展开。
    而const关键字是在程序运行时作用
    3、内存分配：宏定义的都是常量字符串，存储在程序的代码段中。
    const常量定义之后进行内存分配后，存储在程序的数据段中。
    4、作用域不同：宏定义不受作用域限制，而const受作用域限制。

2. malloc的底层实现是怎样的？free是怎么回收内存的？
答：
    1、当开辟的空间A小于128K的时候，malloc底层调用brk()函数，
    brk是将数据段的最高地址指针_edata往高地址推，_edata+30K
    只是完成虚拟地址的分配，A这块内存现在还是没有物理页与之
    对应的，等到进程第一次读写A这块内存的时候，发送缺页中断，
    这个时候，内核才会分配给A这块内存对应的物理页。也就是说，
    如果用malloc分配了A这块内容，然后从来不访问它，那么A对应
    的物理页是不会被分配的。
        而当开辟的空间大于128K的时候，利用mmap系统调用，从堆
    和栈的中间分配一块虚拟内存。这样做主要是因为：
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

3. new/delete与malloc/free的区别与联系是什么？(面试常考)
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


4. 区分以下概念：内存泄漏、内存溢出、内存踩踏、野指针？(面试常考)
答：
    1、内存泄漏：指程序中已动态分配的堆内存由于某种原因程序未释放
    或无法释放，造成系统内存的浪费，导致程序运行速度减慢甚至系统
    崩溃等严重后果
    2、内存溢出：指要求分配的内存超出了系统给出的，系统不能满足需求
    ，于是产生溢出，内存泄漏最终会导致内存溢出。
    3、内存踩踏：访问了不该访问的内存地址即为内存踩踏，比如越界访问
    数组，访问被free掉的内存，栈内存访问越界（指针），对于游戏服务器
    来说，也可以利用内存踩踏来修改程序执行结果（在反编译成功情况下）。
    4、野指针：该指针指向的位置是不可知的（随机的，不正确的，没有
    明确限制的），指针变量在定义时如果未初始化，其值是随机的，指针变
    量的值是别的变量的地址，意味着指针指向了一个地址是不确定的变量，
    此时去解引用就是去访问了一个不确定的变量，所以结果是不可知的，
    free后没有将指针置NULL的话这个指针就变成了野指针。

5. 引用与指针的区别是什么？并且将"引用"作为函数参数有哪些特点？在什么时候需要使用"常引用"？
   答：
    引用与指针的区别：
    1、引用在创建的同时必须初始化，即引用到一个有效的对象；而指针
    在定义的时候不必初始化，可以在定义后面的任何地方重新赋值
    2、不存在NULL引用，引用必须与合法的存储单元关联;而指针可以是NULL
    3、引用一旦被初始化为指向一个对象，它就不能被改变为另一个对象的
    引用(const pointer);而普通指针在任何时候都可以改变为指向另一个
    对象。给引用赋值并不是改变它和原始对象的绑定关系。
    4、引用的创建和销毁并不会调用类的拷贝构造函数。
    5、引用使用比指针更加安全，因为const pointer 仍然存在空指针，并
    且有可能产生野指针。总的来说：引用既有指针的效率，又具有变量使
    用的方便性和直观性。

    将引用作为函数参数有哪些特点：
    1、传递引用给函数与传递指针的效果是一样的。这时，被调函数的形参
    就成为原来主调函数中的实参变量或对象的一个别名来使用，所以在被调
    函数中堆形参变量的操作就是对其相应的目标对象（在主调函数中）的
    操作。
    2、使用引用传递函数的参数，在内存中并没有产生实参的副本，它是直接
    对实参操作；而使用一般变量传递函数的参数，当发生函数调用时，需要给
    形参分配存储单元，形参变量是实参变量的副本；如果传递的是对象，还将
    调用拷贝构造函数。因此，当参数传递的数据较大时，用引用比用一般
    变量传递参数的效率和所占空间都好。
    3、使用指针作为函数的参数虽然也能达到与使用引用的效果，但是，在被
    调函数中同样要给形参分配存储单元，且需要重复使用解引用进行运算，
    很容易产生错误，并且程序的阅读性较差；另一方面，在主调函数的调用
    点处，必须使用变量的地址作为实参。而引用更容易使用，更清晰。

    什么时候使用常引用：
    1、如果既要利用引用提高程序的效率，又要保护传递给函数的数据不在函数
    中被改变，就应使用常引用。

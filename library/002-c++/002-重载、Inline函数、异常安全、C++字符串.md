# C++学习笔记——2.重载、Inline函数、异常安全、C++字符串、类

### 1、函数重载

```c
#include <stdio.h>
//C语言是不支持函数重载的
//原因:不进行名字改编
int add(int x, int y)
{
    return x + y;
}
int add(int x, int y, int z)
{
    return x + y + z;
}
int main()
{
    int a = 3, b = 4, c = 5;
    printf("add(a, b) = %d\n", add(a, b));
    printf("add(a, b, c) = %d\n", add(a, b, c));
    printf("Hello world\n");
    return 0;
}
```

```c++
#include <stdio.h>//C++要兼容C，就必须按照C的方式去编译C的代码
#include <stdlib.h>
#include <string.h>
#include <iostream>
using std::cout;
using std::endl;
//C++是支持函数重载的
//支持函数重载的原因:进行名字改编(name mangling)
//具体的操作步骤：当函数名字相同的时候，根据参数的类型、顺序、个数进行改编
int add(int x, int y)
{
    return x + y;
}
int add(int x, int y, int z)
{
    return x + y + z;
}
float add(float x, float y)
{
    return x + y;
}
int add(int x, float y, int z)
{
    return x + y + z;
}
int main(int argc, char **argv)
{
    int a = 3, b = 4, c = 5;
    cout << "add(a, b) = " << add(a, b) << endl;
    cout << "add(a, b, c) = " << add(a, b, c) << endl;

    int *pInt = static_cast<int *>(malloc(sizeof(int)));
    memset(pInt, 0, sizeof(int));
    free(pInt);

    return 0;
}
```

```c++
#include <stdio.h>//C++要兼容C，就必须按照C的方式去编译C的代码
#include <stdlib.h>
#include <string.h>
#include <iostream>

using std::cout;
using std::endl;

//C++是支持函数重载的
//支持函数重载的原因:进行名字改编(name mangling)
//具体的操作步骤：当函数名字相同的时候，根据参数的类型、顺序、个数进行改编
//
//C与C++的混合编程
#ifdef __cplusplus//C++的内置宏
extern "C"
{
#endif
int add(int x, int y)
{
    return x + y;
}

#ifdef __cplusplus
}//end of extern "C"
#endif
int add(int x, int y, int z)
{
    return x + y + z;
}
float add(float x, float y)
{
    return x + y;
}
int add(int x, float y, int z)
{
    return x + y + z;
}
int main(int argc, char **argv)
{
    int a = 3, b = 4, c = 5;
    cout << "add(a, b) = " << add(a, b) << endl;
    cout << "add(a, b, c) = " << add(a, b, c) << endl;

    int *pInt = static_cast<int *>(malloc(sizeof(int)));
    memset(pInt, 0, sizeof(int));
    free(pInt);

    return 0;
}

```



### 2、默认参数

```c++
#include <iostream>
using std::cout;
using std::endl;
//注意函数重载时候的二义性
#if 0
int add(int x, int y)
{
    return x + y;
}
#endif
//效果：少些代码
//初始化顺序：从右往左
int add(int x = 0, int y = 0, int z = 0)
{
    return x + y + z;
}
int main(int argc, char **argv)
{
    int a = 3, b = 4, c = 5;
    cout << "add() = " << add() << endl;
    cout << "add(a) = " << add(a) << endl;
    cout << "add(a, b) = " << add(a, b) << endl;
    cout << "add(a, b, c) = " << add(a, b, c) << endl;

    return 0;
}
```

### 3、bool类型

bool类型非0代表true

bool类型0代表false

### 4、Inline函数

```c++
#include <iostream>
using std::cout;
using std::endl;
//没有函数的开销，效率就高一些
//带参数的宏定义有安全隐患
#define multiply(x, y) ((x)*(y))

//函数在调用的时候是有开销的
//特点：在函数调用的时候，用函数体里面的内容去进行替换
//编译器优化：现代编译器可以自动识别一些函数是不是inline函数
inline
int add(int x, int y)
{
    return x + y;
}

int main(int argc, char **argv)
{
    int a = 3, b = 4, c = 5, d = 6;
    cout << "multiply(a, b) = " << multiply(a, b) << endl;//形式很像函数
    //a + b * c + d = 3 + 4 * 5 + 6 = 29
    cout << "multiply(a + b, c + d) = " << multiply(a + b, c + d) << endl;
    cout << "add(a, b) = " << add(a, b) << endl;
    return 0;
}
```

### 5、异常安全

```c++
#include <iostream>
using std::cout;
using std::endl;
void test()
{
    double x, y;
    std::cin >> x >> y;
    try
    {
        if(0 == y)
        {
            throw y;
        }
        else
        {
            cout << "(x/y) = " << (x/y) <<endl;
        }
    }
    catch(double ex)
    {
        cout << "catch(double)"  << endl;
    }
    catch(int i)
    {
        cout << "catch(int)" << endl;
    }
}
int main(int argc, char **argv)
{
    test();
    return 0;
}
```



### 6、C++字符串

```c++
#include <stdio.h>
#include <stdlib.h>
#include <string.h>//C的头文件
#include <iostream>
#include <string>//C++的头文件
using std::cout;
using std::endl;
using std::string;

void test()
{
    //字符数组
    //C风格字符串以'\0'结尾
    char str1[] = "hello";
    char str2[] = "world";
    printf("str1: %s\n", str1);
    printf("str2: %s\n", str2);
    str1[0] = 'H';
    printf("str1: %s\n", str1);
    /* str1 = 0x1000H; */

    //获取C风格字符串长度
    int len1 = sizeof(str1);
    int len2 = sizeof(str2);
    printf("len1 = %d\n", len1);
    printf("len2 = %d\n", len2);

    //拼接C风格字符串
    int len = len1 + len2 - 1;
    char *pstr = (char *)malloc(len);
    memset(pstr, 0, len);
    strcpy(pstr, str1);
    strcat(pstr, str2);
    printf("\npstr: %s\n", pstr);

    //字符指针
    const char *pstr1 = "helloworld";
    printf("pstr1: %s\n", pstr1);
    /* cout << "111" << endl; */
    /* pstr1[0] = 'H'; */
    /* cout << "222" << endl; */
    /* printf("pstr1: %s\n", pstr1); */
    /* cout << "333" << endl; */
    pstr1 = "123456";
    printf("pstr1: %s\n", pstr1);

    free(pstr);
}

void test1()
{
    //C++       C
    string s1 = "hello";
    string s2 = "world";
    string s3 = s1 + s2;//不用去考虑空间问题(申请空间、释放)
    cout << "s1 = " << s1 << endl
         << "s2 = " << s2 << endl
         << "s3 = " << s3 << endl;

    //C++风格字符串转换为C风格字符串
    cout << endl;
    const char *pstr = s3.c_str();
    cout << "pstr = " << pstr << endl;

    //获取C++风格字符串的长度
    cout << endl;
    size_t len1 = s3.size();
    size_t len2 = s3.length();
    cout << "len1 = " << len1 << endl
         << "len2 = " << len2 << endl;

    //遍历C++风格字符串
    for(size_t idx = 0; idx != s3.size(); ++idx)
    {
        cout << s3[idx] << " ";
    }
    cout << endl;

    for(auto &elem : s3)
    {
        cout << elem << endl;
    }

    //C++风格字符串的拼接
    cout << endl;
    string s4 = s3 + "wuhan";
    cout << "s4 = " << s4 << endl;

    cout << endl;
    string s5 = s4 + 'A';
    cout << "s5 = " << s5 << endl;

    cout << endl;
    s5.append(s1);
    cout << "s5 = " << s5 << endl;

    //C++风格字符串的查找
    size_t pos = s5.find("wuhan");
    cout << "pos = " << pos << endl;

    //C++风格字符串的截取
    cout << endl;
    string s6 = s5.substr(pos, 7);
    cout << "s6 = " << s6 << endl;
}
int main(int argc, char **argv)
{
    test1();
    return 0;
}
```

### 7、内存分布

2^32 = 4G 虚拟地址空间

3G-4G:内核空间，进程管理、设备管理、虚拟文件管理。

0-3G：用户态空间
栈区：编译器自动分配与释放，函数参数、局部变量。

内存映射段：静态库、动态库，文件映射。

堆区：由程序员进行操作，malloc/free、 new/delete

读写段：全局/静态区，全局/静态变量

只读段：文字常量区，字符串常量
        		程序代码区：存放的就是程序的二进制指令。

```c++
#include <stdio.h>
#include <string.h>
#include <iostream>

using std::cout;
using std::endl;

//Q:可以看看VS等其他编译器下面的排布是不是这样？
//
//
int a;//全局变量，全局区,初始化为0
char *p1;//全局变量，全局区,初始化为NULL

int main(int argc, char **argv)
{
    int b;//栈区,随机值
    char *p2;//栈区,野指针
    static int c = 100;//静态区
    const char *pstr = "12345";//pstr本身位于栈区，字符串常量位于文字常量区

    char *p3 = new char[20]();//p3本身位于栈区，指向空间位于堆区
    strcpy(p3, "hello");

    printf("\n打印变量的地址值\n");
    printf("&a = %p\n", &a);
    printf("&p1 = %p\n", &p1);
    printf("p1 = %p\n", p1);
    printf("&b = %p\n", &b);
    printf("&p2 = %p\n", &p2);
    printf("p2 = %p\n", p2);
    printf("&c = %p\n", &c);
    printf("&pstr = %p\n", &pstr);
    printf("pstr = %p\n", pstr);
    printf("&12345 = %p\n", &"12345");
    printf("&p3 = %p\n", &p3);
    printf("p3 = %p\n", p3);
    printf("&main = %p\n", &main);

    printf("\n打印变量的值\n");
    printf("a = %d\n", a);
    printf("b = %d\n", b);

    delete [] p3;
    return 0;
}
```



### 8、类

面向过程VS面向对象？
C面向过程：模块化，按照事物的逻辑顺序进行。

C++面向对象：抽象、封装、继承、多态。

面向过程角度理解。
第一步：三兄弟交钱给老板，每人100.

第二步：老板退钱50元，交给店员。

第三步：店员把50块钱中30块钱交给三兄弟

面向对象世界：认为一切皆对象。
对象之间进行相互交互使得彼此之间的状态发生变化。

把具有相同属性的对象抽象出来形成类。
类              Person
数据成员        属性(name/id/money)
成员函数		行为/操作(pay/get)

```c++
/* #include "add.h" */
#include <string.h>
#include <iostream>

using std::cout;
using std::endl;
//
//代码规范
//
//C++对struct做了提升，和class用法很相似，可以在内部定义函数与数据
//区别：struct的默认访问权限是public，class默认访问权限是private
//
//类的声明：成员函数的声明
//类的定义:成员函数的定义
class Computer
{
//类的内部：就是大括号范围以内，称为类的内部
public://提供是一个对外的接口，服务
    void setBrand(const char *brand)
    {
        strcpy(_brand, brand);
    }

    void setPrice(float price)
    {
        _price = price;
    }

    void print()
    {
        cout << "brand: " << _brand << endl
             << "price: " << _price << endl;
    }

private://封装，不能在类的外面访问类的私有成员
    char _brand[20];//m_brand  brand_
    float _price;
};

int main(int argc, char **argv)
{
    //类的使用：创建对象，使用对象
    Computer com;
    com.setBrand("Lenovo");
    com.setPrice(6000);
    com.print();

    /* strcpy(com._brand, "Mac");//error */
    /* com._price = 20000; //error*/
    com.print();

    return 0;
}
```



```c++
#include <string.h>
#include <iostream>

using std::cout;
using std::endl;

//类的声明：成员函数的声明
//类的定义:成员函数的定义
//class里默认是private
//struct里默认是public
struct Computer
{
//类的内部：就是大括号范围以内，称为类的内部
/* public: */
    void setBrand(const char *brand)
    {
        strcpy(_brand, brand);
    }

    void setPrice(float price)
    {
        _price = price;
    }

    void print()
    {
        cout << "brand: " << _brand << endl
             << "price: " << _price << endl;
    }
/* private://封装，不能在类的外面访问类的私有成员 */
    char _brand[20];
    float _price;
};

int main(int argc, char **argv)
{
    //类的使用：创建对象，使用对象
    Computer com;
    com.setBrand("Lenovo");
    com.setPrice(6000);
    com.print();

    strcpy(com._brand, "Mac");//ok
    com._price = 20000; //ok
    com.print();

    return 0;
}


```

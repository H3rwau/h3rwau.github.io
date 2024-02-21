# C++学习笔记——5.单例模式，new和delete

### 1.单例模式

```c++
#include <iostream>

using std::cout;
using std::endl;

//单例模式设计要求:一个类只能创建一个对象
//不能创建栈对象，不能创建全局静态对象，只能创建堆对象
//
//单例模式的用途：全局唯一的资源，全局唯一的对象(变量)
//字典库、词典库、网页库、日志系统记录日志的对象

class Singleton
{
public:
    static Singleton *getInstance()
    {
        if(nullptr == _pInstance)
        {
            _pInstance = new Singleton();
        }
        return _pInstance;
    }

    static void destroy()
    {
        if(nullptr != _pInstance)
        {
             delete _pInstance;
             _pInstance = nullptr;
        }
    }
private:
    Singleton() 
    {
        cout << "Singleton()" << endl;
    }
    ~Singleton() 
    {
        cout << "~Singleton()" << endl;
    }
private:
    static Singleton *_pInstance;
};

Singleton *Singleton::_pInstance = nullptr;//静态数据成员的初始化

/* Singleton gs1;//全局对象,error */
/* Singleton gs2;//全局对象 */

int main(int argc, char **argv)
{
    /* Singleton s1;//栈对象,error */
    /* Singleton s2;//栈对象 */
    /* Singleton *ps1 = new Singleton();//堆对象,在类外无法创建 */
    Singleton::getInstance();
    Singleton *ps1 = Singleton::getInstance();
    Singleton *ps2 = Singleton::getInstance();
    cout << "ps1 = " << ps1 << endl
         << "ps2 = " << ps2 << endl;

    /* delete ps1;//error */
    /* delete ps2;//error */
    Singleton::destroy();
    Singleton::destroy();
    Singleton::destroy();
    Singleton::destroy();

    return 0;
}

```

### 2.new和delete表达式

​	1.new表达式工作步骤

​		**1.调用operator new库函数，分配未类型化的空间，用来保存指定类型的一个对象**

​		**2.运行该类型的构造函数初始化对象**

​		**3.返回指向对象的指针**

​	2.delete表达式工作步骤

​		**1.调用析构函数，回收对象中数据成员申请资源**

​		**2.调用operator delete的标准库函数释放该对象所用的内存**

```c++
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>

using std::cout;
using std::endl;

void * operator new(size_t sz)//是静态成员函数
{
    /* printf("this : %p\n", this); */
    cout << "void * operator new(size_t)" << endl;
    void *pret = malloc(sz);

    return pret;
}

void operator delete(void *pointer)//是静态成员函数
{
    /* printf("this : %p\n", this); */
    cout << "void operator delete(void *)" << endl;
    free(pointer);
}

class Student
{
public:
    Student(int id, const char *name)
    : _id(id)
    , _name(new char[strlen(name) + 1]())
    {
        cout << "Student(int, const char *)" << endl;
        strcpy(_name, name);
    }

    /* static void * operator new(size_t sz) */
    /* { */
    /*     /1* printf("this : %p\n", this); *1/ */
    /*     cout << "void * operator new(size_t)" << endl; */
    /*     void *pret = malloc(sz); */

    /*     return pret; */
    /* } */

    /* static void operator delete(void *pointer) */
    /* { */
    /*     /1* printf("this : %p\n", this); *1/ */
    /*     cout << "void operator delete(void *)" << endl; */
    /*     free(pointer); */
    /* } */

    void print() const
    {
        cout << "id: " << _id << endl
             << "name: " << _name << endl;
    }

    ~Student()
    {
        cout << "~Student()" << endl;
        if(_name)
        {
            delete [] _name;
            _name = nullptr;
        }
    }
private:
    int _id;
    char *_name;
};

int main(int argc, char **argv)
{
    Student *pstu = new Student(12, "xiaoming");
    pstu->print();

    //Q:对象的销毁与调用析构函数是不是等价的？
    //A:不等价的，堆对象(析构函数只是对象销毁过程中的一个步骤)
    delete pstu;

    return 0;
}

```

### 3.只能生成堆空间对象

```c++
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>

using std::cout;
using std::endl;

//要求:只能生成堆对象，不能生成栈对象
//做法：将析构函数设置为私有的
class Student
{
public:
    Student(int id, const char *name)
    : _id(id)
    , _name(new char[strlen(name) + 1]())
    {
        cout << "Student(int, const char *)" << endl;
        strcpy(_name, name);
    }

    static void * operator new(size_t sz)
    {
        cout << "void * operator new(size_t)" << endl;
        void *pret = malloc(sz);

        return pret;
    }

    static void operator delete(void *pointer)
    {
        cout << "void operator delete(void *)" << endl;
        free(pointer);
    }

    void print() const
    {
        cout << "id: " << _id << endl
             << "name: " << _name << endl;
    }

    void destroy()
    {
        /* this->~Student(); */
        delete this;//销毁对象本身
        //对象销毁和调用析构函数不是一回事
        //调用析构函数只是对象销毁的一个步骤
    }
private:
    ~Student()
    {
        cout << "~Student()" << endl;
        if(_name)
        {
            delete [] _name;
            _name = nullptr;
        }
    }
private:
    int _id;
    char *_name;
};

int main(int argc, char **argv)
{
    /* Student stu(13, "xiaohong");//error */

    Student *pstu = new Student(12, "xiaoming");
    pstu->print();

    /* delete pstu;//error */

    pstu->destroy();

    return 0;
}


```

### 4.只能生成栈对象

```c++
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>

using std::cout;
using std::endl;
//要求:只能生成栈对象，不能生成堆对象
//做法：将operator new/operator delete设置为私有的
//
class Student
{
public:
    Student(int id, const char *name)
    : _id(id)
    , _name(new char[strlen(name) + 1]())
    {
        cout << "Student(int, const char *)" << endl;
        strcpy(_name, name);
    }
private:
    static void * operator new(size_t sz)
    {
        cout << "void * operator new(size_t)" << endl;
        void *pret = malloc(sz);

        return pret;
    }

    static void operator delete(void *pointer)
    {
        cout << "void operator delete(void *)" << endl;
        free(pointer);
    }

public:
    void print() const
    {
        cout << "id: " << _id << endl
             << "name: " << _name << endl;
    }
/* private: */
    ~Student()
    {
        cout << "~Student()" << endl;
        if(_name)
        {
            delete [] _name;
            _name = nullptr;
        }
    }
private:
    int _id;
    char *_name;
};

int main(int argc, char **argv)
{
    //Q:生成栈对象需要哪些条件?
    //A:构造函数与析构函数都不能设置为私有的,都应该是public
    Student stu(13, "xiaohong");//stu是栈对象
    stu.print();

    /* Student *pstu = new Student(12, "xiaoming");//堆对象 */
    /* pstu->print(); */

    //Q:对象的销毁与调用析构函数是不是等价的？
    //A:不等价的，堆对象(析构函数只是对象销毁过程中的一个步骤)
    /* delete pstu; */

    return 0;
}


```

### 5.C++输入输出流

```c++
#include <iostream>
#include <string>
#include <limits>

using std::cout;
using std::cerr;
using std::endl;
using std::cin;
using std::string;

void printStreamStatus()
{
    cout << "cin's badbit = " << cin.bad() << endl
         << "cin's failbit = " << cin.fail() << endl
         << "cin's eofbit = " << cin.eof() << endl
         << "cin's goodbit = " << cin.good() << endl;
}

void test()
{
    int number = 0;
    printStreamStatus();
    cin >> number;
    printStreamStatus();
    cin.clear();//重置流的状态
    /* cin.ignore(1024, '\n');//清空缓冲区 */
    cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');//清空缓冲区
    printStreamStatus();
    cout << "number = " << number << endl;

    string s1;
    cin >> s1;
    cout << "s1 = " << s1 << endl;
}

void test2()
{
    int number = 0;
    cout << "please input a number " << endl;
    //ctrl + d
    while(cin >> number, !cin.eof())
    {
        if(cin.bad())
        {
            cerr << "stream is bad" << endl;
            return;
        }
        else if(cin.fail())
        {
            cin.clear();
            cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            cout << "please input a valid int number" << endl;
        }
        else
        {
            cout << "number = " << number << endl;
        }
    }
}
int main(int argc, char **argv)
{
    test2();
    return 0;
}
```

### 6.缓冲区

```c++
#include <unistd.h>
#include <iostream>

using std::cout;
using std::endl;
using std::flush;
using std::ends;


void test()
{
    for(size_t idx = 0; idx < 1024; ++idx)
    {
        cout << 'a';
    }
    cout << 'b';
    cout << "123" << flush;//有刷新功能
    cout << "123" << endl;//刷新功能，换行功能
    cout << "123" << ends;//没有刷新功能，会面有个空格

    sleep(5);
}

int main(int argc, char **argv)
{
    test();
    return 0;
}


```


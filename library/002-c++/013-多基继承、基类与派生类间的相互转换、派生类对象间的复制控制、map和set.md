# c++学习笔记——13.多基继承、基类与派生类间的相互转换、派生类对象间的复制控制、set和map

### 1.多基继承

1. 基类继承顺序影响构造顺序

   ```c++
   #include <iostream>
   
   using std::cout;
   using std::endl;
   
   class A
   {
   public:
       A()
       {
           cout << "A()" << endl;
       }
   
       void display() const
       {
           cout << "void A::display() const" << endl;
       }
   
       ~A()
       {
           cout << "~A()" << endl;
       }
   };
   
   class B
   {
   public:
       B()
       {
           cout << "B()" << endl;
       }
   
       void show() const
       {
           cout << "void B::show() const" << endl;
       }
   
       ~B()
       {
           cout << "~B()" << endl;
       }
   };
   
   class C
   {
   public:
       C()
       {
           cout << "C()" << endl; 
       }
   
       void print() const
       {
           cout << "void C::print() const" << endl;
       }
   
       ~C()
       {
           cout << "~C()" << endl;
       }
   };
   
   //对于多基继承而言，对于每一个基类，都要写继承方式，否则就是私有的继承方式
   //
   //在常见派生类对象的时候，基类构造函数的执行顺序与其在派生类构造函数
   //初始化表达式中的顺序没有关系，只与在定义派生类时候，基类继承的顺序有关
   class D
   : public C
   , public B
   , public A
   {
   public:
       D()
       {
           cout << "D()" << endl;
       }
   
       ~D()
       {
           cout << "~D()" << endl;
       }
   };
   
   int main(int argc, char **argv)
   {
       D d;
       d.display();
       d.show();
       d.print();
   
       return 0;
   }
   ```

   

   ### 2.成员函数访问冲突 

   ```c++
   #include <iostream>
   
   using std::cout;
   using std::endl;
   
   class A
   {
   public:
       A()
       {
           cout << "A()" << endl;
       }
   
       void show() const
       {
           cout << "void A::show() const" << endl;
       }
   
       ~A()
       {
           cout << "~A()" << endl;
       }
   };
   
   class B
   {
   public:
       B()
       {
           cout << "B()" << endl;
       }
   
       void show() const
       {
           cout << "void B::show() const" << endl;
       }
   
       ~B()
       {
           cout << "~B()" << endl;
       }
   };
   
   class C
   {
   public:
       C()
       {
           cout << "C()" << endl; 
       }
   
       void show() const
       {
           cout << "void C::show() const" << endl;
       }
   
       ~C()
       {
           cout << "~C()" << endl;
       }
   };
   
   //对于多基继承而言，对于每一个基类，都要写继承方式，否则就是私有的继承方式
   //
   //在常见派生类对象的时候，基类构造函数的执行顺序与其在派生类构造函数
   //初始化表达式中的顺序没有关系，只与在定义派生类时候，基类继承的顺序有关
   class D
   : public C
   , public B
   , public A
   {
   public:
       D()
       {
           cout << "D()" << endl;
       }
   
       ~D()
       {
           cout << "~D()" << endl;
       }
   };
   
   int main(int argc, char **argv)
   {
       D d;
       //在多基继承的时候问题1：成员函数访问冲突
       //解决办法：使用类名加作用域限定符的形式
       d.A::show();
       d.B::show();
       d.C::show();
   
       return 0;
   }
   ```

   ### 3.存储二义性

   ```c++
   #include <iostream>
   
   using std::cout;
   using std::endl;
   
   class A
   {
   public:
       A()
       : _ix(0)
       {
           cout << "A()" << endl;
       }
   
       void setX(double ix) 
       {
           _ix = ix;
       }
   
       void show() const
       {
           cout << "A::_ix = " << _ix << endl;
       }
   
       ~A()
       {
           cout << "~A()" << endl;
       }
   private:
       double _ix;
   };
   
   class B
   : virtual public A
   {
   #if 0
   public:
       B()
       {
           cout << "B()" << endl;
       }
   
       void show() const
       {
           cout << "void B::show() const" << endl;
       }
   
       ~B()
       {
           cout << "~B()" << endl;
       }
   #endif
   };
   
   class C
   : virtual public A
   {
   #if 0
   public:
       C()
       {
           cout << "C()" << endl; 
       }
   
       void show() const
       {
           cout << "void C::show() const" << endl;
       }
   
       ~C()
       {
           cout << "~C()" << endl;
       }
   #endif
   };
   
   //对于多基继承而言，对于每一个基类，都要写继承方式，否则就是私有的继承方式
   //
   //在常见派生类对象的时候，基类构造函数的执行顺序与其在派生类构造函数
   //初始化表达式中的顺序没有关系，只与在定义派生类时候，基类继承的顺序有关
   class D
   : public C
   , public B
   {
   public:
       D()
       {
           cout << "D()" << endl;
       }
   
       ~D()
       {
           cout << "~D()" << endl;
       }
   };
   
   int main(int argc, char **argv)
   {
       cout << "sizeof(A) = " << sizeof(A) << endl;
       cout << "sizeof(B) = " << sizeof(B) << endl;
       cout << "sizeof(C) = " << sizeof(C) << endl;
       cout << "sizeof(D) = " << sizeof(D) << endl;
   
       cout << endl;
       D d;
       //在多基继承的时候问题2：存储二义性
       //解决办法:在B/C继承方式前面加上virtual
       d.setX(1000);
       d.show();
   
       d.A::setX(1);
       d.A::show();
   
       d.B::setX(100);
       d.B::show();
   
       d.C::setX(101);
       d.C::show();
   
       d.show();
       return 0;
   }
   ```

   

### 2.基类与派生类的相互转换

```c++
#include <iostream>

using std::cout;
using std::endl;

class Base
{
public:
    Base()
    : _base(0)
    {
        cout << "Base()" << endl;
    }

    Base(double base)
    : _base(base)
    {
        cout << "Base(double)" << endl;
    }

    void display() const
    {
        cout << "Base::_base = " <<_base << endl;
    }
    ~Base()
    {
        cout << "~Base()" << endl;
    }


private:
    double _base;
};

class Derived
: public Base
{
public:
    Derived()
    : Base(0)
    , _derived(0)
    {
        cout << "Derived()" << endl;
    }

    Derived(double base, double derived)
    : Base(base)
    , _derived(derived)
    {
        cout << "Derived(double)" << endl;
    }

    void print() const
    {
        cout << "Derived::_derived = " << _derived << endl;
    }

    ~Derived()
    {
        cout << "~Derived()" << endl;
    }
private:
    double _derived;
};

int main(int argc, char **argv)
{
    cout << "sizeof(Base) = " << sizeof(Base) << endl;
    cout << "sizeof(Derived) = " << sizeof(Derived) << endl;

    cout << endl;
    Base base(11.11);
    base.display();

    cout << endl;
    Derived derived(22.22, 33.33);
    derived.print();


    cout << endl << endl;
    base = derived;//1、可以吧一个派生类对象赋值给基类对象
    base.operator=(derived);//Base &operator=(const Base &rhs)==>const Base &rhs = derived;
    base.display();


    cout << endl << endl;
    Base &ref = derived;//2、基类的引用可以绑定到派生类对象上
    ref.display();

    cout << endl << endl;
    Base *pbase = &derived;//3、基类的指针可以指向派生类对象(向上转型)
    pbase->display();

    cout << endl << "将基类转换为派生类: " << endl;
    Base base1(100);
    Derived derived1(200, 300); 
#if 0
    derived1 = base1;//error,1、基类的对象不能赋值给派生类对象
    derived1.operator=(base1);//Derived &operator=(const Derived &rhs)==>const Derived &rhs = base1;

    Derived &ref1 = base1;//error,2、派生类的引用不能绑定到基类的对象
    Derived *pderived = &base1;//3、派生类的指针不能指向基类的对象(向下转型)
#endif
    Derived *pderived1 = static_cast<Derived *>(&base1);//不安全的向下转型

    Base *pbase2 = &derived1;
    Derived *pderived2 = static_cast<Derived *>(pbase2);//安全的向下转型
    return 0;
}


```



### 3.派生类对象间的复制控制

1. 如果用户定义了基类的拷贝构造函数，而没有定义派生类的拷贝构造函数，那
   么在用一个派生类对象初始化新的派生类对象时，**两对象间的派生类部分执行**
   **缺省的行为，而两对象间的基类部分执行用户定义的基类拷贝构造函数。**

2.  如果用户重载了基类的赋值运算符函数，而没有重载派生类的赋值运算符函
   数，那么在用一个派生类对象给另一个已经存在的派生类对象赋值时，**两对象**
   **间的派生类部分执行缺省的赋值行为，而两对象间的基类部分执行用户定义的**
   **重载赋值函数。**

   ```c++
   #include <string.h>
   #include <iostream>
   
   
   using std::cout;
   using std::endl;
   
   class Base
   {
   public:
       Base()
       : _pbase(nullptr)
       {
           cout << "Base()" << endl;
       }
   
       Base(const char *pbase)
       : _pbase(new char[strlen(pbase) + 1]())
       {
           cout << "Base(const char *)" << endl;
           strcpy(_pbase, pbase);
       }
   
       Base(const Base &rhs)
       : _pbase(new char[strlen(rhs._pbase) + 1]())
       {
           cout << "Base(const Base &)" << endl;
           strcpy(_pbase, rhs._pbase);
       }
   
       Base &operator=(const Base &rhs)
       {
           cout << "Base &operator=(const Base &)" << endl;
           if(this != &rhs)
           {
               delete [] _pbase;
               _pbase = nullptr;
               _pbase = new char[strlen(rhs._pbase) + 1]();
               strcpy(_pbase, rhs._pbase);
           }
   
           return *this;
       }
   
       ~Base()
       {
           cout << "~Base()" << endl;
           if(_pbase)
           {
               delete [] _pbase;
               _pbase = nullptr;
           }
       }
   
       friend std::ostream &operator<<(std::ostream &os, const Base &rhs);
   private:
       char *_pbase;
   };
   std::ostream &operator<<(std::ostream &os, const Base &rhs)
   {
       if(rhs._pbase)
       {
           os << rhs._pbase;
       }
   
       return os;
   }
   
   class Derived
   : public Base
   {
   public:
       Derived(const char *pbase)
       : Base(pbase)
       {
           cout << "Derived(const char *)" << endl;
       }
   
       ~Derived()
       {
           cout << "~Derived()" << endl;
       }
       friend std::ostream &operator<<(std::ostream &os, const Derived &rhs);
   
   };
   std::ostream &operator<<(std::ostream &os, const Derived &rhs)
   {
       const Base &base = rhs;
       os << base;
       return os;
   }
   
   int main(int argc, char **argv)
   {
       Derived d1("hello");
       cout << "d1 = " << d1 << endl;
   
   
       cout << endl;
       Derived d2(d1);
       cout << "d1 = " << d1 << endl;
       cout << "d2 = " << d2 << endl;
   
       cout << endl;
       Derived d3("world");
       cout << "d3 = " << d3 << endl;
       d3 = d1;
       cout << "d1 = " << d1 << endl;
       cout << "d3 = " << d3 << endl;
       return 0;
   }
   
   
   ```

   

3. 如果用户定义了派生类的拷贝构造函数或者重载了派生类的对象赋值运算符=，
   则在用已有派生类对象初始化新的派生类对象时，或者在派生类对象间赋值
   时，将会执行用户定义的派生类的拷贝构造函数或者重载赋值函数，而不会再
   自动调用基类的拷贝构造函数和基类的重载对象赋值运算符，**这时，通常需要
   用户在派生类的拷贝构造函数或者派生类的赋值函数中显式调用基类的拷贝构
   造或赋值运算符函数 ** 

   ```c++
   #include <string.h>
   #include <iostream>
   
   
   using std::cout;
   using std::endl;
   
   class Base
   {
   public:
       Base()
       : _pbase(nullptr)
       {
           cout << "Base()" << endl;
       }
   
       Base(const char *pbase)
       : _pbase(new char[strlen(pbase) + 1]())
       {
           cout << "Base(const char *)" << endl;
           strcpy(_pbase, pbase);
       }
   
       Base(const Base &rhs)
       : _pbase(new char[strlen(rhs._pbase) + 1]())
       {
           cout << "Base(const Base &)" << endl;
           strcpy(_pbase, rhs._pbase);
       }
   
       Base &operator=(const Base &rhs)
       {
           cout << "Base &operator=(const Base &)" << endl;
           if(this != &rhs)
           {
               delete [] _pbase;
               _pbase = nullptr;
               _pbase = new char[strlen(rhs._pbase) + 1]();
               strcpy(_pbase, rhs._pbase);
           }
   
           return *this;
       }
   
       ~Base()
       {
           cout << "~Base()" << endl;
           if(_pbase)
           {
               delete [] _pbase;
               _pbase = nullptr;
           }
       }
   
       friend std::ostream &operator<<(std::ostream &os, const Base &rhs);
   private:
       char *_pbase;
   };
   std::ostream &operator<<(std::ostream &os, const Base &rhs)
   {
       if(rhs._pbase)
       {
           os << rhs._pbase;
       }
   
       return os;
   }
   
   class Derived
   : public Base
   {
   public:
       Derived(const char *pbase, const char *pderived)
       : Base(pbase)
       , _pderived(new char[strlen(pderived) + 1]())
       {
           cout << "Derived(const char *)" << endl;
           strcpy(_pderived, pderived);
       }
   
       Derived(const Derived &rhs)
       : Base(rhs)//显示调用基类的拷贝构造函数
       , _pderived(new char[strlen(rhs._pderived) + 1]())
       {
           cout << "Derived(const Derived &)" << endl;
           strcpy(_pderived, rhs._pderived);
       }
   
       Derived &operator=(const Derived &rhs)
       {
           cout << "Derived &operator=(const Derived &)" << endl;
           if(this != &rhs)
           {
               Base::operator=(rhs);//显示调用基类的赋值运算符函数，完成基类部分的赋值
               delete [] _pderived;
               _pderived = nullptr;
               _pderived = new char[strlen(rhs._pderived) + 1]();
               strcpy(_pderived, rhs._pderived);
           }
   
           return *this;
       }
   
       ~Derived()
       {
           cout << "~Derived()" << endl;
           if(_pderived)
           {
               delete [] _pderived;
               _pderived = nullptr;
           }
       }
       friend std::ostream &operator<<(std::ostream &os, const Derived &rhs);
   private:
       char *_pderived;
   
   };
   std::ostream &operator<<(std::ostream &os, const Derived &rhs)
   {
       const Base &base = rhs;
       os << base << ", " << rhs._pderived;
       return os;
   }
   
   int main(int argc, char **argv)
   {
       Derived d1("hello", "world");
       cout << "d1 = " << d1 << endl;
   
   
       cout << endl;
       Derived d2(d1);
       cout << "d1 = " << d1 << endl;
       cout << "d2 = " << d2 << endl;
   
       cout << endl;
       Derived d3("hubei", "wuhan");
       cout << "d3 = " << d3 << endl;
       d3 = d1;
       cout << "d1 = " << d1 << endl;
       cout << "d3 = " << d3 << endl;
       return 0;
   }
   
   
   ```

### 4.set和map

```c++
#include <iostream>
#include <set>
#include <map>
#include <string>

using std::cout;
using std::endl;
using std::set;
using std::map;
using std::string;

void test1()
{
    //set特征：
    //1、key值唯一，不能存放关键字相同的元素
    //2、默认情况下，set按照key从小到大排列
    //3、set底层实现是一个红黑树
    int arr[5] = {1, 3, 90, 45, 100};
    set<int> numbers{1, 5, 90, 45, 2};
    numbers.insert(1);
    numbers.insert(2);
    numbers.insert(arr, arr + 5);

    //set遍历
    for(auto &elem : numbers)
    {
        cout << elem << " ";
    }
    cout << endl;

    //set遍历2
    //迭代器可以理解为一个指针
    set<int>::iterator it;
    for(it = numbers.begin(); it != numbers.end(); ++it)
    {
        cout << *it << " ";
    }
    cout << endl;

    //set的查找
    size_t cnt1 = numbers.count(1);
    size_t cnt2 = numbers.count(1000);
    cout << "cnt1 = " << cnt1 <<endl
        << "cnt2 = " << cnt2 << endl;

    auto it1 = numbers.find(1);
    if(it1 == numbers.end())
    {
        cout << "该元素不在set中" << endl;
    }
    else
    {
        cout << "*it1 = " << *it1 << endl;
    }

    //set不支持下标访问运算符
    /* cout << numbers[0] << endl; */
    
    //set不支持元素修改
    /* *it1 = 100; */
}

void test2()
{
    //map存放键值对
    //1、key具有唯一性
    //2、按照key从小到大排列
    //3、map的底层实现也是红黑树
    map<string, string> numbers
    {
        {"027", "武汉"},
        {"010","北京"},
        {"011","天津"},
        {"021", "上海"},
        {"021", "南京"},
        std::pair<string, string>("023","广州")
    };

    for(auto &elem : numbers)
    {
        cout << elem.first << "--->"
             << elem.second << endl;
    }
    cout << endl;

    auto it = numbers.insert({"0271", "新疆"});
    if(it.second)
    {
        cout << "插入成功" << endl;
        cout << it.first->first << "--->"
             << it.first->second << endl;
    }
    else
    {
        cout << "该元素在列表中存在" << endl;
    }

    for(auto &elem : numbers)
    {
        cout << elem.first << "--->"
             << elem.second << endl;
    }
    cout << endl;

    //当map里面对应的key不存在则直接插入map中
    //当key存在，返回key对应value
    cout << endl << "map的下标访问" << endl;
    cout << numbers["027"] << endl;

    numbers["020"] = "杭州";//插入
    numbers.operator[]("020").operator=("杭州");
    for(auto &elem : numbers)
    {
        cout << elem.first << "--->"
             << elem.second << endl;
    }
    cout << endl;
    numbers["020"] = "深圳";//修改
    for(auto &elem : numbers)
    {
        cout << elem.first << "--->"
             << elem.second << endl;
    }
    cout << endl;
}
int main(int argc, char **argv)
{
    test2();
    return 0;
}


```






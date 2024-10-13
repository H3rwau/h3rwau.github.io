`std::forward`是C++11中引入的一个[函数模板](https://so.csdn.net/so/search?q=函数模板&spm=1001.2101.3001.7020)，用于实现==**完美转发**==。它的作用是**根据传入的参数**，==**决定将参数以左值引用还是右值引用的方式进行转发。**==

传统上，当一个左值传递给一个函数时，参数会以左值引用的方式进行传递；当一个右值传递给一个函数时，参数会以右值引用的方式进行传递。**完美转发是为了解决传递参数时的临时对象（右值）被强制转换为左值的问题**。std::forward实现完美转发主要用于以下场景：**提高模板函数参数传递过程的转发效率。**


对于形如`T&&`的变量或者参数，如果`T`可以进行推导，那么`T&&`称之为万能引用。换句话说，对于形如`T&&`的类型来说，其既可以绑定左值，又可以绑定右值，而这个的**前提是`T`需要进行推导**。最常见的万能引用方式如以下两种：

```c++
template<typename T>
void f(T&& param); // 存在类型推导，param是一个万能引用
```

```c++
auto&& var = var1; // 存在类型推导，var是一个万能引用
```

**注意**：只有当**发生自动类型推断**时（例如：函数模板的类型自动推导），`T &&`才是万能引用。下面一个示例中的`&&` 并不是一个万能引用，例如：

```c++
template<typename T>
void f( T&& param); // 这里T的类型需要推导，所以&&是一个 universal references

template<typename T>
class Test {
	Test(Test&& rhs);  // Test是一个特定的类型，不需要类型推导，所以&&表示右值引用  
};
```

万能引用进行类型推导时需要推导出`T&&`中的`T`的真实类型：若传入的参数是一个左值，则`T`会被推导为左值引用；而如果传入的参数是一个右值，则`T`会被推导为原生类型（非引用类型）。

对于万能引用来说，条件之一就是**类型推导**，但是类型推导是万能引用的**必要非充分条件**，也就是说参数必须被声明为`T&&`形式不一定是万能引用。示例如下：

```c++
template<typename T>
void func(std::vector<T>&& t); // t是右值引用
```

调用`func`时会执行类型推导，但是参数`t`的类型声明的形式并非`T &&`而是`std::vector &&`。 之前强调过，万能引用必须是`T &&`才行，因此，`t`是一个右值引用，如果尝试将左值传入，编译器将会报错：

```c++
std::vector<int> v;
fun(v); // 编译错误，不能将左值绑定到右值
```

形如`const T&&`的方式也不是万能引用：

```c++
template<typename T>
void f(const T&& t); // t是右值引用

int main() {
  int a = 0;
  f(a); // 错误
}
```

## 引用折叠

引用折叠是一种特性，允许在模板元编程中使用引用类型的参数来创建新的引用类型。由于存在`T&&`这种**万能引用类型**，当它作为参数时，有可能被一个左值/左值引用或右值/右值引用的参数初始化，这需要通过类型推导，推导后得到的参数类型会发生类型变化，这种变化就称为引用折叠。

根本原因是因为C++中禁止reference to reference，所以编译器需要对四种情况（& &、& &&，&& &,&& &&）进行处理，将他们折叠成一种单一的reference。引用折叠的规则如下：**如果两个引用中至少其中一个引用是左值引用，那么折叠结果就是左值引用**；否则折叠结果就是右值引用。示例如下：


```c++
using T = int &;
T& r1;  // int& & r1 -> int& r1
T&& r2; // int& && r2 -> int& r2
  
using U = int &&;
U& r3;  // int&& & r3 -> int& r3
U&& r4; // int&& && r4 -> int&& r4
```

```c++
template<typename T>
void func(T &&t) {
    cout << "hello world" << endl;
}

int main() {
    int a = 1;
    int &b = a;
    func(a); // T 推导成 int &; T && ==> int & && ==> int &
    func(b); // T 推导成 int &; T && ==> int & && ==> int &
    func(1); // T 推导成 int; T && ==> int &&
    func(std::move(a)); // T 推导成 int &&; T && ==> int && && ==> int &&
    return 0;
}
```

完美转发是为了解决传递参数时的临时对象（右值）被强制转换为左值的问题，`std::forward`源码如下：

```c++
template<class T>
T&& forward(typename std::remove_reference<T>::type& t) noexcept {
  return static_cast<T&&>(t);
}

template <class T>
T&& forward(typename std::remove_reference<T>::type&& t) noexcept {
  return static_cast<T&&>(t);
}
```

其内部实现只有一行代码，即static_cast<T&&>(t)使用static_cast<>进行类型转换，与std::move()实现方式类似。结合前面介绍的引用折叠，**当接收一个左值作为参数时，std::forward<>()返回左值引用，相应的，当接收一个右值作为参数时，std::forward<>()返回右值引用。**


下面给出一个案例没有实现完美转发，如下：

```c++
#include <iostream>

template <typename T>
void wrapper(T u) {
    fun(u);
}

class MyClass {};

void fun(MyClass& a) { std::cout << "in fun(MyClass&)\n"; }
void fun(const MyClass& a) { std::cout << "in fun(const MyClass&)\n"; }
void fun(MyClass&& a) { std::cout << "in fun(MyClass &&)\n"; }

int main(void) {
    MyClass a;
    const MyClass b;

    fun(a);
    fun(b);
    fun(MyClass());

    std::cout << "----- Wrapper ------\n";
    wrapper(a);
    wrapper(b);
    wrapper(MyClass());

    return 0;
}

```

输出结果：

```c
in func(MyClass&)
in func(const MyClass&)
in func(MyClass &&)
----- Wrapper ------
in func(MyClass&)
in func(const MyClass&)
in func(const MyClass&)

Process returned 0 (0x0)   execution time : 0.253 s
Press any key to continue.
```

**最后一行函数调用结果不符合预期**，传入的是MyClass &&右值引用，预期调用fun(MyClass&& a)，实际上调用的却是fun(const MyClass& a)。调用wrapper函数时触发拷贝构造，基于右值创建了左值u（即：wrapper函数的参数），u的实际类型是const MyClass，匹配的是fun(const MyClass& a)


**使用std::forward实现完美转发**

```c++
#include <iostream>

template <typename T>
void wrapper(T &&u) { // 万能引用
    func(std::forward<T>(u)); // 完美转发
}

class MyClass {};

void func(MyClass& a) { std::cout << "in func(MyClass&)\n"; }
void func(const MyClass& a) { std::cout << "in func(const MyClass&)\n"; }
void func(MyClass&& a) { std::cout << "in func(MyClass &&)\n"; }

int main(void) {
    MyClass a;
    const MyClass b;

    func(a);
    func(b);
    func(MyClass());

    std::cout << "----- Wrapper ------\n";
    wrapper(a);
    wrapper(b);
    wrapper(MyClass());

    return 0;
}
```

```c++
in func(MyClass&)
in func(const MyClass&)
in func(MyClass &&)
----- Wrapper ------
in func(MyClass&)
in func(const MyClass&)
in func(MyClass &&)

Process returned 0 (0x0)  execution time : 0.210 s
Press any key to continue.

```

`std::forward()`建议**仅用于模板函数**，对于**非模板的，因为不涉及到类型推导，所以使用完美转发是没有意义的**。

**疑惑**
可能有人会说，这不对啊，使用 std::forward 修改之前函数参数就是 int&& 类型，修改之后得到的返回值还是 int&& 类型，这有什么区别吗？

这里的区别就在于，**使用 std::forward 之前的 int&& 是有名字的变量 t**，**它是一个左值**，而**使用 std::forward 返回之后的 int&& 是有个匿名变量，它是一个右值，真正的差距就在这里。**

具名变量都是左值

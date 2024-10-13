### const为运行时常量，constexpr为编译时常量

编译器会将constexpr函数视为内联函数！所以在编译时若能求出其值，则会把函数调用替换成结果值。

类的构造函数也可以使用constexpr关键字

constexpr还能修饰类的构造函数，即保证传递给该构造函数的所有参数都是constexpr，那么产生的对象的所有成员都是constexpr。该对象是constexpr对象了，可用于只使用constexpr的场合。 
        注意constexpr构造函数的函数体必须为空，所有成员变量的初始化都放到初始化列表中。

```c++

#include <iostream>
using namespace std;
 
class Test 
{
public:
	constexpr Test(int num1, int num2) : m_num1(num1), m_num2(num2)
	{
		
	}
 
public:
	int m_num1;
	int m_num2;
};
 
int main(void) 
{
	constexpr Test t1(1, 2);
 
	enum e
	{ 
		x = t1.m_num1, 
		y = t1.m_num2 
	};
 
	return 0;
}

```

## const和constexpr对指针的修饰有什么差别呢？

（1）const 和 constexpr 变量之间的主要区别在于：**==const 变量的初始化可以延迟到运行时==**，**而 ==constexpr 变量必须在编译时进行初始化==。所有 constexpr 变量均为常量，因此必须使用常量表达式初始化**。

（2）constexpr和指针
       在使用const时，如果关键字const出现在星号左边，表示被指物是常量；如果出现在星号右边，表示指针本身是常量；如果出现在星号两边，表示被指物和指针两者都是常量。

​	与const不同，**在constexpr声明中如果定义了一个指针，限定符constexpr仅对指针有效**，与指针所指对象无关。

   constexpr是一种很强的约束，更好的保证程序的正确定语义不被破坏；编译器可以对constexper代码进行非常大的优化，**例如：将用到的constexpr表达式直接替换成结果, 相比宏来说没有额外的开销。**

```c++
#include <iostream>
using namespace std;
 
int g_tempA = 4;
const int g_conTempA = 4;
constexpr int g_conexprTempA = 4;
 
int main(void)
{
	int tempA = 4;
	const int conTempA = 4;
	constexpr int conexprTempA = 4;
	/*1.正常运行，编译通过*/
	const int &conptrA = tempA;
	const int &conptrB = conTempA;
	const int &conptrC = conexprTempA;
 
	/*2.有两个问题：一是引用到局部变量，不能再编译器确定；二是conexprPtrB和conexprPtrC应该为constexpr const类型，编译不过*/
	constexpr int &conexprPtrA = tempA;
	constexpr int &conexprPtrB = conTempA;
	constexpr int &conexprPtrC = conexprTempA;
 
	/*3.第一个编译通过，后两个不通过，原因是因为conexprPtrE和conexprPtrF应该为constexpr const类型*/
	constexpr int &conexprPtrD = g_tempA;
	constexpr int &conexprPtrE = g_conTempA;
	constexpr int &conexprPtrF = g_conexprTempA;
 
	/*4.正常运行，编译通过*/
	constexpr const int &conexprConPtrD = g_tempA;
	constexpr const int &conexprConPtrE = g_conTempA;
	constexpr const int &conexprConPtrF = g_conexprTempA;
 
	return 0;
}
```

简单的说**constexpr所引用的对象必须在编译期就决定地址**。还有一个奇葩的地方就是可以通过上例conexprPtrD来修改g_tempA的值，也就是说**constexpr修饰的引用不是常量**，如果要确保其实**常量引用需要constexpr const**来修饰。

C++ 11标准中，为了**解决 const 关键字的双重语义问题**，保留了 const 表示“只读”的语义，而将“常量”的语义划分给了新添加的 constexpr 关键字。因此 C++11 标准中，建议将 const 和 constexpr 的功能区分开，**即凡是表达“只读”语义的场景都使用 const，表达“常量”语义的场景都使用 constexpr。**

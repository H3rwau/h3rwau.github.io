# c++学习笔记——23.bind,remove,自定义vector

### 1.bind

```c++
#include <iostream>
#include <functional>


using std::cout;
using std::cin;
using std::endl;
using std::bind;
using std::function;
using namespace std::placeholders;

int add(int x,int y)
{
    cout<<"int add(int x,int y)"<<endl;
    return x+y;
}

class Test
{
    public:
    int add(int x,int y)
    {
        cout<<"int Test::add(int,int)"<<endl;
        return x+y;
    }
    int _data=9527;//c++11新特性，bind能够绑定到数据成员
};

void test()
{
    // auto f=bind(add,7,2);
    // cout<<"f()="<<f()<<endl;

    //std::function +std::bind可以取代继承+多态
    //function其实就是函数的容器
    function<int()> f=bind(add,2,3);
    cout<<"f()="<<f()<<endl;

    Test t;
    function<int()> f2=bind(&Test::add,&t,33,77);//绑定到成员函数
    cout<<"f2()="<<f2()<<endl;

    f2=bind(&Test::_data,&t);//绑定到数据成员
    cout<<"f2()="<<f2()<<endl;

    //占位符
    // using namespace std::placeholders;
    std::function<int(int)> f3=bind(add,9,_1);
    cout<<"f3(7)="<<f3(7)<<endl;
}

typedef int(*pF)(int);//函数指针
int func1(int x)
{
    return  x;
}
int func2(int x)
{
    return  2*x;
}
void test1()
{
    //对于f注册回调函数，C语言是可以实现多态的，通过函数指针实现多态
    pF f=func1;
    cout<<"f(1)="<<f(1)<<endl;

    f=func2;
    cout<<"f(1)="<<f(1)<<endl;

}
void func3(int x1,int x2,int x3,const int &x4,int x5)
{
    cout<<"-"<<x1
        <<"-"<<x2
        <<"-"<<x3
        <<"-"<<x4
        <<"-"<<x5
        <<endl;
}
void test3()
{
    //bind绑定参数的时候采用的是值传递
    //占位符本身所在的位置是形参的位置
    //占位符的数字代表实参传递时候的位置
    //cref = const reference 叫做引用包装器

    int num=99;
    auto f=bind(func3,2,3,4,num,num);
    num=77;
    f();

    auto f1=bind(func3,2,3,4,std::cref(num),num);
    num=66;
    f1();

    auto f2=bind(func3,3,_1,_2,std::cref(num),_3);
    f2(11,9,7,8,88);//对于没有作用的实参是无效的参数
}
int main(int argc,char **argv)
{
    // test();
    // test1();
    test3();
    return 0;
}

```

### 2.remove

```c++
#include <iostream>
#include <algorithm>
#include <vector>
#include <iterator>
using std::cout;
using std::cin;
using std::endl;
using std::remove_if;
using std::vector;
using std::ostream_iterator;
using std::copy;

bool judge(int &n)
{
    return n>5;
}

void test()
{
    //remove删除不彻底
    vector<int> num{1,3,4,4,9,2,3,5,1,7,8};
    copy(num.begin(),num.end(),ostream_iterator<int>(cout,"-"));
    cout<<endl;
    auto it=remove_if(num.begin(),num.end(),judge);
    //remove_if与erase结合使用才能达到预期效果
    num.erase(it,num.end());
    copy(num.begin(),num.end(),ostream_iterator<int>(cout,"-"));
}
void test2()
{
    vector<int> num;
    num.push_back(3);
    bool flg=true;//容器在进行遍历的时候，不要去进行写操作，可能迭代器以及失效了
    for (auto it = num.begin(); it != num.end(); it++)
    {
        cout<<*it<<" ";
        if(flg)
        {
            num.push_back(4);//此时vector的底层已经发生了扩容操作，it迭代器还是指在原来的空间，而vector的空间已经转移了
            flg=false;
        }   
    }
}
void test3()
{
    //remove删除不彻底
    vector<int> num{1,3,4,4,9,2,3,5,1,7,8};
    copy(num.begin(),num.end(),ostream_iterator<int>(cout,"-"));
    cout<<endl;
    // std::less<int> lt;
    // auto it=remove_if(num.begin(),num.end(),std::bind1st(lt,5));//将大于5的删除
    std::greater<int> gt;
    auto it=remove_if(num.begin(),num.end(),std::bind2nd(gt,5));//将大于5的删除
    //remove_if与erase结合使用才能达到预期效果
    num.erase(it,num.end());
    copy(num.begin(),num.end(),ostream_iterator<int>(cout,"-"));
}
void test4()//vector删除
{
    vector<int> num{1,2,3,4,5,6,7};
    for(auto &a:num)
    {
        cout<<a<<"-";
    }
    cout<<endl;
    #if 0
    //error---------------
    auto it=num.begin()+2;
    for(;it!=num.end();)
    {
        num.erase(it++);
    }
    //--------------------
    #endif
    #if 0
    //correct---------------
    auto it=num.begin()+2;
    for(;it!=num.end();)
    {
        num.erase(it);
    }
    //--------------------
    #endif
    #if 1
    //correct---------------
    auto it=num.begin()+2;
    for(;it!=num.end();)
    {
        it=num.erase(it);
    }
    //--------------------
    #endif
    for(auto &a:num)
    {
        cout<<a<<"-";
    }
    cout<<endl;
}
int main(int argc,char **argv)
{
    // test3();
    test4();
    
    return 0;
}

```

### 3.自定义vector

```c++
#include <iostream>
#include <memory>

using std::cout;
using std::cin;
using std::endl;
using std::uninitialized_copy;

template<typename T>
class Vector
{
public:
    //typedef T* iterator;
    Vector();
    ~Vector();
    
    void push_back(const T & v); 
    void pop_back();    
    
    int size();
    int capacity();
    T& operator[](size_t i);

    T* /*iterator*/ begin()
    {
        return _start;
    } 
    T* /*iterator*/ end()
    {
        return _finish;
    }
private:
    void reallocate();//重新分配内存,动态扩容要用的
private:    
    static std::allocator<T> _alloc;
    
    T * _start;      //指向数组中的第一个元素
    T * _finish; //指向最后一个实际元素之后的那个元素
    T * _end_of_storage;        //指向数组本身之后的位置
};

template<typename T>
Vector<T>::Vector()
:_start(nullptr)
,_finish(nullptr)
,_end_of_storage(nullptr)
{

}
template<typename T>
Vector<T>::~Vector()
{
    if(_start)//Vector不为空
    {
        while(_start!=_finish)
        {
            --_finish;
            _alloc.destroy(_finish);//删除元素
        }
        _alloc.deallocate(_start,capacity());//释放空间
    }
}

template<typename T>
void Vector<T>::push_back(const T &v)
{
    if(size()==capacity())
    {
        reallocate();
    }
    _alloc.construct(_finish++,v);
}
template<typename T>
void Vector<T>::pop_back()   
{
    if(size()>0)
    {
        _alloc.destroy(--_finish);
    }
}

template<typename T>
int Vector<T>::size()
{
    return _finish-_start;
}
template<typename T>
int Vector<T>::capacity()
{
    return _end_of_storage-_start;
}
template<typename T>
void Vector<T>::reallocate()//重新分配内存,动态扩容要用的
{
    int nowC=capacity();
    int newC;
    if(0==nowC)
    {
        newC=1;
    }else
    {
        newC=2*nowC;
    }
    T* newStart=_alloc.allocate(newC);
    if(_start)
    {
        uninitialized_copy(_start,_finish,newStart);
        // uninitialized_copy 会在目标地址构造对象. 
        // 当要把对象复制到一段未初始化的内存地址的时候用.
        while(_start!=_finish)
        {
            --_finish;
            _alloc.destroy(_finish);//删除元素
        }
        _alloc.deallocate(_start,nowC);//释放空间
    }
    _start=newStart;
    _finish=_start+nowC;
    _end_of_storage=_start+newC;
}
template<typename T>
T& Vector<T>::operator[](size_t i)
{
    return _start[i];
}

template<typename T>
std::allocator<T> Vector<T>::_alloc;

void test_my_vector()
{
    Vector<int> myVector;
    cout<<"the size now:"<<myVector.size()<<endl;
    cout<<"the capacity now:"<<myVector.capacity()<<endl;

    for (size_t i = 0; i < 10; i++)
    {
        myVector.push_back(i);
        cout << "the size now:" << myVector.size() << endl;
        cout << "the capacity now:" << myVector.capacity() << endl;
    }
    for (size_t i = 0; i < 5; i++)
    {
        myVector.pop_back();
        cout << "the size now:" << myVector.size() << endl;
        cout << "the capacity now:" << myVector.capacity() << endl;
    }

    for(size_t i=0;i<myVector.size();i++)
    {
        cout<<myVector[i]<<"-";
    }
    cout<<endl;
    
    for(auto &e:myVector)
    {
        cout<<e<<endl;
    } 
}
int main(int argc,char **argv)
{
    test_my_vector(); 
    return 0;
}

```
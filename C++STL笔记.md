# STL笔记

## Day20

### 一、标准模板库STL

六大组件

1、容器 用来存数据的，也就是数据结构

- 序列式容器  vector
- 关联式容器  set、map
- 无序关联式容器  unordered_set、unordered_map

2、迭代器  看成是指针，泛型指针，具备指针的功能。访问容器中的元素的。

3、算法  操作容器中的元素。迭代器可以看成是容器与算法之间的桥梁。

4、适配器   做适配操作

- 容器适配器 stack queue
- 迭代器适配器 
- 函数适配器 

5、函数对象（仿函数）  定制化操作。

6、空间配置器  进行空间的申请与释放的。（用法 + 原理 + 源代码 ）

程序 = 数据结构（容器） + 算法。



### 二、序列式容器

```C++
//.bashrc的最后一行
export PS1='\[\e[36;47m\]\u\[\e[33;47m\]@\[\e[36;47m\]\h\[\e[35;47m\]:\[\e[31;47m\]\W\[\e[00m\]\$ '
 
//.vimrc下面，添加这么一行(多标签之间的切换)
nmap <Tab> :bn<cr> 
```

![image-20230610111113883](C++STL笔记.assets/image-20230610111113883.png)

#### 1、初始化

三种容器的初始化方式是完全一样。都有五种初始化的方式。

![image-20230610113018947](C++STL笔记.assets/image-20230610113018947.png)

#### 2、遍历

vector与deque有四种遍历方式，但是list没有重载下标访问运算符。（不支持下标）

![image-20230610113055057](C++STL笔记.assets/image-20230610113055057.png)

![image-20230610113121317](C++STL笔记.assets/image-20230610113121317.png)

==注意：list不支持下标访问==

![image-20230610114126622](C++STL笔记.assets/image-20230610114126622.png)

#### 3、在尾部进行插入与删除

三种容器的在尾部的插入与删除是一致的。

![image-20230610115650366](C++STL笔记.assets/image-20230610115650366.png)



## Day21

### 一、序列式容器

#### 1、在头部进行插入与删除

deque与list是支持在头部进行插入与删除的，但是vector不支持。

![image-20230612094903554](C++STL笔记.assets/image-20230612094903554.png)

![image-20230612094834183](C++STL笔记.assets/image-20230612094834183.png)



#### 2、vector的源码

![image-20230612095613269](C++STL笔记.assets/image-20230612095613269.png)

![image-20230612095756555](C++STL笔记.assets/image-20230612095756555.png)

![image-20230612100009537](C++STL笔记.assets/image-20230612100009537.png)

![image-20230612100938230](C++STL笔记.assets/image-20230612100938230.png)

```C++
class vector
{
public:
  typedef _Tp value_type;
  typedef value_type* pointer;
  typedef const value_type* const_pointer;
  typedef value_type* iterator;
  typedef const value_type* const_iterator;
  typedef value_type& reference;
  typedef const value_type& const_reference;
  typedef size_t size_type;
  typedef ptrdiff_t difference_type;
    
   typedef typename _Base::allocator_type allocator_type;
    
};
```

```C++
//泛型编程的思想
//类型萃取
Container::size_type 

Container::iterator 

//size_t是无法符号的，如果是-1，就会转变为最大值
for(size_t idx = 9; idx > 0; idx -= 2)
{
    //9 7 5 3 1 -1
}

for(int idx = 9; idx > 0; idx -= 2)
{
    //9 7 5 3 1 -1
}
```

at函数与下标都可以随机访问，但是at有范围检查，比下标更加安全一些。

![image-20230612110202907](C++STL笔记.assets/image-20230612110202907.png)

![image-20230612110231562](C++STL笔记.assets/image-20230612110231562.png)

#### 3、deque的源码

![image-20230612111159956](C++STL笔记.assets/image-20230612111159956.png)

![image-20230612111924643](C++STL笔记.assets/image-20230612111924643.png)

#### 4、在任意位置插入元素

![image-20230612142228386](C++STL笔记.assets/image-20230612142228386.png)

![image-20230612142311125](C++STL笔记.assets/image-20230612142311125.png)

#### 5、vector迭代器失效（==重要==）

在vector使用insert进行插入元素的时候，因为插入元素的**个数是不一定的**，所以有可能导致**底层发生扩容现象**，而如果没有重置迭代器，就有可能发生迭代器指向老的空间的现象，而下一次操作的时候是新的空间。为了解决这个问题，**每次使用迭代器的时候，将迭代器重新置位即可**（也就是让迭代器在使用的时候，与新的空间产生联系即可）

![image-20230612145352746](C++STL笔记.assets/image-20230612145352746.png)

#### 6、vector的删除会导致迭代器失效（==重要==）

![image-20230612150529657](C++STL笔记.assets/image-20230612150529657.png)

![image-20230612150657050](C++STL笔记.assets/image-20230612150657050.png)

#### 7、元素的清空

对于vector而言，提供了size()函数记录元素的个数，以及capacity()函数记录容量的大小，清空元素的时候，空间是没有回收的，所以可以使用shrink_to_fit()回收多余的空间。对于deque而言，提供了size()函数记录元素的个数的函数，但是没有提供capacity()函数记录容量的大小，但是提供了shrink_to_fit()回收多余的空间；对于list而言，删除元素的时候，也会回收空间，所以没有shrink_to_fit()函数。

![image-20230612153117518](C++STL笔记.assets/image-20230612153117518.png)

#### 8、list的特殊使用

##### sort函数

![image-20230612163018028](C++STL笔记.assets/image-20230612163018028.png)

![image-20230612163113101](C++STL笔记.assets/image-20230612163113101.png)

##### unique函数

![image-20230612163838086](C++STL笔记.assets/image-20230612163838086.png)

##### merge函数

![image-20230612164603105](C++STL笔记.assets/image-20230612164603105.png)

##### splice函数

![image-20230612173007054](C++STL笔记.assets/image-20230612173007054.png)

![image-20230612182003712](C++STL笔记.assets/image-20230612182003712.png)

![image-20230612182030375](C++STL笔记.assets/image-20230612182030375.png)

#### 9、vector的Insert扩容

![image-20230612181843554](C++STL笔记.assets/image-20230612181843554.png)



## Day22

### 一、问题回顾

1、序列式容器的初始化方式有哪几种？遍历有哪几种？

2、序列式容器的insert操作需要注意什么？

3、vector的迭代器失效？

4、list的特殊操作？



### 二、set的使用

```C++
1、如何将左值转换为右值
int a = 10;
std::move(a);//std::move本质就是做了一个强转，static_cast<T &&>(lvalue)

2、如何将右值转换为左值
int b = std::move(a);
int &&rref = std::move(a);

3、如何缩短变量的生命周期
void test
{
    {
        int a = 10;
    }
   
    int b = 20;
    
    int c = 10;
    //...
    //...
    //...
}
```

#### 1、set的特征

![image-20230613110000871](C++STL笔记.assets/image-20230613110000871.png)

#### 2、set的查找

![image-20230613100106574](C++STL笔记.assets/image-20230613100106574.png)

#### 3、insert操作

![image-20230613102848808](C++STL笔记.assets/image-20230613102848808.png)

#### 4、set不支持下标

![image-20230613105549557](C++STL笔记.assets/image-20230613105549557.png)

#### 5、不支持修改操作

![image-20230613105921062](C++STL笔记.assets/image-20230613105921062.png)



#### 6、针对于自定义类型（==重点==）

![image-20230613114710972](C++STL笔记.assets/image-20230613114710972.png)

![image-20230613114755562](C++STL笔记.assets/image-20230613114755562.png)

![image-20230613114848264](C++STL笔记.assets/image-20230613114848264.png)



### 三、multiset的使用

#### 1、multiset的特征

![image-20230613144721626](C++STL笔记.assets/image-20230613144721626.png)

#### 2、其他操作

查找操作count与find与set完全相同，插入操作insert，因为multiset可以存放重复元素，所以就没有返回类型是pair的，另外插入的一个元素、多个元素都与set完全一致。multiset也不支持下标，也不支持修改操作。

#### 3、查找函数

![image-20230613145944074](C++STL笔记.assets/image-20230613145944074.png)

#### 4、针对于自定义类型

使用方法类似与set容器，可以特化std::less、或者重载小于符号、或者写函数对象的形式。



### 四、map的使用

#### 1、map的特征

![image-20230613175720221](C++STL笔记.assets/image-20230613175720221.png)

#### 2、map的操作

![image-20230613151824614](C++STL笔记.assets/image-20230613151824614.png)

#### 3、map的插入操作

![image-20230613152721083](C++STL笔记.assets/image-20230613152721083.png)

#### 4、下标（==重要==）

```C++
templete <typename Container>
void fun(const Container &con)
{
    cout << con[2] << endl;
}
```

![image-20230613160211459](C++STL笔记.assets/image-20230613160211459.png)



![image-20230613155929189](C++STL笔记.assets/image-20230613155929189.png)

#### 5、针对于自定义类型

![image-20230613161743638](C++STL笔记.assets/image-20230613161743638.png)

如果map的key是一个自定义类型的时候，需要针对自定义类型实现std::less，否则会报错。
==注意：std::less针对的是key类型，而不是pair类型==





### 五、multimap的使用

#### 1、multimap的特征

![image-20230613162516258](C++STL笔记.assets/image-20230613162516258.png)

#### 2、其他操作

multimap的查找操作count与find与map是完全一样，插入操作insert基本与map一致。



#### 3、不支持下标访问

![image-20230613162728102](C++STL笔记.assets/image-20230613162728102.png)

#### 4、针对于自定义类型

与map是一样的。



### 六、哈希相关的概念

#### 1、哈希函数

通过key值找到对应的位置值。

```C++
index = H(key)
```

#### 2、构建方法

除留取余法：H(key) = key mod p (p <= m, m为表长)  



#### 3、哈希冲突（==重要==）

不同的key值，经过哈希函数之后，对应的位置值是一样的，称为哈希冲突

```C++
H(key1) = H(key2)   (key1 != key2)
```



#### 4、解决哈希冲突

链地址法

![image-20230613163942979](C++STL笔记.assets/image-20230613163942979.png)  

#### 5、装载因子

装载因子 a = (实际装载数据的长度n)/(表长m)



### 七、unordered_set的使用

#### 1、基本特征

![image-20230613171058874](C++STL笔记.assets/image-20230613171058874.png)

#### 2、针对于自定义类型(==重要==)

![image-20230613171522517](C++STL笔记.assets/image-20230613171522517.png)

##### 模板参数Hash的设计

![image-20230613173732078](C++STL笔记.assets/image-20230613173732078.png)

![image-20230613173829787](C++STL笔记.assets/image-20230613173829787.png)

##### 模板参数equal_to的设计

因为equal_to代表的是等号，也就是一个运算符，所以会多一个运算符的重载。

![image-20230613173941898](C++STL笔记.assets/image-20230613173941898.png)

![image-20230613174009542](C++STL笔记.assets/image-20230613174009542.png)

![image-20230613174049159](C++STL笔记.assets/image-20230613174049159.png)



### 八、unordered_multiset的使用

#### 1、基本特征

![image-20230613174910253](C++STL笔记.assets/image-20230613174910253.png)

#### 2、针对于自定义类型

基本使用方法与unordered_set完全一致。



## Day23

### 一、问题回顾

1、关联式容器的特点？

元素是排好序的、红黑树。

2、关联式容器的基本操作：初始化、遍历、查找（两个）、插入、删除、清空、交换操作？哪些具备下标？

map具备下标

3、针对自定义类型的方式有哪些？（重要）

模板的特化、函数对象形式（自定义函数对象）、进行运算符重载

4、无序关联式容器的底层实现是什么？

哈希



### 二、unordered_map的使用

#### 1、基本特征

![image-20230614095037715](C++STL笔记.assets/image-20230614095037715.png)

#### 2、下标

![image-20230614095113741](C++STL笔记.assets/image-20230614095113741.png)

#### 3、针对于自定义类型

常规的数据类型都已经做了std::hash的特化，string也做了hash的特化。

![image-20230614094759125](C++STL笔记.assets/image-20230614094759125.png)

![image-20230614094858227](C++STL笔记.assets/image-20230614094858227.png)

### 三、unordered_multimap的使用

#### 1、基本特征

![image-20230614095534426](C++STL笔记.assets/image-20230614095534426.png)

#### 2、不支持下标访问的

![image-20230614095601850](C++STL笔记.assets/image-20230614095601850.png)

#### 3、针对于自定义类型

与unordered_map完全一致。



### 四、优先级队列

![image-20230614100551563](C++STL笔记.assets/image-20230614100551563.png)

![image-20230614102711005](C++STL笔记.assets/image-20230614102711005.png)



### 五、容器的选择(==重点==)

#### 1、元素是有序的

**关联式容器**中的元素默认是有序的，无序关联式容器中的元素是没有顺序的。

#### 2、容器是否有下标

序列式容器：vector、deque。

关联式容器：map

无序关联式容器：unoredered_map

#### 3、时间复杂度

序列式容器：O(N)

关联式容器：O(logN)

无序关联式容器：O(1)

#### 4、迭代器的类型

随机访问迭代器：vector、deque
双向迭代器：list、关联式容器
前向迭代器：无序关联式容器

#### 5、是否所有的容器都具备迭代器

容器适配器是没有迭代器



## Day24

### 一、迭代器

#### 1、概念

概念：迭代器可以看成是一种指针。具备普通指针的功能。

本质：是种更高层次的抽象，它使得算法独立于容器

#### 2、类型

![image-20230614115518893](C++STL笔记.assets/image-20230614115518893.png)

#### 3、输出流迭代器

![image-20230615142407767](C++STL笔记.assets/image-20230615142407767.png)

```C++
class ostream_iterator
{
public:
    //ostream_iterator<int> osi(cout, "\n");
    //ostream_type& __s = cout
    //const _CharT* __c = "\n";
    //_M_stream = &cout;
    //_M_string = "\n"
    ostream_iterator(ostream_type& __s, const _CharT* __c) 
    : _M_stream(&__s)
    , _M_string(__c) 
    {}
    
    ostream_iterator<_Tp>& operator=(const _Tp& __value) { 
    *_M_stream << __value;
    if (_M_string) *_M_stream << _M_string;
    return *this;
  }
    
    ostream_iterator<_Tp>& operator*() 
    { 
        return *this; 
    }
    ostream_iterator<_Tp>& operator++() 
    { 
        return *this; 
    } 
    ostream_iterator<_Tp>& operator++(int) 
    { 
        return *this; 
    } 
private:
  ostream_type* _M_stream;
  const _CharT* _M_string;

};

_Trivial:平凡的、琐碎的。
POD类型。

template <class _InputIter, class _OutputIter>
inline _OutputIter copy(_InputIter __first, _InputIter __last,
                        _OutputIter __result) {
  __STL_REQUIRES(_InputIter, _InputIterator);
  __STL_REQUIRES(_OutputIter, _OutputIterator);
  return __copy_aux(__first, __last, __result, __VALUE_TYPE(__first));
}

template <class _InputIter, class _OutputIter, class _Tp>
inline _OutputIter __copy_aux(_InputIter __first, _InputIter __last,
                              _OutputIter __result, _Tp*) {
  typedef typename __type_traits<_Tp>::has_trivial_assignment_operator
          _Trivial;
  return __copy_aux2(__first, __last, __result, _Trivial());
}

template <class _InputIter, class _OutputIter>
inline _OutputIter __copy_aux2(_InputIter __first, _InputIter __last,
                               _OutputIter __result, __true_type) {
  return __copy(__first, __last, __result,
                __ITERATOR_CATEGORY(__first),
                __DISTANCE_TYPE(__first));
}

template <class _InputIter, class _OutputIter, class _Distance>
inline _OutputIter __copy(_InputIter __first, _InputIter __last,
                          _OutputIter __result,
                          input_iterator_tag, _Distance*)
{
  for ( ; __first != __last; ++__result, ++__first)
    *__result = *__first;
  return __result;
}

// __first = vec.begin()
//__last = vec.end()
// __result = osi
//vector<int> vec = {1, 4, 7, 9, 3};
copy(vec.begin(), vec.end(), osi);
              last
1, 4, 7, 9, 3
               f
                  
*osi = 7 ;  


ostream_iterator<_Tp>& operator=(const _Tp& __value) 
{ 
    cout << 7;
    if (_M_string) cout << "\n";
    return *this;
  }
```

#### 4、输入流迭代器

![image-20230615142437511](C++STL笔记.assets/image-20230615142437511.png)

```C++
class istream_iterator 
{
public:
    //istream_iterator<int> isi(std::cin);
    //istream_type& __s = cin;
    //_M_stream  = &cin;
    istream_iterator(istream_type& __s) 
    : _M_stream(&__s) 
    { 
        _M_read(); 
    }
    
    istream_iterator() 
    : _M_stream(0)
     , _M_ok(false) {}
    
    istream_iterator& operator++() 
    { 
        _M_read(); 
        return *this;
    }
    
    reference operator*() const 
    {
        return _M_value; 
    }
    
    bool _M_equal(const istream_iterator& __x) const
    { 
        return (_M_ok == __x._M_ok) && (!_M_ok || _M_stream == __x._M_stream); 
    }
private:
   istream_type* _M_stream;
   _Tp _M_value;
   bool _M_ok;
    
    if(cin)//operator bool(){}
    {
        
    }
    
     void _M_read() 
     {
         _M_ok = (_M_stream && *_M_stream) ? true : false;//三目运算符
         if (_M_ok) 
         {
             *_M_stream >> _M_value;//cin >> value
             _M_ok = *_M_stream ? true : false;
         }
     }

};


//__x1 = isi
//__y = istream_iterator<int>()
inline bool operator!=(const istream_iterator<_Tp, _CharT, _Traits, _Dist>& __x1,
                       const istream_iterator<_Tp, _CharT, _Traits, _Dist>& __y) 
{
  return !__x1._M_equal(__y);
}

bool _M_equal(const istream_iterator& __x) const
{ 
    return (_M_ok == __x._M_ok) && (!_M_ok || _M_stream == __x._M_stream); 
}

template <class _Container>
inline back_insert_iterator<_Container> back_inserter(_Container& __x) {
  return back_insert_iterator<_Container>(__x);
}


copy(isi, istream_iterator<int>(), std::back_inserter(vec));

//_InputIter __first = isi;
// _InputIter __last = istream_iterator<int>()
//_OutputIter __result = std::back_inserter(vec)
inline _OutputIter __copy(_InputIter __first, _InputIter __last,
                          _OutputIter __result,
                          input_iterator_tag, _Distance*)
{
  for ( ; __first != __last; ++__result, ++__first)
    *__result = *__first;
  return __result;
}

*__result = 2;



class back_insert_iterator {
public:
    back_insert_iterator<_Container>&  
    operator=(const typename _Container::value_type& __value) 
    { 
        container->push_back(__value);//调用了vector放入push_back将数据value插入到尾部
        return *this;
    }
    
    back_insert_iterator<_Container>& operator*()
    { 
        return *this; 
    }
    
    back_insert_iterator<_Container>& operator++() { return *this; }
    back_insert_iterator<_Container>& operator++(int) { return *this; }
}
```



#### 5、迭代器适配器

![image-20230615145427401](C++STL笔记.assets/image-20230615145427401.png)

![image-20230615145404261](C++STL笔记.assets/image-20230615145404261.png)

#### 6、反向迭代器

![image-20230615145553492](C++STL笔记.assets/image-20230615145553492.png)

![image-20230615150133826](C++STL笔记.assets/image-20230615150133826.png)



### 二、算法

算法库中的函数都是非成员函数（自由函数、全局函数）

#### 1、分类

1、非修改式的算法：**for_each**、count、find

2、修改式的算法：**copy**、**remove_if**、swap

3、排序算法：**sort**

4、二分搜索：lower_bound、upper_bound

5、集合操作：set_intersection

6、堆相关的操作：make_heap

7、取最值：max、min

8、未初始化的操作：uninitialized_copy



#### 2、for_each算法

一元函数：函数的参数只有一个。二元函数：函数的参数是两个。

一元谓词/断言：函数的参数只有一个，并且函数的返回类型是bool。

二元谓词/断言：函数的参数有两个，并且函数的返回类型是bool。

![image-20230615155933755](C++STL笔记.assets/image-20230615155933755.png)



#### 3、remove_if算法

![image-20230615173024206](C++STL笔记.assets/image-20230615173024206.png)

```C++
template<class ForwardIt, class UnaryPredicate>
ForwardIt remove_if(ForwardIt first, ForwardIt last, UnaryPredicate p)
{
    first = std::find_if(first, last, p);
    if (first != last)
        for(ForwardIt i = first; ++i != last; )
            if (!p(*i))
                *first++ = std::move(*i);
    return first;
}

template<class InputIt, class UnaryPredicate>
constexpr InputIt find_if(InputIt first, InputIt last, UnaryPredicate p)
{
    for (; first != last; ++first) {
        if (p(*first)) {
            return first;
        }
    }
    return last;
}


bool func(int value)
{   
     return value > 6;
} 

remove_if(number.begin(), number.end(), func);
vector<int> number = {2, 4, 6, 9, 8, 5, 3};
//ForwardIt first = number.begin();
//ForwardIt last = number.end()
//p = func
ForwardIt remove_if(ForwardIt first, ForwardIt last, UnaryPredicate p)
{
    first = std::find_if(first, last, p);
    if (first != last)
    {
         for(ForwardIt i = first; ++i != last; )
         {
               if (!p(*i))
               {
                   *first++ = std::move(*i);
               }               
         }         
    }
       
    return first;
}
         f
2, 4, 6, 9, 8, 5, 3
               i
               f      last
2, 4, 6, 5, 3, 5, 3
                      i

constexpr InputIt find_if(InputIt first, InputIt last, UnaryPredicate p)
{
    for (; first != last; ++first) {
        if (p(*first)) {
            return first;
        }
    }
    return last;
}

//有一种方式，可以将函数的某一个参数固定，那么就可以将二元函数转变为一元函数
bool func1(int x， int y = 6)====>bool func1(int x) { return x > 6;}
{
    return x > y;
}


bool func2(int x = 6， int y )====>bool func2(int y) { return 6 < y;}
{
    return 6 < y;
}
```

![image-20230615170047549](C++STL笔记.assets/image-20230615170047549.png)

![image-20230615172945918](C++STL笔记.assets/image-20230615172945918.png)



#### 4、迭代器失效

![image-20230615164455686](C++STL笔记.assets/image-20230615164455686.png)



#### 5、bind12的使用

![image-20230615173223185](C++STL笔记.assets/image-20230615173223185.png)



### 三、bind的使用

![image-20230615174443080](C++STL笔记.assets/image-20230615174443080.png)



## Day25

### 一、作业

```C++
ifstream ifs(filename);
if(!ifs)
{
    //....异常处理
}

//1、读一行，然后将一行的内容交给istringstream进行处理
string line;
while(getline(ifs, line))
{
    istringstream iss(line);//istringstream属于串IO
    string word;
    while(iss >> word)
    {
        //对word进行处理
    }
}

//2、直接使用ifs进行读操作
string word;
while(ifs >> word)//磁盘IO的次数就比较多
{
    //对word进行处理   
}

//3、一次将文件中的内容读到内存中
//打开文件的时候，可以使用追加模式
size_t len = ifs.tellg();
char buf[10000] = {0};//string buf;  buf.c_str();
ifs.read(buf, len);
istringstream iss(buf);//istringstream属于串IO
string word;
while(iss >> word)
{
    //对word进行处理
}


ifs.close();
```

![image-20230616105555835](C++STL笔记.assets/image-20230616105555835.png)



### 二、问题回顾

1、迭代器的种类？输出流迭代器与输入流迭代器的源码阅读？三对插入迭代器？

2、for_each算法与remove_if算法的传参，以及使用方法？

3、lambda表达式的使用？（C++11中的语法特性）



### 三、函数指针（==重要==）

![image-20230616111515800](C++STL笔记.assets/image-20230616111515800.png)



### 四、bind的使用（==重点==）

#### bind的占位符概念

![image-20230616113343957](C++STL笔记.assets/image-20230616113343957.png)

#### bind绑定到数据成员

![image-20230616114645619](C++STL笔记.assets/image-20230616114645619.png)





### 五、function的使用（==重要==）

![image-20230616114148349](C++STL笔记.assets/image-20230616114148349.png)

![image-20230616114134619](C++STL笔记.assets/image-20230616114134619.png)



### 六、左值与右值

```C++
int number = 10;
int &ref = number;//ok,左值引用，可以绑定到左值，不能绑定到右值
int &ref1 = 10;//error
const int &ref2 = 10;//ok
const int &ref3 = number;//ok
//const左值引用既可以绑定到左值，也可以绑定到右值。

//C++11里面提出了右值引用
int &&rref = 10;//ok,右值引用可以绑定到右值
int &&rref1 = number;//error
//结论：右值引用可以绑定到右值，但是不能绑定到左值。


int &&func()
{
    return 10;
}

class String
{
public:
    String(const String &rhs)
    : _pstr(new char[strlen(rhs._pstr) + 1]())
    {
        
    }
 
    
    String(String &&rhs)
    : _pstr(rhs._pstr)
    {
        rhs._pstr = nullptr;
    }
    
    //赋值运算符函数
    String &operator=(const String &rhs)
    {
        if(this != &rhs)
        {
            delete [] _pstr;
            _pstr = nullptr;
            
            //深拷贝
            _pstr = new char[strlen(rhs._pstr) + 1]();
            strcpy(_pstr, rhs._pstr);
        }
        
        return *this;
    }
    
    //移动赋值函数
    String &operator=(String &&rhs)//String &&rhs = std::move(cb)
    {
        if(this != &rhs)
        {
            delete [] _pstr;
            _pstr = nullptr;
            
            //浅拷贝
            _pstr = rhs._pstr;
            rhs._pstr = nullptr;
        }
        
        return *this;
    }
    
private:
    char *_pstr;
}

String s1 = String("hello");
```



### 七、bind与function结合使用

![image-20230616155016792](C++STL笔记.assets/image-20230616155016792.png)

![image-20230616155035520](C++STL笔记.assets/image-20230616155035520.png)



### 八、成员函数适配器mem_fn

![image-20230616162627009](C++STL笔记.assets/image-20230616162627009.png)



### 九、函数对象（仿函数）

所有与小括号结合，体现函数的含义的都称为函数对象

- 普通函数名
- 函数指针
- 重载了函数调用运算符的类创建的对象



### 十、空间配置器（==重要==）

![image-20230616163708735](C++STL笔记.assets/image-20230616163708735.png)

会将空间的申请与释放以及对象的构建与销毁严格的分开。

在STL中，对象往往不是一个一个申请，而是大批量申请的，所以不能创建一个对象就申请一片空间，这样空间的申请就比较频繁。

```C++
Point pt(1, 2);
```



#### 四个重要函数

```C++
#include <memory>

//空间的申请
T* allocate( std::size_t n );

//空间的释放
void deallocate( T* p, std::size_t n );

//对象的构建
void construct( pointer p, const_reference val );

//对象的销毁
void destroy( pointer p );
```

![image-20230617130609497](C++STL笔记.assets/image-20230617130609497.png)





```C++
class Base
{
    virtual print()
    {
        
    }
    
    void func1()
    {
        this->print();
    }
    
    void func2()
    {
        Base::print();
    }
}


class Derived: public Base
{
    virtual print()
    {
        
    }
}

void test()
{
    Base *pbase1 = &derived;
    pbase1->func1();
    pbase1->func2();
}
```

```C++
class Base1
{
public:
    virtual void print1()
    {
        
    }
private:
    int _ibase1;
}


class Base2
{
public:
    virtual void print2()
    {
        
    }
private:
    int _ibase2;
}

class Base3
{
public:
    virtual void print3()
    {
        
    }
private:
    int _ibase3;
}


class Derived
:  virtual public Base1
,virtual public Base2
,virtual public Base3
{
public:
    virtual void print()
    {
        
    }
private:
    int _idervied;
}

_vbptr
_idervied;

vfptr
_ibase;



//_vfptr
_vbptr    
_idervied
_vfptr
_ibase1 
_vfptr
_ibase2 
_vfptr
_ibase3
```



```C++
class Singleton
{
private:
    class AutoRelease
    {
        
    };
private:
    static AutoRelease _ar;
};
```


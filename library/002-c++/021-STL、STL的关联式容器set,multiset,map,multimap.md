# c++学习笔记——21.STL、STL的关联式容器set,multiset,map,multimap

1.set

```c++
#include <math.h>
#include <iostream>
#include <set>
#include <vector>

using std::cout;
using std::endl;
using std::set;
using std::vector;

template <typename Container>
void display(const Container &c)
{
    for(auto &elem : c)
    {
        cout << elem << " ";
    }
    cout << endl;
}

void test()
{
    //set不能存放关键相同的元素
    set<int> numbers{1, 3, 7, 9, 8, 6, 4, 2, 5, 1, 5};
    /* set<int,std::greater<int>> numbers{1, 3, 7, 9, 8, 6, 4, 2, 5, 1, 5}; */
    display(numbers);

    //set不支持下标访问运算符
    /* cout << "neumers[0] = " << numbers[0] << endl;//error */
    auto sit = numbers.begin();
    ++sit;
    cout << "*sit = " << *sit << endl;

    //set元素的查找
    cout << endl << "容器的查找 : " << endl;
    size_t cnt = numbers.count(1);
    size_t cnt2 = numbers.count(10);
    cout << "cnt = " << cnt << endl;
    cout << "cnt2 = " << cnt2 << endl;

    /* set<int>::iterator it = numbers.find(9); */
    set<int>::iterator it = numbers.find(10);
    if(it == numbers.end())
    {
        cout << "该元素不存在number中" << endl;
    }
    else
    {
        cout << "该元素存在numbers中 ： "  << *it << endl;
    }

    //set的插入(添加元素)
    cout << endl << "对容器执行insert操作: " << endl;
    /* std::pair<set<int>::iterator, bool> ret = numbers.insert(1); */
    /* std::pair<set<int>::iterator, bool> ret = numbers.insert(10); */
    auto  ret = numbers.insert(10);
    if(ret.second)
    {
        cout << "添加成功" << *ret.first << endl;
    }
    else
    {
        cout << "添加失败，这个元素已经存在set之中: " << endl;
    }

    //添加一对迭代器范围元素
    cout << endl << endl;
    vector<int> vec{10, 9, 8, 5, 30, 20, 11, 39};
    numbers.insert(vec.begin(), vec.end());
    display(numbers);

    cout << endl << endl;
    numbers.insert(std::initializer_list<int>({100, 21, 500}));
    display(numbers);

    //set的删除erase
    cout << endl << "删除元素" << endl;
    auto it2 = numbers.begin();
    ++it2;
    ++it2;
    ++it2;
    numbers.erase(it2);
    display(numbers);

    //红黑树调整：左旋/右旋
    //红黑树：
    //1、节点不是红色就是黑色
    //2、根节点是黑色的
    //3、叶子节点也是黑色
    //4、如果一个节点是红色的，它的左右孩子节点必须是黑色
    //5、从根节点到叶子节点上所有路径要保证黑色节点的个数要相同
    //
    //set修改元素
    it2 = numbers.begin();
    /* *it2 = 200;//error */

}

class Point
{
public:
    Point(double dx = 0, double dy = 0)
    : _dx(dx)
    , _dy(dy)
    {
        /* cout << "Point(double = 0, double = 0)" << endl; */
    }

    void print()  const
    {
        cout << "(" << _dx 
             << ", " << _dy 
             << ")" << endl;
    }
    ~Point()
    {
        /* cout << "~Point()" << endl; */
    }

    double getDistance() const
    {
        return hypot(_dx, _dy);
    }
    friend class PointComparator;
    friend bool operator<(const Point &lhs, const Point &rhs);
    friend bool operator>(const Point &lhs, const Point &rhs);
    friend std::ostream &operator<<(std::ostream &os, const Point &rhs);

private:
    double _dx;
    double _dy;
};
bool operator<(const Point &lhs, const Point &rhs)
{
    if(lhs.getDistance() < rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return lhs._dx < rhs._dx;
    }
    else
    {
        return false;
    }
}
bool operator>(const Point &lhs, const Point &rhs)
{
    cout << "bool operator>(const Point &, const Point &)" << endl;
    if(lhs.getDistance() > rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return lhs._dx > rhs._dx;
    }
    else
    {
        return false;
    }
}
std::ostream &operator<<(std::ostream &os, const Point &rhs)
{
    os << "(" << rhs._dx 
       << ", "  << rhs._dy
       <<")" << endl;

    return os;
}

//函数调用
struct PointComparator
{
    
    bool operator()(const Point &lhs, const Point &rhs)
    {
        cout << "bool PointComparator::operator()(const Point &, const Point &)" << endl;
        if(lhs.getDistance() > rhs.getDistance())
        {
            return true;
        }
        else if(lhs.getDistance() == rhs.getDistance())
        {
            return (lhs._dx > rhs._dx) || (lhs._dy > rhs._dy);
        }
        else
        {
            return false;
        }

    }
};
void test2()
{
    /* set<Point> points{ */
    /* set<Point,std::greater<Point>> points{ */
    set<Point, PointComparator> points{
        Point(1, 2),
        Point(3, 4),
        Point(-1, 2),
        Point(3, 4),
        Point(0, 6),
    };
    display(points);
}
int main(int argc, char **argv)
{
    test2();
    return 0;
}


```



2.multiset

```c++
#include <math.h>
#include <iostream>
#include <set>
#include <vector>

using std::cout;
using std::endl;
using std::multiset;
using std::vector;

template <typename Container>
void display(const Container &c)
{
    for(auto &elem : c)
    {
        cout << elem << " ";
    }
    cout << endl;
}

void test()
{
    //multiset可以存放关键相同的元素
    multiset<int> numbers{1, 3, 7, 9, 2, 2, 2, 8, 6, 4, 2, 5, 1, 5};
    /* multiset<int,std::greater<int>> numbers{1, 3, 7, 9, 8, 6, 4, 2, 5, 1, 5}; */
    display(numbers);

    //multiset不支持下标访问运算符
    /* cout << "neumers[0] = " << numbers[0] << endl;//error */
    auto sit = numbers.begin();
    ++sit;
    cout << "*sit = " << *sit << endl;

    //multiset元素的查找
    cout << endl << "容器的查找 : " << endl;
    size_t cnt = numbers.count(1);
    size_t cnt2 = numbers.count(10);
    cout << "cnt = " << cnt << endl;
    cout << "cnt2 = " << cnt2 << endl;

    /* multiset<int>::iterator it = numbers.find(9); */
    multiset<int>::iterator it = numbers.find(10);
    if(it == numbers.end())
    {
        cout << "该元素不存在number中" << endl;
    }
    else
    {
        cout << "该元素存在numbers中 ： "  << *it << endl;
    }

    //multiset的插入(添加元素)
    cout << endl << "对容器执行insert操作: " << endl;
    /* std::pair<multiset<int>::iterator, bool> ret = numbers.insert(1); */
    /* std::pair<multiset<int>::iterator, bool> ret = numbers.insert(10); */
    auto  ret = numbers.insert(10);
    display(numbers);
#if 0
    if(ret.second)
    {
        cout << "添加成功" << *ret.first << endl;
    }
    else
    {
        cout << "添加失败，这个元素已经存在multiset之中: " << endl;
    }
#endif
    //添加一对迭代器范围元素
    cout << endl << endl;
    vector<int> vec{10, 9, 8, 5, 30, 20, 11, 39};
    numbers.insert(vec.begin(), vec.end());
    display(numbers);

    cout << endl << endl;
    numbers.insert(std::initializer_list<int>({100, 21, 500}));
    display(numbers);

    //multiset的删除erase
    cout << endl << "删除元素" << endl;
    auto it2 = numbers.begin();
    ++it2;
    ++it2;
    ++it2;
    numbers.erase(it2);
    display(numbers);

    //红黑树调整：左旋/右旋
    //红黑树：
    //1、节点不是红色就是黑色
    //2、根节点是黑色的
    //3、叶子节点也是黑色
    //4、如果一个节点是红色的，它的左右孩子节点必须是黑色
    //5、从根节点到叶子节点上所有路径要保证黑色节点的个数要相同
    //
    //multiset修改元素
    it2 = numbers.begin();
    /* *it2 = 200;//error */

    cout << endl << "查找范围的元素: " << endl;
    it = numbers.lower_bound(2);//不大于key的第一个位置
    it2 = numbers.upper_bound(2);//大于key的第一个位置
    /* cout << "*it = " << *it << endl; */
    /* cout << "*it2 = " << *it2 << endl; */
    while(it != it2)
    {
        cout << *it << " ";
        ++it;
    }
    cout << endl;

    cout << endl << endl;
    std::pair<multiset<int>::iterator, multiset<int>::iterator> ret2 = numbers.equal_range(2);
    /* auto ret2 = numbers.equal_range(2); */
    while(ret2.first != ret2.second)
    {
        cout << *ret2.first << " ";
        ++ret2.first;
    }
    cout << endl;

}
#if 1
class Point
{
public:
    Point(double dx = 0, double dy = 0)
    : _dx(dx)
    , _dy(dy)
    {
        /* cout << "Point(double = 0, double = 0)" << endl; */
    }

    void print()  const
    {
        cout << "(" << _dx 
             << ", " << _dy 
             << ")" << endl;
    }
    ~Point()
    {
        /* cout << "~Point()" << endl; */
    }

    double getDistance() const
    {
        return hypot(_dx, _dy);
    }
    friend class PointComparator;
    friend bool operator<(const Point &lhs, const Point &rhs);
    friend bool operator>(const Point &lhs, const Point &rhs);
    friend std::ostream &operator<<(std::ostream &os, const Point &rhs);

private:
    double _dx;
    double _dy;
};
bool operator<(const Point &lhs, const Point &rhs)
{
    if(lhs.getDistance() < rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return lhs._dx < rhs._dx;
    }
    else
    {
        return false;
    }
}
bool operator>(const Point &lhs, const Point &rhs)
{
    cout << "bool operator>(const Point &, const Point &)" << endl;
    if(lhs.getDistance() > rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return lhs._dx > rhs._dx;
    }
    else
    {
        return false;
    }
}
std::ostream &operator<<(std::ostream &os, const Point &rhs)
{
    os << "(" << rhs._dx 
       << ", "  << rhs._dy
       <<")" << endl;

    return os;
}

//函数调用
struct PointComparator
{
    
    bool operator()(const Point &lhs, const Point &rhs)
    {
        cout << "bool PointComparator::operator()(const Point &, const Point &)" << endl;
        if(lhs.getDistance() > rhs.getDistance())
        {
            return true;
        }
        else if(lhs.getDistance() == rhs.getDistance())
        {
            return (lhs._dx > rhs._dx) || (lhs._dy > rhs._dy);
        }
        else
        {
            return false;
        }

    }
};
void test2()
{
    /* multiset<Point> points{ */
    /* multiset<Point,std::greater<Point>> points{ */
    multiset<Point, PointComparator> points{
        Point(1, 2),
        Point(3, 4),
        Point(-1, 2),
        Point(1, -2),
        Point(3, 4),
        Point(0, 6),
    };
    display(points);
}
#endif
int main(int argc, char **argv)
{
    test();
    return 0;
}


```



3.map

```c++
#include <math.h>
#include <iostream>
#include <map>
#include <string>

using std::cout;
using std::endl;
using std::map;
using std::string;
using std::pair;

template <typename Container>
void display(const Container &c)
{
    for(auto &elem : c)
    {
        cout << elem.first << "--->" 
             << elem.second << endl;
    }
}

void test()
{
    //map存放关键字key唯一,默认排序方式是升序的
    map<int, string, std::greater<int>> cities{
    /* map<int, string> cities{ */
        pair<int,string>(1, "北京"),
        pair<int,string>(2, "上海"),
        std::make_pair(3, "广州"),
        std::make_pair(4, "深圳"),
        std::make_pair(1, "武汉"),
    };
    display(cities);

    //map支持下标访问运算符
    cout << endl;
    cout << "cities[1] = " << cities[1] << endl;
    cout << "cities[0] = " << cities[0] << endl;
    cities[0] = "长沙";
    display(cities);
}

class Point
{
public:
    Point(double dx = 0, double dy = 0)
    : _dx(dx)
    , _dy(dy)
    {
        cout << "Point(double = 0, double = 0)" << endl;
    }

    ~Point()
    {
        /* cout << "~Point()" << endl; */
    }

    double getDistance() const
    {
        return hypot(_dx, _dy);
    }
    friend class PointComparator;
    friend bool operator<(const Point &lhs, const Point &rhs);
    friend bool operator>(const Point &lhs, const Point &rhs);
    friend std::ostream &operator<<(std::ostream &os, const Point &rhs);

private:
    double _dx;
    double _dy;
};

bool operator<(const Point &lhs, const Point &rhs)
{
    cout << "bool operator<(const Point &, const Point &)" << endl;
    if(lhs.getDistance() < rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return (lhs._dx < rhs._dx) || (lhs._dy < rhs._dy) ;
    }
    else
    {
        return false;
    }
}

bool operator>(const Point &lhs, const Point &rhs)
{
    cout << "bool operator>(const Point &, const Point &)" << endl;
    if(lhs.getDistance() > rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return (lhs._dx > rhs._dx) || (lhs._dy > rhs._dy) ;
    }
    else
    {
        return false;
    }
}
std::ostream &operator<<(std::ostream &os, const Point &rhs)
{
    os << "(" << rhs._dx 
       << ", "  << rhs._dy
       <<")" << endl;

    return os;
}
#if 0
//函数调用
struct PointComparator
{
    
    bool operator()(const Point &lhs, const Point &rhs)
    {
        cout << "bool PointComparator::operator()(const Point &, const Point &)" << endl;
        if(lhs.getDistance() > rhs.getDistance())
        {
            return true;
        }
        else if(lhs.getDistance() == rhs.getDistance())
        {
            return (lhs._dx > rhs._dx) || (lhs._dy > rhs._dy);
        }
        else
        {
            return false;
        }

    }
};
#endif

void test2()
{
    /* map<string, Point> points{ */
    /* map<string, Point, std::greater<string>> points{ */
    map<string, Point> points{
        pair<string, Point>("1", Point(1, 2)),
        pair<string, Point>("22", Point(-1, 2)),
        std::make_pair("333", Point(5, 6)),
        std::make_pair("4444", Point(0, 6)),
        std::make_pair("22", Point(0, 6)),
    };
    display(points);

    cout << endl << "map下标访问运算" << endl;
    //时间复杂度O(logN)
    cout << "points[\"1\"] = " << points["1"] << endl;
    cout << "points[\"0\"] = " << points["0"] << endl;
    points["0"] = Point(10, 20);
    display(points);

    cout << endl << "在map进行insert: " << endl;
    /* std::pair<map<string, Point>::iterator, bool> ret3 = */ 
    auto ret3 = 
        /* points.insert(std::make_pair("333", Point(10, 40))); */
        points.insert(std::make_pair("999", Point(10, 40)));
    if(ret3.second)
    {
        cout << "添加元素成功 :  " << ret3.first->first << "---->"
             << ret3.first->second << endl;
    }
    else
    {
        cout << "添加失败，该元素存在于map之中 : " << ret3.first->first << "--->"
             << ret3.first->second << endl;
    }
}
int main(int argc, char **argv)
{
    test2();
    return 0;
}


```



4.multimap

```c++
#include <math.h>
#include <iostream>
#include <map>
#include <string>

using std::cout;
using std::endl;
using std::multimap;
using std::string;
using std::pair;

template <typename Container>
void display(const Container &c)
{
    for(auto &elem : c)
    {
        cout << elem.first << "--->" 
             << elem.second << endl;
    }
}

void test()
{
    //multimap存放关键字key不唯一,默认排序方式是升序的
    /* multimap<int, string, std::greater<int>> cities{ */
    multimap<int, string> cities{
        pair<int,string>(1, "北京"),
        pair<int,string>(2, "上海"),
        std::make_pair(3, "广州"),
        std::make_pair(4, "深圳"),
        std::make_pair(1, "武汉"),
    };
    display(cities);
#if 0
    //multimap不支持下标访问运算符
    cout << endl;
    cout << "cities[1] = " << cities[1] << endl;//error
    cout << "cities[0] = " << cities[0] << endl;//error
    cities[0] = "长沙";
    display(cities);
#endif
}
#if 1
class Point
{
public:
    Point(double dx = 0, double dy = 0)
    : _dx(dx)
    , _dy(dy)
    {
        cout << "Point(double = 0, double = 0)" << endl;
    }

    ~Point()
    {
        /* cout << "~Point()" << endl; */
    }

    double getDistance() const
    {
        return hypot(_dx, _dy);
    }

    friend class PointComparator;
    friend bool operator<(const Point &lhs, const Point &rhs);
    friend bool operator>(const Point &lhs, const Point &rhs);
    friend std::ostream &operator<<(std::ostream &os, const Point &rhs);

private:
    double _dx;
    double _dy;
};

bool operator<(const Point &lhs, const Point &rhs)
{
    cout << "bool operator<(const Point &, const Point &)" << endl;
    if(lhs.getDistance() < rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return (lhs._dx < rhs._dx) || (lhs._dy < rhs._dy) ;
    }
    else
    {
        return false;
    }
}

bool operator>(const Point &lhs, const Point &rhs)
{
    cout << "bool operator>(const Point &, const Point &)" << endl;
    if(lhs.getDistance() > rhs.getDistance())
    {
        return true;
    }
    else if(lhs.getDistance() == rhs.getDistance())
    {
        return (lhs._dx > rhs._dx) || (lhs._dy > rhs._dy) ;
    }
    else
    {
        return false;
    }
}
std::ostream &operator<<(std::ostream &os, const Point &rhs)
{
    os << "(" << rhs._dx 
       << ", "  << rhs._dy
       <<")" << endl;

    return os;
}
#if 1
//函数调用
struct PointComparator
{
    
    bool operator()(const string &lhs, const string &rhs)
    {
        cout << "bool PointComparator::operator()(const Point &, const Point &)" << endl;
        if(lhs > rhs)
        {
            return true;
        }
        else
        {
            return false;
        }

    }
};
#endif

void test2()
{
    /* multimap<string, Point> points{ */
    multimap<string, Point, std::greater<string>> points{
    /* multimap<string, Point, PointComparator> points{ */
        pair<string, Point>("1", Point(1, 2)),
        pair<string, Point>("22", Point(-1, 2)),
        std::make_pair("333", Point(5, 6)),
        std::make_pair("4444", Point(0, 6)),
        std::make_pair("22", Point(0, 6)),
    };
    display(points);

    /* cout << endl << "multimap下标访问运算" << endl; */
    /* //时间复杂度O(logN) */
    /* cout << "points[\"1\"] = " << points["1"] << endl; */
    /* cout << "points[\"0\"] = " << points["0"] << endl; */
    /* points["0"] = Point(10, 20); */
    /* display(points); */

    cout << endl << "在multimap进行insert: " << endl;
    /* std::pair<multimap<string, Point>::iterator, bool> ret3 = */ 
    auto ret3 = 
        /* points.insert(std::make_pair("333", Point(10, 40))); */
        points.insert(std::make_pair("999", Point(10, 40)));
    display(points);
    /* if(ret3.second) */
    /* { */
    /*     cout << "添加元素成功 :  " << ret3.first->first << "---->" */
    /*          << ret3.first->second << endl; */
    /* } */
    /* else */
    /* { */
    /*     cout << "添加失败，该元素存在于multimap之中 : " << ret3.first->first << "--->" */
    /*          << ret3.first->second << endl; */
    /* } */
}
#endif
int main(int argc, char **argv)
{
    test2();
    return 0;
}


```

5.unordered_set和unordered_map

```c++
#include <math.h>
#include <iostream>
#include <unordered_set>
#include <unordered_map>
#include <vector>
#include <string>
#include <ostream>

using std::cout;
using std::cin;
using std::endl;
using std::unordered_set;
using std::unordered_map;
using std::vector;
using std::string;
using std::ostream;
using std::make_pair;
template <typename Container>
void display(const Container &c)
{
    for(auto &elem : c)
    {
        cout << elem.first << " -- "
            <<elem.second<<endl;
    }
    cout << endl;
}

class Point
{
private:
    int _ix;
    int _iy;

public:
    Point()
        : _ix(0), _iy(0)
    {
        // cout << "Point()" << endl;
    }
    Point(int a, int b)
        : _ix(a), _iy(b)
    {
        // cout << "Point(int,int)" << endl;
    }
    ~Point()
    {
        // cout << "~Point()" << endl;
    }
    void print()
    {
        cout << "(" << _ix << "," << _iy << ")" << endl;
    }
    double getDistance() const
    {
        return hypot(_ix,_iy);
    } 
    int getX() const
    {
        return _ix;
    }
    int getY() const
    {
        return _iy;
    }
    friend ostream & operator<<(ostream &out,const Point &p) ;
};
#if 0
bool operator>(const Point &lhs,const Point &rhs)
{
    if (lhs.getDistance() > rhs.getDistance())
    {
        return true;
    }
    else if (lhs.getDistance() == rhs.getDistance())
    {
        return (lhs.getX() > rhs.getX()) ||
               (lhs.getY() > rhs.getY());
    }
    else
    {
        return false;
    }
}
bool operator<(const Point &lhs,const Point &rhs)
{
    if (lhs.getDistance() < rhs.getDistance())
    {
        return true;
    }
    else if (lhs.getDistance() == rhs.getDistance())
    {
        return (lhs.getX() < rhs.getX()) ||
               (lhs.getY() < rhs.getY());
    }
    else
    {
        return false;
    }
}
#endif
#if 1
bool operator==(const Point &lhs,const Point &rhs)
{
    return (lhs.getX()==rhs.getX())&&(lhs.getY()==rhs.getY());
}
#endif
ostream & operator<<(ostream &out,const Point &p) 
{
     out<<"("<<p._ix<<","<<p._iy<<")";
     return out;
}
#if 0
namespace std
{   
    template<>
    struct less<Point>
    {
        bool operator()(const Point &lhs,const Point &rhs)
        {
            if(lhs.getDistance()<rhs.getDistance())
            {
                return true;
            }else if (lhs.getDistance()==rhs.getDistance())
            {
                return (lhs.getX()<rhs.getX())||
                (lhs.getY()<rhs.getY());
            }else
            {
                return false;
            }
        }
    };   
    template<>
    struct greater<Point>
    {
        bool operator()(const Point &lhs,const Point &rhs)
        {
            if(lhs.getDistance()>rhs.getDistance())
            {
                return true;
            }else if (lhs.getDistance()==rhs.getDistance())
            {
                return (lhs.getX()>rhs.getX())||
                (lhs.getY()>rhs.getY());
            }else
            {
                return false;
            }
        }
    };   
}
#endif
//仿函数调用
struct PointGreaterComparator
{
    bool operator()(const Point &lhs, const Point &rhs)
    {
        if (lhs.getDistance() > rhs.getDistance())
        {
            return true;
        }
        else if (lhs.getDistance() == rhs.getDistance())
        {
            return (lhs.getX() > rhs.getX()) ||
                   (lhs.getY() > rhs.getY());
        }
        else
        {
            return false;
        }
    }
};
namespace std
{
    template<>
    struct hash<Point>
    {
        size_t operator()(const Point &pt) const
        {
            return (pt.getX()<<1)^(pt.getY()<<1);
        }
    };
}
struct Pointhash
{
    size_t operator()(const Point &pt) const
    {
        return (pt.getX() << 1) ^ (pt.getY() << 1);
    }
};
#if 0
void test_set_point()
{
    // unordered_set<Point,Pointhash> points{//可以通过仿函数(函数对象)调用
    unordered_set<Point> points{
        Point(1, 2),
        Point(3, 4),
        Point(-1, 2),
        Point(3, 4),
        Point(0, 6)
    };
    display(points);

    cout<<endl<<"在无序容器中插入"<<endl;
    auto it=points.insert(Point(7,9));

    display(points);
}
#endif
void test_map_point()
{
    // unordered_set<Point,Pointhash> points{//可以通过仿函数(函数对象)调用
    unordered_map<Point,string> points{
        make_pair(Point(1, 2),"12"),
        make_pair(Point(3, 4),"34"),
        make_pair(Point(-1, 2),"-12"),
        make_pair(Point(3, 4),"34"),
        make_pair(Point(0, 6),"06")
    };
    display(points);

    cout<<endl<<"在无序容器中插入"<<endl;
    auto it=points.insert(make_pair(Point(7,9),"79"));

    display(points);
}
int main(int argc,char **argv)
{
    // test_set_point();
    test_map_point();
    return 0;
}

```


# c++学习笔记——22.iterator,reverseiterator,priority_queue,foreach,copy的用法

### 1.priority_queue

```c++
#include <math.h>
#include <iostream>
#include <vector>
#include <string>
#include <ostream>
#include <queue>

using std::cout;
using std::cin;
using std::endl;
using std::vector;
using std::string;
using std::priority_queue;
using std::ostream;
using std::make_pair;
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
#if 1
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
void test_priority_queue()
{
    vector<int> num{1,4,5,2,3,7,6,9,8};
    // priority_queue<int,vector<int>,std::less<int>> myque;
    priority_queue<int> myque;
    for (size_t i = 0; i < num.size(); ++i)
    {
        myque.push(num[i]);
        cout<<"当前优先级最高是"<<myque.top()<<endl;
    }

    while(!myque.empty())
    {
        cout<<myque.top()<<"";
        myque.pop();
    }
    cout<<endl;
    
}
void test_priority_queue_point()
{
    vector<Point> points{
        Point(1, 2),
        Point(3, 4),
        Point(-1, 2),
        Point(3, 4),
        Point(0, 6)
        };
    // priority_queue<Point> myque;
    priority_queue<Point,vector<Point>,std::greater<Point>> myque;
    for (size_t i = 0; i < points.size(); ++i)
    {
        myque.push(points[i]);
        cout<<"当前优先级最高是"<<myque.top()<<endl;
    }

    while(!myque.empty())
    {
        cout<<myque.top()<<"";
        myque.pop();
    }
    cout<<endl;

}
int main(int argc,char **argv)
{
    // test_priority_queue();
    test_priority_queue_point();
    
    return 0;
}

```



### 2.iterator和ostream_iterator

```c++
#include <iostream>
#include <iterator>
#include <vector>
#include <algorithm>
#include <list>
#include <set>

using std::cout;
using std::cin;
using std::endl;
using std::ostream_iterator;
using std::istream_iterator;
using std::vector;
using std::copy;
using std::list;
using std::set;
using std::back_insert_iterator;
using std::front_insert_iterator;
using std::insert_iterator;

void test()
{
    vector<int> num1{1,5,8};
    list <int> num2{44,55,66};
    copy(num2.begin(),num2.end(),back_insert_iterator<vector<int>>(num1));
    copy(num1.begin(),num1.end(),ostream_iterator<int>(cout,"-"));

    cout<<endl;
    copy(num1.begin(),num1.end(),front_insert_iterator<list<int>>(num2));
    copy(num2.begin(),num2.end(),ostream_iterator<int>(cout,"-"));
    cout<<endl;


    set<int> num3{177,277,377,477};
    auto sit=num3.begin();
    ++sit;
    copy(num1.begin(),num1.end(),insert_iterator<set<int>>(num3,sit));
    copy(num3.begin(),num3.end(),ostream_iterator<int>(cout,"-"));
    cout<<endl;



}
int main(int argc,char **argv)
{
    test(); 
    return 0;
}

```

```c++
#include <iostream>
#include <iterator>
#include <vector>
#include <algorithm>
using std::cout;
using std::cin;
using std::endl;
using std::ostream_iterator;
using std::vector;
using std::copy;

void test()
{
    vector<int> num{3,4,5,1,2};

    ostream_iterator<int> osi(cout,"-");
    copy(num.begin(),num.end(),osi);
    cout<<endl;
}
int main(int argc,char **argv)
{
    
    test();
    return 0;
}

```



### 3.reverse_iterator

```c++
#include <iostream>
#include <vector>
#include <algorithm>
using std::cout;
using std::cin;
using std::endl;
using std::vector;

void test()
{
    vector<int> num{1,2,3,4,5};
    // vector<int>::reverse_iterator rit=num.rbegin();
    auto rit=num.rbegin();
    for(;rit!=num.rend();++rit)
    {
        cout<<*rit<<"--";
    }
    cout<<endl;
}
int main(int argc,char **argv)
{
    test();
    return 0;
}

```

### 4.for_each

```c++
#include <iostream>
#include <vector>
#include <algorithm>

using std::cout;
using std::cin;
using std::for_each;
using std::vector;
using std::endl;

void display(int &num)
{
    num-=5;
    cout<<num<<"||";
}
void test()
{
    vector<int> num{2,3,1,4,5,6,9,8,7};
    std::sort(num.begin(),num.end());
    for_each(num.begin(),num.end(),display);

    cout<<endl;
    //lambda
    for_each(num.begin(),num.end(),[](int &number){number=-number;cout<<number<<"||";});
    cout<<endl;
    
    for(auto &e:num)
    {
        cout<<e<<" ";
    }
    //时间复杂度为O(N)
    cout<<endl;
    int ret=std::count(num.begin(),num.end(),4);
    cout<<"ret="<<ret<<endl;
    //时间复杂度为O(N)
    cout<<endl;
    auto it=std::find(num.begin(),num.end(),4);
    cout<<"*it="<<*it<<endl;
    //时间复杂度为O(log(n))
    cout<<endl;
    std::sort(num.begin(),num.end());
    for(auto &e:num)
    {
        cout<<e<<" ";
    }
    auto flg=std::binary_search(num.begin(),num.end(),4);
    cout<<"flg="<<flg<<endl;

}
int main(int argc,char **argv)
{
    test(); 
    return 0;
}

```


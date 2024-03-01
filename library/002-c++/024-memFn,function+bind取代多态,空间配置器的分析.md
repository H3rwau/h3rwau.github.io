# c++学习笔记——24.memFn,function+bind取代多态,空间配置器的分析

### 1.memFn

```c++
#include <iostream>
#include <functional>
#include <vector>
#include <algorithm>

using std::cout;
using std::endl;
using std::vector;
using std::mem_fn;

class Number
{
public:
    Number(size_t data = 0)
    : _data(data)
    {

    }

    void print() const
    {
        cout << _data << " ";
    }

    bool isEven() const
    {
        return (0 == _data % 2);
    }

    bool isPrime() const
    {
        if(1 == _data)
        {
            return false;
        }
        //质数/素数
        for(size_t idx = 2; idx <= _data/2; ++idx)
        {
            if(0 == _data % idx)
            {
                return false;
            }
        }

        return true;
    }
private:
    size_t _data;
};

void test()
{
    vector<Number> numbers;
    for(size_t idx = 1; idx != 10; ++idx)
    {
        numbers.push_back(Number(idx));
    }
    
    std::for_each(numbers.begin(), numbers.end(), mem_fn(&Number::print));
    cout << endl;

    numbers.erase(remove_if(numbers.begin(), numbers.end(), mem_fn(&Number::isEven)), numbers.end());
    std::for_each(numbers.begin(), numbers.end(), mem_fn(&Number::print));
    cout << endl;

    numbers.erase(remove_if(numbers.begin(), numbers.end(), mem_fn(&Number::isPrime)), numbers.end());
    std::for_each(numbers.begin(), numbers.end(), mem_fn(&Number::print));
    cout << endl;
}
int main(int argc, char **argv)
{
    test();
    return 0;
}


```

2.function+bind

```c++
#include <math.h>
#include <iostream>
#include <functional>

using std::cout;
using std::endl;
using std::function;
using std::bind;

//基于对象
//使用std::function + std::bind取代继承 + 虚函数,体现多态
//灵活性高，使用起来比较简单

//具体类
class Figure
{
public:
    /* virtual */ 
    /* void display() const = 0; */

    /* virtual */ 
    /* double area() const = 0; */ 
    function<void()> _displayCallback;
    function<double()> _areaCallback;


    void setDisplayCallback(function<void()> &&cb)
    {
        _displayCallback = std::move(cb);
    }

    void setAreaCallback(function<double()> &&cb)
    {
        _areaCallback = std::move(cb);
    }

    void handleDispalyCallback() const
    {
        if(_displayCallback)
        {
            _displayCallback();
        }
    }

    double handleAreaCallback() const
    {
        if(_areaCallback)
        {
            return _areaCallback();
        }
        else
        {
            return 0;
        }
    }
};

void test(const Figure &fig)
{
    fig.handleDispalyCallback();
    cout << "'s area is : " << fig.handleAreaCallback() << endl;
}

class Rectangle
{
public:
    Rectangle(double length, double width)
    : _length(length)
    , _width(width)
    {

    }

    void display(int ix) const
    {
        cout << "Rectangle:";
    }

    double area() const
    {
        return _length * _width;
    }
private:
    double _length;
    double _width;
};

class Circle
{
public:
    Circle(double radis)
    : _radis(radis)
    {

    }

    void show() const
    {
        cout << "Circle :";
    }

    double getArea() const
    {
        return _radis * _radis * 3.1415;
    }
private:
    double _radis;
};

class Traingle
{
public:
    Traingle(double a, double b, double c)
    : _a(a)
    , _b(b)
    , _c(c)
    {

    }

    void print() const
    {
        cout << "Traingle: ";
    }

    //海伦公式
    double calcArea() const
    {
        double tmp = (_a + _b + _c)/2;

        return sqrt(tmp * (tmp - _a) * (tmp - _b) * (tmp - _c));
    }
private:
    double _a;
    double _b;
    double _c;
};

int main(int argc, char **argv)
{
    Rectangle rectangle(10, 20);
    Circle circle(10);
    Traingle traingle(3, 4, 5);

    Figure figure;
    figure.setDisplayCallback(bind(&Rectangle::display, &rectangle, 10));
    figure.setAreaCallback(bind(&Rectangle::area, &rectangle));
    test(figure);

    figure.setDisplayCallback(bind(&Circle::show, &circle));
    figure.setAreaCallback(bind(&Circle::getArea, &circle));
    test(figure);

    figure.setDisplayCallback(bind(&Traingle::print, &traingle));
    figure.setAreaCallback(bind(&Traingle::calcArea, &traingle));
    test(figure);

    return 0;
}


```


# c++学习笔记——11.string类实现以及写时复制

### 1.string类的实现

```c++
#include <string.h>
#include <iostream>
#include <vector>

using std::cout;
using std::endl;
using std::vector;

class String 
{
public:
    String()
    : _pstr(nullptr)
    {
        cout << "String()" << endl;
    }
    String(const char *pstr)
    : _pstr(new char[strlen(pstr) + 1]())
    {
        cout << "String(const char *)" << endl;
        strcpy(_pstr, pstr);
    }

    String(const String &rhs)
    : _pstr(new char[strlen(rhs._pstr) +1]())
    {
        cout << "String(const String &)" << endl;
        strcpy(_pstr, rhs._pstr);
    }

    ~String()
    {
        cout << "~String()" << endl;
        if(_pstr)
        {
            delete [] _pstr;
            _pstr = nullptr;
        }
    }

    String &operator=(const String &rhs)
    {
        cout << "String &operator=(const String &)" << endl;
        if(this != &rhs)
        {
            delete [] _pstr;
            _pstr = nullptr;
            _pstr = new char[strlen(rhs._pstr) + 1]();
            strcpy(_pstr, rhs._pstr);
        }
        return  *this;
    }

    // s1 = "hello";
    String &operator=(const char *pstr)
    {
        cout << "String &operator=(const char *)" << endl;
        String tmp(pstr);
        *this = tmp;

        return *this;
    }

    String &operator+=(const String &rhs)
    {
        cout << "String &operator+=(const String &)" <<endl;
        String tmp;
        tmp._pstr = new char[strlen(_pstr) + 1];
        strcpy(tmp._pstr, _pstr);
        delete [] _pstr;
        _pstr = nullptr;
        _pstr = new char[strlen(rhs._pstr) + strlen(tmp._pstr) + 1]();
        strcpy(_pstr, tmp._pstr);
        strcat(_pstr, rhs._pstr);

        return *this;
    }
    String &operator+=(const char *pstr)
    {
        cout << "String &operator+=(const char *)" << endl;
        String tmp(pstr);
        *this += tmp;

        return *this;
    }

    char &operator[](std::size_t index)//index > = 0
    {
        if(index < size())
        {
            return _pstr[index];
        }
        else
        {
            static char nullchar = '\0';
            return nullchar;
        }
    }

    const char &operator[](std::size_t index) const
    {
        if(index < size())
        {
            return _pstr[index];
        }
        else
        {
            static char nullchar = '\0';
            return nullchar;
        }

    }

    std::size_t size() const
    {
        return strlen(_pstr);
    }

    const char* c_str() const
    {
        return _pstr;
    }

    friend bool operator==(const String &, const String &);
    friend bool operator!=(const String &, const String &);

    friend bool operator<(const String &, const String &);
    friend bool operator>(const String &, const String &);
    friend bool operator<=(const String &, const String &);
    friend bool operator>=(const String &, const String &);

    friend std::ostream &operator<<(std::ostream &os, const String &s);
    friend std::istream &operator>>(std::istream &is, String &s);

private:
    char * _pstr;

};
bool operator==(const String &lhs, const String &rhs)
{
    return !strcmp(lhs._pstr, rhs._pstr);
}

bool operator!=(const String &lhs, const String &rhs)
{
    return strcmp(lhs._pstr, rhs._pstr);
}

bool operator<(const String &lhs, const String &rhs)
{
    return strcmp(lhs._pstr, rhs._pstr) < 0;
}

bool operator>(const String &lhs, const String &rhs)
{
    return strcmp(lhs._pstr, rhs._pstr) > 0;
}
bool operator<=(const String &lhs, const String &rhs)
{
    return strcmp(lhs._pstr, rhs._pstr) <= 0;
}
bool operator>=(const String &lhs, const String &rhs)
{
    return strcmp(lhs._pstr, rhs._pstr) >= 0;
}

std::ostream &operator<<(std::ostream &os, const String &rhs)
{
    if(rhs._pstr)
    {
        os << rhs._pstr;
    }

    return os;
}

std::istream &operator>>(std::istream &is, String &rhs)
{
    if(rhs._pstr)
    {
        delete [] rhs._pstr;
        rhs._pstr = nullptr;
    }
    vector<char> buffer;
    char ch;
    while((ch = is.get()) != '\n')
    {
        buffer.push_back(ch);
    }

    rhs._pstr = new char[buffer.size() + 1]();
    strncpy(rhs._pstr, &buffer[0], buffer.size());

    return is;
}

String operator+(const String &lhs, const String &rhs)
{
    cout << "String operator+(const String &, const String &)" << endl;

    String tmp(lhs);
    tmp += rhs;

    return tmp;
}
String operator+(const String &lhs, const char *pstr)
{
    cout << "String operator+(const String &, const char *)"<< endl;
    String tmp(lhs);
    tmp += pstr;

    return tmp;

}
String operator+(const char *pstr, const String &rhs)
{
    cout << "String operator+(const char*, const String &)" << endl;
    String tmp(pstr);
    tmp += rhs;

    return tmp;

}


void test()
{
    String s1;
    /* std::cin >> s1; */
    cout << "s1 = " << s1 << endl;

    cout << endl << endl;
    String s2 = "hello";
    cout << "s2 = " << s2 << endl;

    cout << endl << "1111" <<  endl;
    s2 = "world"; //error
    cout << "s2 = " << s2 << endl;

    cout << endl << endl;
    s2 = s2;
    cout << "s2 = " << s2 << endl;

    cout << endl << endl;
    String s3 = "wuhan";
    s3 += " welcome to string word";
    cout << "s3 = " << s3 << endl;

}
int main(int argc, char **argv)
{
    test();
    return 0;
}

```



### 2.string类的写时复制

```c++
#include <string.h>
#include <stdio.h>
#include <iostream>
using std::cout;
using std::cin;
using std::endl;
using std::ostream;

class String_COW
{
    public:
    class mychar;
    void reset_ref_count()
    {
        *(int*)(_pstr-4)=1;
    }
    void increase_ref_count()
    {
        ++*(int*)(_pstr-4);
    }
    void decrease_ref_count()
    {
        --*(int*)(_pstr-4);
    }
    int return_ref_count()
    {
        return *(int*)(_pstr-4);
    }
    String_COW()
    :_pstr(new char[5]()+4)
    {
        cout<<"String_COW()"<<endl;
        reset_ref_count();
    }
    String_COW(const char * p)
    :_pstr(new char[strlen(p)+1+4]()+4)
    {
        strcpy(_pstr,p);
        cout<<"String_COW(const char *p)"<<endl;
        reset_ref_count();
    }
    String_COW(const String_COW &str)
    :_pstr(str._pstr)//写时复制，先浅拷贝
    {
        cout<<"String_COW(const String_COW &str)"<<endl;
        increase_ref_count();
    }
    ~String_COW()
    {
        cout<<"~Stirng_COW()"<<endl;
        delete_pstr();
    }
    size_t size() const 
    {
        return strlen(_pstr);
    }
    const char * c_str() const
    {
        return _pstr;
    }
    void delete_pstr()
    {
        decrease_ref_count();
        if(0==return_ref_count())
        {
            delete [] (_pstr-4);
            cout<<"delete_pstr()"<<endl;
        }   
    }
    String_COW & operator=(const String_COW &str)
    {
        if(&str!=this)
        {
            delete_pstr();//赋值为另外一个串，先执行delete_pstr
            _pstr=str._pstr;//浅拷贝
            increase_ref_count();//引用计数+1
        }
        return *this;
    }
    
    mychar  operator[](size_t i)
    {
        if(i<strlen(_pstr))
        {
            mychar mc(*this,i);
            return mc;
        }else
        {
            String_COW nullstr("");
            mychar mcnull(nullstr,0);
            return mcnull; 
        }
    }
    class mychar
    {
        public:
        mychar(String_COW &str,size_t idx)
        :_str(str)
        ,_idx(idx)
        {
            // cout<<"mychar()"<<endl;
        }
        ~mychar()
        {
            // cout<<"~mychar()"<<endl;
        }
        mychar &operator=(const char &dch)//用来写:str[0]='H'
        {
            if((*this)._str.size()==0)//代表这个mychar是mcnull
            {
                return *this;
            }
            //先判断这个字符串的引用计数是否大于1
            if(_str.return_ref_count()>1)//大于1代表需要new空间
            {   
               char * pstrtemp=new char[_str.size()+1+4]()+4;
               strcpy(pstrtemp,_str._pstr);
               _str.decrease_ref_count();
               _str._pstr=pstrtemp;
               _str.reset_ref_count();
            }
            _str._pstr[_idx]=dch;
            return *this;
        }
        friend ostream &operator <<(ostream & os,mychar mc); 
        private:
        String_COW &_str;
        size_t _idx;
    };
    friend ostream &operator <<(ostream & os,mychar mc); 
    friend ostream &operator <<(ostream & os,const String_COW &str);
    friend ostream &operator <<(ostream & os,const char ch); 
    private:
    char * _pstr;//_pstr指向字符串开始的位置，前面4字节存储的是引用计数

};
ostream &operator <<(ostream & os,String_COW::mychar mc)//用来读单个字符
{
    const char ch=(mc._str.c_str())[mc._idx];
    os<<ch;
    return os;
} 
ostream &operator <<(ostream & os,const char ch)//用来读单个字符
{
    os<<ch;
    return os;
} 
ostream &operator <<(ostream & os,const String_COW &str)
{
    if(str._pstr)
    {
        os<<str._pstr;
    }
    return os;
}
void test()
{
    String_COW s1("hello");
    String_COW s2 = s1;
    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s1's refcount = " << s1.return_ref_count() << endl;
    cout << "s2's refcount = " << s2.return_ref_count() << endl;
    printf("s1's address: %p\n", s1.c_str());
    printf("s2's address: %p\n", s2.c_str());

    cout << endl;
    String_COW s3("world");
    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s3 = " << s3 << endl;
    cout << "s1's refcount = " << s1.return_ref_count() << endl;
    cout << "s2's refcount = " << s2.return_ref_count() << endl;
    cout << "s3's refcount = " << s3.return_ref_count() << endl;
    printf("s1's address: %p\n", s1.c_str());
    printf("s2's address: %p\n", s2.c_str());
    printf("s3's address: %p\n", s3.c_str());

    cout << endl << "执行赋值 s3 = s1 " << endl;
    s3 = s1;
    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s3 = " << s3 << endl;
    cout << "s1's refcount = " << s1.return_ref_count() << endl;
    cout << "s2's refcount = " << s2.return_ref_count() << endl;
    cout << "s3's refcount = " << s3.return_ref_count() << endl;
    printf("s1's address: %p\n", s1.c_str());
    printf("s2's address: %p\n", s2.c_str());
    printf("s3's address: %p\n", s3.c_str());

    cout << endl << "对s3[0]执行写操作 : " << endl;
    s3[0] = 'H';//s3.operator[](0)
    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s3 = " << s3 << endl;
    cout << "s1's refcount = " << s1.return_ref_count() << endl;
    cout << "s2's refcount = " << s2.return_ref_count() << endl;
    cout << "s3's refcount = " << s3.return_ref_count() << endl;
    printf("s1's address: %p\n", s1.c_str());
    printf("s2's address: %p\n", s2.c_str());
    printf("s3's address: %p\n", s3.c_str());

    cout << endl << "对s1[0]执行读操作 : " << endl;
    cout << "s1[0] = " << s1[0] << endl;
    cout << "s1 = " << s1 << endl;
    cout << "s2 = " << s2 << endl;
    cout << "s3 = " << s3 << endl;
    cout << "s1's refcount = " << s1.return_ref_count() << endl;
    cout << "s2's refcount = " << s2.return_ref_count() << endl;
    cout << "s3's refcount = " << s3.return_ref_count() << endl;
    printf("s1's address: %p\n", s1.c_str());
    printf("s2's address: %p\n", s2.c_str());
    printf("s3's address: %p\n", s3.c_str());
}
int main(int argc,char **argv)
{
    test();
   return 0;
}

```




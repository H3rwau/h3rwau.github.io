# c++学习笔记——20.STL、STL的线性容器vector,deque,list

1.STL

2.线性容器

1. vector

   ```c++
   class Point
   {
   public:
       Point(double dx = 0, double dy = 0)
       : _dx(dx)
       , _dy(dy)
       {
           cout << "Point(double = 0, double = 0)" << endl;
       }
       void print()  const
       {
           cout << "(" << _dx 
                << ", " << _dy 
                << ")" << endl;
       }
       ~Point()
       {
           cout << "~Point()" << endl;
       }
   private:
       double _dx;
       double _dy;
   };
   
   void test()//emplace_back和push_back的区别
   {
   // 在引入右值引用，转移构造函数，转移复制运算符之前，
   // 通常使用push_back()向容器中加入一个右值元素（临时对象）的时候
   // ，首先会调用构造函数构造这个临时对象，然后需要调用拷贝构造函数
   // 将这个临时对象放入容器中。原来的临时变量释放。这样造成的问题是
   // 临时变量申请的资源就浪费。
   // 引入了右值引用，转移构造函数后，push_back()右值时就会调用构造
   // 函数和转移构造函数。
   // 在这上面有进一步优化的空间就是使用emplace_back
   // 在容器尾部添加一个元素，这个元素原地构造，不需要触发拷贝构造和转移构造。
   // 而且调用形式更加简洁，直接根据参数初始化临时对象的成员。
       vector<Point> ps;
       ps.reserve(10);//初始就确定好vector的capacity，
                       //这样之后添加元素如果扩容，就不会有资源因为
                       //空间移动带来的销毁了
       ps.emplace_back(1,2);
       ps.emplace_back(3,4);
       // ps.push_back(Point(5,6));
       for(auto it=ps.begin();it!=ps.end();++it)
       {
           it->print();
       }
   }
   
   void test_vector()//vector的使用
   {
       cout<<"sizeof(vector<int>)="<<sizeof(vector<int>)<<endl;
       cout<<"sizeof(vector<string>)="<<sizeof(vector<string>)<<endl;
       //vector的大小在64位为24字节，三个指针的大小
       //vector有3个迭代器，分别指向目前使用空间的头和尾以及可用空间的尾
   
       //一、vector的初始化
       //1、使用数字进行初始化
       //vector<int> num(10,1);//保存10个1，如果只写1个参数，代表元素个数，默认0
       //2、使用迭代器范围初始化
       //int arr[10]={1,2,3,4,5,6,7,8,9};
       //vector<int> num(arr,arr+10);
       //3、使用大括号初始化
       vector<int> num={1,2,3,4,5,6,7,8,9};
   
       //二、vector的遍历
       //1、迭代器遍历
       vector<int>::const_iterator cit;
       //也可以使用auto cit=num.begin()
       for(cit=num.begin();cit!=num.end();++cit)
       {
           cout<<*cit<<" ";
       }
       cout<<endl;
       //2、auto和for结合使用，遍历容器
       // for(auto &e:num)
       // {
       //     cout<<e<<" ";
       // }
       // cout<<endl;
   
       print(num);
       //capacity在可用空间不够的情况下以2倍增长(gcc)
       cout<<"num.size()="<<num.size()<<endl;
       cout<<"num.capacity()="<<num.capacity()<<endl;
       
       //三、vector的插入和删除
       num.push_back(10);
       num.push_back(11);
       print(num);
       num.shrink_to_fit();//可以回收多余的可用空间，使size==capacity
       cout<<"num.size()="<<num.size()<<endl;
       cout<<"num.capacity()="<<num.capacity()<<endl;
   
       num.pop_back();//在容器尾部进行删除
       //获取vector元素的地址
       &num;//这个方法只是获取对象栈上的地址
       &num[0];
       &*num.begin();
       int *pd=num.data();//data()能够返回指向数据空间的指针
       cout<<"*pd="<<*pd<<endl;
       //vector不能在头部进行插入与删除，因为开销大，时间复杂度是O(N)
   
       //在中间插入
       //在中间插入的时候，迭代器可能会失效，如果再去操作可能出现错误
       //扩容的时候，迭代器指向的还是原来的位置，并不是新扩容的空间的对应位置
       //由于push_back每次只会插入一个，所以可以按照统一的形式2*size()
       //但是insert的时候，插入元素的个数是不定的
       //insert的扩容规则:
       //capacity()=n,size()=t   insert的时候，插入的元素个数为m
       // 1、m<n-t,这个时候没有扩容直接插入
       // 2、n-t<m<t,就按照t的2倍去进行扩容,新的空间就是2*t
       // 3、n-t<m<n且m>t，就按照t+m进行扩容
       // 4、m>n时，就按照t+m进行扩容
       cout<<endl<<"在vector中间插入"<<endl;
       print(num);
       auto it=num.begin();
       ++it;
       ++it;
       cout<<"*it="<<*it<<endl;
       num.insert(it,22);
       print(num);
       cout<<"*it="<<*it<<endl;//vector的insert之后的迭代器是根据
                               //指向的位置来的
       cout<<"num.size()="<<num.size()<<endl;
       cout<<"num.capacity()="<<num.capacity()<<endl;
   
       vector<int> vec{99,98,97,96,95,94,93,92};
       num.insert(it,vec.begin(),vec.end());
       print(num);
       cout<<"这个it失效了,*it="<<*it<<endl;//此时的it已经失效，因为扩容了
                               //指向的空间为原来的旧空间，没有所有权
                               //只能查看，随时会被其他数据覆盖
       // cout<<"下面这个操作是有问题的"<<endl;
       // num.insert(it,44);
       cout<<"num.size()="<<num.size()<<endl;
       cout<<"num.capacity()="<<num.capacity()<<endl;
       //此时还有3个可用空间
       auto it1=num.begin();
       it1+=2;
       cout<<"*it1="<<*it1<<endl;
       num.insert(it1,5,55);
       print(num);
       cout<<"这个it1失效了，*it1="<<*it1<<endl;//这里的it也已经失效了
       cout<<"num.size()="<<num.size()<<endl;
       cout<<"num.capacity()="<<num.capacity()<<endl;
   
       //四、vector支持下标运算
       cout<<endl<<endl;
       cout<<"num[0]="<<num[0]<<endl;
       cout<<"num[1]="<<num[1]<<endl;
   
       //五、vector的清空
       cout<<endl<<"清空容器中的元素"<<endl;
       num.clear();//清空容器中的元素，size变为0
       num.shrink_to_fit();//回收多余的空间
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
       cout<<"num.capacity()="<<num.capacity()<<endl;
   
   }
   ```

   

2. deque

   ```c++
   void test_deque()
   {
       cout<<"sizeof(deque<int>)="<<sizeof(deque<int>)<<endl;
       cout<<"sizeof(deque<string>)="<<sizeof(deque<string>)<<endl;
       //deque的大小在64位为80字节，十个指针的大小
       //deque有一个开始和结束迭代器，
       //每个分别有4个指针，cur、first、last、node
       //还有1个map指针，指向中控器(指针数组)
       //以及中控器指向第一个缓冲区的指针
   #if 1
       //一、deque的初始化
       //1、使用数字进行初始化
       //deque<int> num(10,1);//保存10个1，如果只写1个参数，代表元素个数，默认0
       //2、使用迭代器范围初始化
       //int arr[10]={1,2,3,4,5,6,7,8,9};
       //deque<int> num(arr,arr+10);
       //3、使用大括号初始化
       deque<int> num={1,2,3,4,5,6,7,8,9};
   
       //二、deque的遍历
       //1、迭代器遍历
       deque<int>::const_iterator cit;
       //也可以使用auto cit=num.begin()
       for(cit=num.begin();cit!=num.end();++cit)
       {
           cout<<*cit<<" ";
       }
       cout<<endl;
       //2、auto和for结合使用，遍历容器
       // for(auto &e:num)
       // {
       //     cout<<e<<" ";
       // }
       // cout<<endl;
   
       print(num);
       //deque没有capacity这个概念
       cout<<"num.size()="<<num.size()<<endl;
       
       //三、deque的插入和删除
       cout<<endl<<"在deque的尾部进行插入:"<<endl;
       num.push_back(10);
       num.push_back(11);
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
       num.pop_back();//在容器尾部进行删除
   
       cout<<endl<<"在deque的头部进行插入:"<<endl;
       num.push_front(20);
       num.push_front(21);
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
       num.pop_front();//在容器头部进行删除
       
       
       //获取deque元素的地址
       &num;//这个方法只是获取对象栈上的地址
       &num[0];
       &*num.begin();
   
   // 插入操作：
   // 1、在队前或队后插入元素时（push_back(),push_front()）,由于可能缓冲区的空间
   // 不够，需要增加map中控器，而中控器的个数也不够，所以新开辟更大的空间来容纳中控
   // 器，所以可能会使迭代器失效；但指针、引用仍有效，因为缓冲区已有的元素没有重新分
   // 配内存。
   // 2、在队列其他位置插入元素时，由于会造成缓冲区的一些元素的移动（源码中执行copy()
   // 来移动数据），所以肯定会造成迭代器的失效；并且指针、引用都会失效。
   
   // 删除操作：
   // 1、删除队头或队尾的元素时，由于只是对当前的元素进行操作，所以其他元素的迭代器不
   // 会受到影响，所以一定不会失效，而且指针和引用也都不会失效；
   // 2、删除其他位置的元素时，也会造成元素的移动，所以其他元素的迭代器、指针和引用都会失效。
   
       cout<<endl<<"在deque中间插入"<<endl;
       print(num);
       auto it=num.begin();
       ++it;
       ++it;
       cout<<"*it="<<*it<<endl;
       num.insert(it,22);
       print(num);
       cout<<"*it="<<*it<<endl;
       cout<<"num.size()="<<num.size()<<endl;
   
       deque<int> vec{99,98,97,96,95,94,93,92};
       num.insert(it,vec.begin(),vec.end());
       print(num);
       cout<<"*it="<<*it<<endl;
       cout<<"num.size()="<<num.size()<<endl;
   
       //四、deque支持下标运算
       cout<<endl<<endl;
       cout<<"num[0]="<<num[0]<<endl;
       cout<<"num[1]="<<num[1]<<endl;
   
       //五、deque的清空
       cout<<endl<<"清空容器中的元素"<<endl;
       num.clear();//清空容器中的元素，size变为0
       num.shrink_to_fit();//回收多余的空间
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
      #endif 
   }
   ```

   

3. list

   ```c++
   void test_list()
   {
       cout<<"sizeof(list<int>)="<<sizeof(list<int>)<<endl;
       cout<<"sizeof(list<string>)="<<sizeof(list<string>)<<endl;
       //list的大小为24字节，
   #if 1
       //一、list的初始化
       //1、使用数字进行初始化
       //list<int> num(10,1);//保存10个1，如果只写1个参数，代表元素个数，默认0
       //2、使用迭代器范围初始化
       //int arr[10]={1,2,3,4,5,6,7,8,9};
       //list<int> num(arr,arr+10);
       //3、使用大括号初始化
       list<int> num={1,2,3,4,5,6,7,8,9};
   
       //二、list的遍历
       //1、迭代器遍历
       list<int>::const_iterator cit;
       //也可以使用auto cit=num.begin()
       for(cit=num.begin();cit!=num.end();++cit)
       {
           cout<<*cit<<" ";
       }
       cout<<endl;
       //2、auto和for结合使用，遍历容器
       // for(auto &e:num)
       // {
       //     cout<<e<<" ";
       // }
       // cout<<endl;
   
       print(num);
       //list没有capacity这个概念
       cout<<"num.size()="<<num.size()<<endl;
       
       //三、list的插入和删除
       cout<<endl<<"在list的尾部进行插入:"<<endl;
       num.push_back(10);
       num.push_back(11);
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
       num.pop_back();//在容器尾部进行删除
   
       cout<<endl<<"在list的头部进行插入:"<<endl;
       num.push_front(20);
       num.push_front(21);
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
       num.pop_front();//在容器头部进行删除
       
       
   // list增加任何元素都不会使迭代器失效。删除元素时，
   // 除了指向当前被删除元素的迭代器外，其它迭代器都不会失效
       cout<<endl<<"在list中间插入"<<endl;
       print(num);
       auto it=num.begin();
       ++it;
       ++it;
       cout<<"*it="<<*it<<endl;
       num.insert(it,22);
       print(num);
       cout<<"*it="<<*it<<endl;
       cout<<"num.size()="<<num.size()<<endl;
   
       list<int> vec{99,98,97,96,95,94,93,92};
       num.insert(it,vec.begin(),vec.end());
       print(num);
       cout<<"*it="<<*it<<endl;
       cout<<"num.size()="<<num.size()<<endl;
   
       //四、list不支持下标运算
       cout<<endl<<endl;
       // cout<<"num[0]="<<num[0]<<endl;
       // cout<<"num[1]="<<num[1]<<endl;
   
       //五、list的清空
       cout<<endl<<"清空容器中的元素"<<endl;
       num.clear();//清空容器中的元素，size变为0
       print(num);
       cout<<"num.size()="<<num.size()<<endl;
      #endif 
   
   }
   void test_list_operation()
   {
       list<int> num{8, 3, 4, 3, 6, 7, 6, 9, 1, 8, 9};
       print(num);
       num.unique();
       print(num);
   
       cout << endl << ">>>test sort ..." << endl;
       num.sort();//默认情况是以小于符号进行排序
       print(num);
       /* num.sort(std::less<int>()); */
       /* print(num); */
       /* num.sort(std::greater<int>()); */
       /* print(num); */
       num.unique();//unique在去除重复元素的时候，链表必须为有序
       print(num);
   
       //
       cout << endl << ">>>test merge..." << endl;
       list<int> num2{11, 22, 33};
       num.merge(num2);
       print(num);
       print(num2);//原来的num2就没有了
   
       cout << endl << ">>>test reverse..." << endl;
       num.reverse();//逆置链表
       print(num);
   
       cout << endl << ">>>test splice..." << endl;
       list<int> num3{41, 42, 43, 44, 45, 46, 47};
       auto it = num.begin();
       ++it;
       ++it;
       //  num.splice(it, num3); //将num3拼接到it(num的迭代器)指向的位置
       //  print(num); 
   #if 1
       auto it2 = num3.begin();
       ++it2;
       ++it2;
       num.splice(it, num3, it2);//将num3的it2指向的元素拼接到it指向的位置
       print(num);
       print(num3);//num3的it2元素没有了
   
       auto it3 = num.end();
       it = num.begin();
       --it3;
       num.splice(it, num, it3);//将本链表的某个元素拼接到某个迭代器指向的元素之前
       print(num);
   #endif
   }
   ```

   
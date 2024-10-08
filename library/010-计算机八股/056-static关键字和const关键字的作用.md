## 参考答案

`static`和`const`是`C++` 中两个常用的关键字, 有以下作用：

1. `static` 关键字: 用于控制变量和函数的生命周期、作用域和访问权限。
   - 声明静态变量：静态变量的**生命周期直到程序结束**。当在函数内部声明静态变量时，即使函数执行完了也不会释放它，下次调用该函数时会保留上次的状态。
   - 在类中，被static声明的成员被称为静态成员。
     - 静态成员变量：在类中使用static关键字修饰的成员变量，表示该变量属于类而不是类的实例，所有实例共享同一份数据
     - 静态成员函数：在类内使用static关键字修饰的成员函数，**所有对象共享同一个函数**；**静态成员函数只能访问静态成员变量**；**静态成员函数调用可以不需要通过创建类的实例，而是直接通过类名调用**。
   - `static`变量如果被多个线程访问，需要特别注意线程安全问题。
2. `const`: 关键字用于定义常量，即**一旦初始化后其值不能被修改**：
   - 常量变量：声明变量，使变量的值不能修改（只读）
   - 常量成员函数，表示该函数不会修改对象的成员变量
   - 常量指针：可以指向一个 `const` 类型的值，或者是一个指向 `const` 值的指针，表明指针指向的值不能通过这个指针被修改。
   - `const`变量由于其不可变性，天然具有线程安全性。
3. 有时候`static`和`const` 可以组合使用，如`static const`变量，表示一个静态的常量。

总结来说，`static`关键字用于创建类的静态成员，而`const` 关键字用于定义常量。

## 背诵版：

1. `static` 关键字: 用于**控制变量和函数的生命周期、作用域和访问权限**。
   - 声明静态变量：静态变量的**生命周期直到程序结束**。当在函数内部声明静态变量时，即使函数执行完了也不会释放它，下次调用该函数时会保留上次的状态。
   - 在类中，被**static声明的成员被称为静态成员**。
     - **静态成员变量**：在类中使用static关键字修饰的**成员变量**，表示该**变量属于类**而不是类的实例，所有实例共享同一份数据
     - **静态成员函数**：在类内使用static关键字修饰的**成员函数**，**所有对象共享同一个函数**；**静态成员函数只能访问静态成员变量**；**静态成员函数调用可以不需要通过创建类的实例，而是直接通过类名调用**。
   - `static`变量如果被多个线程访问，需要特别**注意线程安全问题**。
2. `const`: 关键字用于定义常量，即**一旦初始化后其值不能被修改**：
   - **常量变量**：声明变量，**使变量的值不能修改（只读）**
   - 常量成员函数，表示**该函数不会修改对象的成员变量**
   - **常量指针**：可以指向一个 `const` 类型的值，或者是一个指向 `const` 值的指针，表明指针指向的值不能通过这个指针被修改。
   - `const`变量由于其不可变性，天然具有线程安全性。
3. 有时候`static`和`const` 可以组合使用，如`static const`变量，表示一个静态的常量。

总结来说，`static`关键字用于**创建类的静态成员**，而`const` 关键字**用于定义常量**。
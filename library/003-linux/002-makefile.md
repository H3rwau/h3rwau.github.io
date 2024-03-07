## Makefile

执行模式:增量编译

规则:目标文件 依赖文件命令

伪目标

变量

通配符 模式匹配

内置函数

循环结构

编译:预处理+编译+汇编

每个.c文件形成一个.o文件

makefile建立目标与依赖之间的关系，根据修改时间来决定命令是否执行

规则

目标:依赖文件

[tab] 命令



make 目标名 伪目标：这个目标是文件

变量（起别名） 字符串替换

A=b 运行时替换

A:=b 定义时替换

out:=main 其他地方写$(out)

$(A)自定义变量



自动变量：

$@ 目标文件

$< 第一个依赖文件

$^ 所有依赖文件

$? 新文件(修改比较晚)

$(@D) 目标文件的目录部分

$(@F) 目标文件的文件名部分



内置函数

wildcard 对文件系统使用通配符

patsubst (pattern ,replacement, text)将text的内容按模式进行替换

```makefile
CC := gcc
out := main.exe
srcs := $(wildcard *.c)
objs := $(srcs:%.c=%.o)
objs := $(patsubst %.c,%.o,$(srcs))
$(out):$(objs)
	$(CC) $^ -o $@
%.o: %.c
	$(CC) -c $^ -o $@
.PHONY:clean rebuild
rebuild:clean $(out)
clean:
	rm -rf $(objs) $(out)
```

%在规则的目标中，自动匹配上一个规则的依赖项

内置函数



命令`g++ -DDEBUG test.o main.o bitruss.o temporal_bipartite_graph.o beindex.o time.o -o main`是链接命令，它用于将多个对象文件（`.o`文件）链接为一个可执行文件。当你在这个阶段使用`-DDEBUG`时，它不会影响到链接的对象文件，因为这些文件在之前的编译阶段已经被编译成机器代码了，宏定义的添加应该发生在源代码编译阶段。

另一方面，当你使用`gcc -DDEBUG *.c -o main`时，这是一个编译加链接的命令，它会首先处理`*.c`文件，这个过程中会考虑`-DDEBUG`宏定义，然后将得到的对象文件链接成可执行文件。在这个步骤中，`-DDEBUG`有效地添加了宏定义，因为它是在源代码被编译为对象代码之前。

如果你想要在使用`g++`进行单独的编译步骤时添加宏定义，你应该在编译每个源文件（而不是链接对象文件）时添加`-DDEBUG`选项，例如：

```bash
g++ -DDEBUG -c test.c -o test.o
g++ -DDEBUG -c main.c -o main.o
# ... 对其他源文件执行相同的操作 ...
```

这样在编译时`DEBUG`宏就会被定义，然后你可以链接这些对象文件创建最终的可执行文件：

```bash
g++ test.o main.o bitruss.o temporal_bipartite_graph.o beindex.o time.o -o main
```

请确保在编译步骤中为所有需要的源文件添加`-DDEBUG`选项。


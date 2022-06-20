Makefile

执行模式:增量编译

规则:目标文件 依赖文件命令

伪目标

变量

通配符模式匹配

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
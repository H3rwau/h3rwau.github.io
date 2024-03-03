sudo apt install ssh 安装ssh

ps -elf|grep sshd 查看ssh是否运行



kernel(内核) 1.硬件(进程(cpu)，内存(内存管理),文件(磁盘)) 

2.环境(系统调用)

3.shell 命令解释器

4.library routines 公共函数库

5.应用程序



## linux初步使用

cat /etc/passwd 查看用户

uname -a 查看自己操作系统的内核版本

cat /etc/issue 查看发行版的版本

sudo可以临时提高权限

passwd 给用户配置口令

su [其他用户]    切换用户(不加用户名就是切换到root用户)

普通用户的命令提示符是$

cat /etc/group 查看组

exit 退出用户

useradd 添加用户 -m [用户名] (创建家目录) -s /bin/bash(指定shell,默认是sh）

设计理念：没有消息就是最好的消息

userdel -r [用户名] 删除用户

history 查看命令历史

Ubuntu的安全设计：使用ssh登录的时候，只能通过普通用户登录 ssh=secure shell   , telnet ,tftp 不安全，口令传输的时候无加密

## 关于git

sudo apt-get isntall git 安装git客户端

配置姓名和邮箱地址

git config --global user.name 姓名

git config --global user.email 邮箱



git clone repo地址

git pull origin master

git add .

git commit -m "[提交信息]"

git push origin master



## 文件系统(VFS)

linux是单根目录结构(树)

pwd 当前工作目录

目录文件是非叶子节点，普通文件是叶子节点



/bin 存放了可执行程序(各种命令)

/etc 存放了一些配置文件

/home 存放了家目录

/proc 进程信息





cd 改变目录

cd .. 回到父目录

cd 或者 cd ~  回到家目录

cd - 回到上一次的目录

mkdir 创建目录

rmdir 删除目录 只能删除空目录

cp 复制 mv剪切 删除rm

ls 显示当前工作目录的文件 -a显示隐藏文件 -l显示详细信息

drwxrwxr-x

文件类型 d目录 -普通文件 c字符设备文件(IO以字节为单位,键盘鼠标) b块设备文件(IO以块为单位，磁盘) l软链接(快捷方式，存储了路径)

用户权限，组权限，其他用户权限 r读w写x执行  

ls --help 可以接什么参数



树状目录显示

sudo apt install tree

tree 显示当前路径的树状目录

tree [路径] -h 显示文件大小





man [命令] 可以查看命令的帮助手册

修改文件权限 chmod 

**文字设定法**： chmod [who]  [+ | - |=]  [mode] 文件名(可以重复多次用逗号分隔)

who:u用户g组o其他a所有 mode:r w x

例子:

chmod +r file1 给这个文件所有用户加r权限

chmod ug+r file1 给这个文件用户和组用户加r权限

chmod a=wx file1 将这个文件所有用户设置为wx的权限

**数字设定法**:chmod 8进制数 文件名

umask 查看权限掩码 后加可修改掩码 修改生效在本次登陆



文件的查找：

find [起始目录] [查找条件] [操作] （递归查找） 必须要有目录的读权限

命令的查找条件可以是一个逻辑运算符not,and,or组成的复合条件

**-a（逻辑与） -o（逻辑或）!（逻辑非）**

**通配符的使用（只是用来匹配文件名的）：**

*(0~任意多个字符)   dir\* 代表以dir开头的文件

? (1个任意字符)

[] 括号里是范围内字符 [0-9] [A-Za-z]

常用的查找条件有：

（1）根据名称和文件属性查找

​		-name 名字

​		-gid 属于用户组Id

​		-uid 属于用户id

​		-group 属于用户组名

​		-user 属于用户名

​		-empty 查找大小为0

​		-perm 指定权限 接666 664

​		-size  n[bckw] 大小

​		-type [bcdpfls] 类型

（2）按时间查找

​		-**a**min 查找n分钟以前**被访问过**的所有文件

​		-**c**min 查找n分钟以前**文件状态被修改**过的所有文件

​		-**m**min 查找n分钟以前**文件内容被修改**过的所有文件

​		-atime 查找n天以前被访问过的所有文件

​		-ctime 查找n天以前文件状态被修改过的所有文件



find命令和exec 组合执行后续操作

fInd命令  -exec [命令]  {} \；find命令的结果的每一行作为参数传入命令1，{}代表find结果的每一行



### **管道**

ps -elf |grep sshd  (grep筛选内容)

**xargs 将管道的内容拆成一行行的单词**

find . -name "file" | xargs ls-l

统计当前目录有多少文件 ls|wc -l



磁盘的相关命令

man -k disk 查询磁盘的相关命令

df  文件系统的使用情况(字节显示)

df- h 显示整个磁盘详细使用情况

du  -h 当前目录占多少大小  --max-depth=0 深度调整



文件查看和处理

cat 文件  -b对非空行编号 -E对每行结束加$（显示换行） -n对每行编号 -s将连续空行合并显示

file 查看文件类型

sort 每一行按字典序排

uniq 将相连的重复的不显示

sort file |uniq

 sudo cat /etc/shadow 查看密码

SHA512加密    \$[salt值]\$  

使用salt值加上明文利用SHA512算法转换成密文

数据库存储 盐值和密文 ，用户提供明文，通过算法转换成的密文和旧密文比较。

文件数字统计

wc 会显示行单词字节 -l,-w,-c



### **标准输入输出**

描述符0，1,2分别表示标准输入，标准输出，错误输出

可以利用描述符重定向

echo [内容] 将内容显示在屏幕上 -n 去掉换行

echo [内容] \> file1 将内容重定向到内容

echo -n >file ，touch file,vim file和 cat >file 然后ctrl+D 这几种方法都可以创建新文件

\> 重定向标准输出 \>>将结果追加尾部

<重定向标准输入 2>重定向标准错误

&>将标准输出和错误同时输出

假设a.out有标准输出和错误输出

./a.out >file1  这样标准输出到了file1里面，错误输出显示屏幕

./a.out 2>file1  这样标准输出显示在屏幕，错误输出到了file1里面

./a.out &>file1  这样标准输出显示和错误输出都到了file1里面

./a.out <file1 也可以将file1里的内容作为输入到a.out的标准输入



部分显示：

head -n [文件名] 显示文件的前n行，默认前十行

tail -n [文件名] 显示文件的后n行，默认后十行

单页显示：

more [文件]  显示文件,bf控制，q退出,h显示帮助  （less差不多）



alias 查看别名

gb2312 gbk编码 utf-8 utf编码

iconv -f [原来] -t [目标] [文件名] 显示目标文件转换编码方式的内容。



分号;可以让命令依次执行，一次输入多个命令

cmd1;cmd2 先执行cmd1再执行cmd2



管道 cmd1|cmd2 将cmd1的输出作为cmd2的输入



**grep** 指定一个格式，将文件中会符合格式的行打印出来（按文件内容进行查找）

grep [选项]  [查找模式] [文件名1，文件名2......]

选项：

**-F 忽略控制字符，每个模式作为固定的字符串对待,可以不加\\**

**-c 只显示匹配行的数量**

**-i 比较不区分大小写**

**-n在输出前加上匹配串所在的行号**

**-E参数可以扩展选项为正则表达式**

\加转义字符 变成 普通字符  

**正则表达式：字符串的生成规则**

g(a|e) y  gay或者gey

·匹配任意一个字符  相当于通配符的?

[a-z]匹配a-z任一字符

[基本单位?]   基本单位出现0或1次

[^基本单位]，基本单位出现在行首

[基本单位$]，基本单位出现在行尾

[基本单位*],  基本单位出现0~多次 +：1~多次 {x,y} x~y次

.* 可以匹配任意字符

grep -E  "gr(a|e)y" file

### grep和find同时使用

find . -name "*.[ch]" |**xargs** grep -nE "main"



命令替换

cmd1 \`cmd2`  将cmd2的结果作为参数传入到了cmd1中

 $(cmd2)符号也可作命令替换



### 打包和压缩

tar [主选项+辅助选项]  目标文档 源文件/目录

主选项:c创建 r追加 x释放

辅助选项:f使用包文件 v显示处理文件 z用gzip压缩文件



创建cfv 追加cfv 释放xfv

打包会先分配一个较大的文件

压缩包 cfvz  解压缩 xfvz





### scp命令

用作上传/下载

scp -r [源路径] [目标路径]

**远程主机的路径：用户名@ip地址:路径名**





### 密钥管理

公钥 id_rsa.pub  私钥 id_rsa



我们可以讲公钥放到云端服务器

cd ~/.ssh

ssh-keygen 生成公钥和私钥



cat id_rsa.pub >> .ssh/authorized_keys





编译工具gcc

源代码.c+头文件.h   -----预处理-----   编译.s -------- 汇编.o -------链接-----可执行程序

预处理 gcc -E 源文件 -o 目标文件.i

编译 gcc -s 源文件 -o 目标文件.s

-c 自动生成目标文件.o 仅执行编译，不进行链接





rbp base pointer

rsp stack pointer



as 汇编文件 -o 目标文件(二进制文件)

nm 目标文件 (查看符号表)



-I 目录名 指定头文件的目录

-D 宏名 相当于在代码头部添加了一个 #define 宏 设置一个开关，一份代码多份版本



库

静态库 静态链接的时候，把库文件打包到程序卡里面 ，容易部署 难以升级体积大

1. gcc -c add.c 得到add.o
2. 打包 ar crsv libadd.a add.o
3. sudo cp libadd.a /usr/lib 将库文件放在库目录
4. gcc -o main main.c -ladd 编译时加入库名

动态库 链接的时候，得库文件的位置，在运行时再加载到内存，难以部署，容易升级，体积小,dll

 	1. gcc -c add.c -fpic 得到add.o
 	2. gcc -shared -o libadd.so add.o
 	3. sudo cp libadd.so /usr/lib
 	4. gcc -o main main.c -ladd\

ldd 查看依赖的动态库

版本更新 libadd.so 符号链接(软链接)

1. 删除原软链接
2. 重新建立链接 ln -s

sudo ln -s libadd.so.0.0.0 libadd.so


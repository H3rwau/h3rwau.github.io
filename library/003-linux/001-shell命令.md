cat /etc/passwd 查看用户

uname -a 查看自己操作系统的内核版本

cat /etc/issue 查看发行版的版本

sudo可以临时提高权限

passwd 给用户配置口令

su 切换用户

cat /etc/group 查看组

exit 退出用户

useradd 添加用户 -m 用户名(创建家目录) -s /bin/bash(指定shell,默认是sh）

userdel -r 用户名 删除用户

history 查看命令历史



关于git

sudo apt-get isntall git 安装git客户端

配置姓名和邮箱地址

git config --global user.name 姓名

git config --global user.email 邮箱



git clone repo地址

git pull origin master

git add

git commit -m "  "

git push origin master







linux是单根目录结构

pwd 当前工作目录

ls 显示当前工作目录的文件 -a显示隐藏文件 -l显示详细信息

mkdir 创建目录

rmdir 删除目录

cp 复制 mv剪切 删除rm

修改文件权限 chmod 

文字设定法： chmod [who]  [+ | - |=]  [mode] 文件名

who:u用户g组o其他a所有 mode:r w x

数字设定法:chmod 8进制数 文件名

umask 查看权限掩码 后加可修改掩码 修改生效在本次登陆



文件的查找：

find 起始目录 查找条件 操作 （递归查找） 必须要有目录的读权限

命令的查找条件可以是一个逻辑运算符not,and,or组成的复合条件

-a（逻辑与） -o（逻辑或）!（逻辑非）

通配符的使用：

*(0~任意多个字符)

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

​		-perm 指定权限

​		-size 大小

​		-type 类型

（2）按时间查找

​		-amin 查找n分钟以前被访问过的所有文件

​		-cmin 查找n分钟以前文件状态被修改过的所有文件

​		-mmin 查找n分钟以前文件内容被修改过的所有文件

​		-atime 查找n天以前被访问过的所有文件

​		-ctime 查找n天以前文件状态被修改过的所有文件



find命令和exec 组合执行后续操作

fInd命令  -exec 命令1 ｛｝\；find命令的结果的每一行作为参数传入命令1



管道

ps -elf |grep sshd  (grep筛选内容)

xargs 将管道的内容拆成一行行的单词

统计当前目录有多少文件 ls|wc -l



磁盘的相关命令

man -k disk 查询磁盘的相关命令

df 

df- h 显示整个磁盘使用情况

du-h 当前目录占多少大小



文件查看和处理

cat 文件  -b对非空行编号 -E对每行结束加$ -n对每行编号 -s合并空行

file 查看文件类型

sort 每一行按字典序排

uniq 将相连的重复的不显示



文件数字统计

wc 会显示行单词字节 -l,-w,-c



alias 查看别名

cmd1;cmd2 先执行cmd1再执行cmd2

管道 cmd1|cmd2 将cmd1的输入作为cmd2的输出



grep 指定一个格式，将文件中会符合格式的行打印出来

grep [选项]  [查找模式] [文件名1，文件名2。。。。。。。]

-F 每个模式作为固定的字符串对待

-c 只显示匹配行的数量

-i 比较不区分大小写

-n在输出前加上匹配串所在的行号

-E参数可以扩展选项为正则表达式

(a|e)   ·匹配任意一个字符 [a-z]匹配a-z任一字符

基本单位? 基本单位出现0或1次

^基本单位，基本单位出现在行首

基本单位$，基本单位出现在行尾

基本单位*,基本单位出现0~多次 +：1~多次 {x,y} x~y次



grep和find同时使用

find . -name "*.[ch]" |xargs grep -nE "main"

命令替换

cmd1 \`cmd2`  将cmd2的结果作为参数传入到了cmd1中

 $(cmd2)符号也可作命令替换



打包和压缩

tar [主选项+辅助选项]  目标文档 源文件/目录

主选项:c创建 r追加 x释放

辅助选项:f使用包文件 v显示处理文件 z用gzip压缩文件



创建cfv 追加cfv 释放xfv

打包会先分配一个较大的文件

压缩包 cfvz 解压缩 xfvz





scp命令

上传/下载

scp -r 源路径 目标路径

远程主机的路径：用户名@ip地址:路径名





ssh-keygen 生成公钥

cd ~/.ssh

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


## 参考答案

- **AOF 日志**：每执行一条写操作命令，就把**该命令以追加的方式写入到一个文件**里；
- **RDB 快照**：将某一时刻的内存数据，以二进制的方式生成一个dump.rdb文件写入磁盘，但是rdb方式是通过在指定的时间间隔内，执行指定次数的写操作或者是通过其他命令来触发，**不能确保数据的完整性和一致性**；
- **混合持久化方式**：Redis 4.0 新增的方式，集成了 AOF 和 RBD 的优点；
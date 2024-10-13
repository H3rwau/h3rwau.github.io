根据数据量大的情况：

按需查询字段,也能减少网络IO消耗

不要使用select *，减少Mysql优化器负担

查询的字段尽量保证索引覆盖

借助Redis等nosql缓存数据缓解Mysql的压力

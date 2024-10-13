## 参考答案

使用函数setsocketopt可以调整套接字的属性  

SO_RCVBUF和SO_SNDBUF：用来获取和调整接收/发送缓冲区的大小。注意到
setsockopt之后再getsockopt的结果会和之前传入的参数不一致。  

SO_RCVLOWAT和SO_SNDLOWAT：这个参数说明**一个缓冲区的下限**，如果缓冲区的字节少于下限，那么数据就不会从套接字中传递给内核协议栈或者发送给用户。这样修改了之后，**发送方的数据量如果比较少**，将不会触发epoll_wait的读就绪    

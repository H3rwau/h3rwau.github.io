## 参考答案：

`HTTPS` 主要基于`SSL/TLS` 协议，**确保了数据传输的安全性和完整性, 其建立连接并传输数据的过程如下：**

1. **密钥交换**：客户端发起HTTPS请求后，**服务器会发送其公钥证书给客户端**。
2. **证书验证**：客户端**会验证服务器的证书是否由受信任的证书颁发机构（`CA` ）签发**，并检查证书的有效性。
3. **加密通信**：一旦证书验证通过，**客户端会生成一个随机的对称加密密钥**，**并使用服务器的公钥加密这个密钥，然后发送给服务器。**
4. **建立安全连接**：服务器**使用自己的私钥解密得到对称加密密钥**，此时客户端和服务器都有了相同的密钥，可以进行加密和解密操作。
5. **数据传输**：使用**对称加密密钥对所有传输的数据进行加密，确保数据在传输过程中的安全性**。
6. **完整性校验**：SSL/TLS协议还包括**消息完整性校验机制**，如**消息认证码，确保数据在传输过程中未被篡改**。
7. **结束连接**：数据传输完成后，**通信双方会进行会话密钥的销毁**，以确保不会留下安全隐患。


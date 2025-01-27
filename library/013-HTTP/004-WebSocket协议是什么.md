从http协议的角度来看，就是点一下网页的某个按钮，前端发一次HTTP请求，网站返回一次HTTP响应。这种都是由客户端主动请求，服务器响应的方式也满足大部分网页的功能场景。

那服务器主动发消息给客户端的场景呢？

其实问题的痛点在于，**怎么样才能在用户不做任何操作的情况下，网页能收到消息并发生变更。**

最常见的解决方案是，**网页的前端代码里不断定时发 HTTP 请求到服务器，服务器收到请求后给客户端响应消息。**
这其实时一种**「伪」**服务器推的形式。

它其实并不是服务器主动发消息到客户端，而是客户端自己不断偷偷请求服务器，只是用户无感知而已

用这种方式的场景也有很多，最常见的就是**扫码登录**，
比如，某信公众号平台，登录页面二维码出现之后，前端网页根本不知道用户扫没扫，于是不断去向后端服务器询问，看有没有人扫过这个码。而且是以大概1到2秒的间隔去不断发出请求，这样可以保证用户在扫码后能在1到 2秒内得到及时的反馈，不至于等太久。

### 使用**HTTP定时轮询**

但这样，会有两个比较明显的问题
当你打开 F12 页面时，你会发现满屏的 HTTP 请求。虽然很小，但这其实也**消耗带宽**，同时也会**增加下游服务器**的负担。

最坏情况下，用户在扫码后，需要等个 1~2 秒，正好才触发下一次 HTTP 请求，然后才跳转页面，用户会感到**明显的卡顿**。
使用起来的体验就是，二维码出现后，手机扫一扫，然后在手机上点个确认，这时候卡顿等个 1~2 秒页面才跳转。

### 长轮询

我们知道，HTTP 请求发出后，，一般会给服务器留一定的时间做响应，比如3秒，规定时间内没返回就认为是超时。

如果我们的 HTTP 请求将**超时设置的很大**，比如 30 秒，**在这 30 秒内只要服务器收到了扫码请求，就立马返回给客户端网页。如果超时，那就立马发起下一次请求。**
这样就**减少了 HTTP 请求的个数**，并且由于大部分情况下，用户都会在某个 30 秒的区间内做扫码操作，所以响应也是及时的。

![image-20240927205905164](D:\笔记gitpage\h3rwau.github.io\library\010-计算机八股\八股.assets\image-20240927205905164.png)

像这种发起一个请求，在较长时间内等待服务器响应的机制，就是所谓的长轮询机制。常用的消息队列RocketMQ中，消费者去取数据时，也用到了这种方式。

## WebSocket是什么

我们知道 TCP 连接的两端，**同一时间里**，**双方**都可以**主动**向对方发送数据。这就是所谓的全双工也是基于TCP协议的，同一时间里，客户端和服务器只能有一方主动

而现在使用最广泛的 HTTP/1.1发数据，同一时间里客户端和服务器只有一方主动发数据，这就是所谓的半双工

也就是说，好好的全双工 TCP，被 HTTP/1.1 用成了半双工。
为什么?
这是由于 HTTP 协议设计之初，考虑的是看看网页文本的场景，能能做到客户端发起请求再由服务器响应，就够了，根本就没考虑网页游戏这种，客户端和服务器之间都要互相主动发大量数据的场景。

所以，为了更好的支持这样的场景，我们需要另外一个基于TCP的新协议。于是新的**应用层协议Websocket**就被设计出来了大家别被这个名字给带偏了。虽然名字带了个socket，但其实 socket 和 Websocket 之间，!就跟雷峰和雷峰塔一样，二者接近毫无关系。

怎么建立WebSocket连接

我们平时刷网页，一般都是在览器上刷的，一会刷刷图文，这时候用的是 HTTP 协议，一会打开网页游戏，这时候就得切换成我们新介绍的 Websocket 协议。

为了兼容这些使用场景。浏览器在 TCP 三次握手建立连接之后，都统一使用 HTTP 协议先进行一次通信。
如果此时是普通的 HTTP 请求，那后续双方就还是老样子继续用普通 HTTP 协议进行交互，这点没啥疑问。

如果这时候是想建立 WebSocket 连接，就会在 HTTP 请求里带上一些特殊的header 头，如下:

```web-idl
Connection: upgrade
Upgrade: WebSocket
Sec-Websocket-key:T2a6wZlAwhgQNgruz2YUyg==\r\n
```

这些 header 头的意思是，浏览器想升级协议(Connection: Upgrade)，并且想升级成 WebSocket 协议(Upgrade: WebSocket)。同时带上一段随机生成的 base64码(Sec-WebSocket-Key)，发给服务甜。

如果服务器正好支持升级成 WebSocket 协议。就会走 WebSocket 握手流程，同时根据客户端生成的base64 码，用某个**公开**的算法变成另一段字符串，放在 HTTP响应的 sec-websocket-Accept 头里，同时带上 101状态码 ，发回给浏览器。HTTP 的响应如下:

```c
HTTP/1.1 101 Switching Protocols\r\nSec-Websocket-Accept:iBJKv/ALIW2DobfoA4dmr3JHBCY=lrinUpgrade: websocketlrin
Connection:upgradelr\n
```

这个101表示**协议切换**

## WebSocket的使用场景

它适用于需要服务器和客户端（浏览器）频繁交互的大部分场景，比如网页/小程序游戏，网页聊天室，以及一些类似飞书这样的网页协同办公软件。
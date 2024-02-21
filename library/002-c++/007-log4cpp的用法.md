# c++学习笔记——7.log4cpp的用法

### 1.log4cpp

```c++
#include <log4cpp/SimpleLayout.hh>
#include <log4cpp/BasicLayout.hh>
#include <log4cpp/PatternLayout.hh>
#include <log4cpp/OstreamAppender.hh>
#include <log4cpp/FileAppender.hh>
#include <log4cpp/RollingFileAppender.hh>
#include <log4cpp/Category.hh>
#include <log4cpp/Priority.hh>
#include <iostream>

using std::cout;
using std::endl;

using namespace log4cpp;//一次性把log4cpp里面的实体全部引出来

void test()
{
    //日志的格式
    SimpleLayout *psl = new SimpleLayout();

    //日志的目的地
    OstreamAppender *poa = new OstreamAppender("OstreamAppender", &cout);
    poa->setLayout(psl);

    //日志种类
    Category &root = Category::getRoot();
    root.setAppender(poa);
    /* root.setPriority(Priority::DEBUG); */
    root.setPriority(Priority::ERROR);

    //日志记录器：只有当日志的优先级大于等于Category的优先级的时候，日志
    //才会被记录，否则日志就会被过滤掉

    root.emerg("This is an emerg message");
    root.fatal("This is an fatal message");
    root.alert("This is an alert message");
    root.crit("This is an crit message");
    root.error("This is an error message");
    root.warn("This is an warn message");
    root.notice("This is an notice message");
    root.info("This is an info message");
    root.debug("This is an debug message");

    //回收
    Category::shutdown();
}

void test1()
{
    //日志的格式
    /* SimpleLayout *psl = new SimpleLayout(); */
    /* BasicLayout *pbl = new BasicLayout(); */
    PatternLayout *ppl = new PatternLayout();
    ppl->setConversionPattern("%d %c [%p] %m%n");

    //日志的目的地
    OstreamAppender *poa = new OstreamAppender("OstreamAppender", &cout);
    /* poa->setLayout(psl); */
    /* poa->setLayout(pbl); */
    poa->setLayout(ppl);

    //日志种类
    /* Category &root = Category::getRoot(); */
    Category &root = Category::getRoot().getInstance("mycat");
    root.setAppender(poa);
    /* root.setPriority(Priority::DEBUG); */
    root.setPriority(Priority::ERROR);

    //日志记录器：只有当日志的优先级大于等于Category的优先级的时候，日志
    //才会被记录，否则日志就会被过滤掉

    root.emerg("This is an emerg message");
    root.fatal("This is an fatal message");
    root.alert("This is an alert message");
    root.crit("This is an crit message");
    root.error("This is an error message");
    root.warn("This is an warn message");
    root.notice("This is an notice message");
    root.info("This is an info message");
    root.debug("This is an debug message");

    //回收
    Category::shutdown();
}
void test2()
{
    //日志的格式
    PatternLayout *ppl1 = new PatternLayout();
    ppl1->setConversionPattern("%d %c [%p] %m%n");

    PatternLayout *ppl2 = new PatternLayout();
    ppl2->setConversionPattern("%d %c [%p] %m%n");

    //日志的目的地
    //对于每一种日志的目的地，必须有自己的格式，不能共用
    OstreamAppender *poa = new OstreamAppender("OstreamAppender", &cout);
    poa->setLayout(ppl1);

    FileAppender *pfl = new FileAppender("FileAppender11", "wd.log");
    pfl->setLayout(ppl2);

    //日志种类
    Category &root = Category::getRoot().getInstance("mycat");
    root.addAppender(poa);
    root.addAppender(pfl);
    /* root.setPriority(Priority::DEBUG); */
    root.setPriority(Priority::ERROR);

    //日志记录器：只有当日志的优先级大于等于Category的优先级的时候，日志
    //才会被记录，否则日志就会被过滤掉

    root.emerg("This is an emerg message");
    root.fatal("This is an fatal message");
    root.alert("This is an alert message");
    root.crit("This is an crit message");
    root.error("This is an error message");
    root.warn("This is an warn message");
    root.notice("This is an notice message");
    root.info("This is an info message");
    root.debug("This is an debug message");

    //回收
    Category::shutdown();
}
void test3()
{
    //日志的格式
    PatternLayout *ppl1 = new PatternLayout();
    ppl1->setConversionPattern("%d %c [%p] %m%n");

    PatternLayout *ppl2 = new PatternLayout();
    ppl2->setConversionPattern("%d %c [%p] %m%n");

    //日志的目的地
    //对于每一种日志的目的地，必须有自己的格式，不能共用
    OstreamAppender *poa = new OstreamAppender("OstreamAppender", &cout);
    poa->setLayout(ppl1);

    RollingFileAppender *pfl = new RollingFileAppender("FileAppender11", "wd.log",
                                                       5 * 1024, 3);
    pfl->setLayout(ppl2);

    //日志种类
    Category &root = Category::getRoot().getInstance("mycat");
    root.addAppender(poa);
    root.addAppender(pfl);
    root.setPriority(Priority::DEBUG);
    /* root.setPriority(Priority::ERROR); */

    //日志记录器：只有当日志的优先级大于等于Category的优先级的时候，日志
    //才会被记录，否则日志就会被过滤掉

    for(size_t idx = 0; idx != 100; ++idx)
    {
        root.emerg("This is an emerg message");
        root.fatal("This is an fatal message");
        root.alert("This is an alert message");
        root.crit("This is an crit message");
        root.error("This is an error message");
        root.warn("This is an warn message");
        root.notice("This is an notice message");
        root.info("This is an info message");
        root.debug("This is an debug message");

    }

    //回收
    Category::shutdown();
}
int main(int argc, char **argv)
{
    test3();
    return 0;
}


```


# python3-proxypool
初学scrapy如何使用代理时用过的一个简易代理池，普通爬虫任务足够胜任。


## 主要模块：存储模块/获取模块/检测模块/接口模块


## 存储模块：

>采用Redis的有序集合构建（去重，区分优先级），代理ip作为元素，每个元素有一个分数字段（分数值可以重复）。
主要逻辑是 接收获取模块传递的代理并设置初始分数，向检测模块提供代理并根据检测结果给相应代理调整分数，向接口模块提供高分数代理。


## 获取模块：

>定义了一个Crawler类以及若干以 crawl_ 开头命名的方法（分别从不同网站获取代理），并使用元编程，使其可以自动识别这些方法并遍历，
方便后续添加或删除方法。

## 检测模块：


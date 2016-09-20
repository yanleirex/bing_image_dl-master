# bing_image_dl
download bing image

从bing上搜索关键字图片，并下载

使用redis实现一个分布式队列，并使用这个队列进行去重。

searching.py用来搜索图片链接并放入redis队列
download.py用来下载队列里面的图片链接

添加console来监控下载进度与redis状态
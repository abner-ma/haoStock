# haoStock
fantianhou get stock

I create this to get stock info.

设计目标：
自动从网页上获取股票的信息
初期使用python脚本编写，把本程序部署在服务器上后，通过每日定时任务，检查github，获得最新代码，定时执行
后期直接编写了haoStock.lua代码，放在openwrt的路由器上，通过crond定时在15点10分执行，把当日的股票情况发邮件到指定的邮箱了。
有需要的可以使用haoStock.lua，该脚本执行后获得的数据更全。

长时间不使用了。
Last updated: Sat Aug  9 12:26:44 UTC 2025

# PUL监测器

## Description

用于检查协作商户发出的PUL单，并将符合条件的数据自动导入至内部系统

## Software Architecture

* pyqt5: 基于C++源生界面框架，可跨平台使用
* sqlalchem: 常用ORM工具，在DB层搭载相应的驱动，可访问多类型数据库
* requests: http request发送工具，用于获取网页数据
* pyodbc,连接mysqlserver
* pymysql
* apscheduler: 定时任务工具，类似于Java | C# 的Quartz
* fbs: 将PYthon代码转换为其他平台应用，如osx, linux, windows 
* pyinstaller: fbs的组件
## 安装，打包，使用说明
  

***
### 下载

* [Python](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe)
* [NSIS](https://sourceforge.net/projects/nsis)
* [VCRuntime](https://www.microsoft.com/en-us/download/details.aspx?id=30679)

***
### 安装

* Python装在当前用户具有写权限的目录下，后续需要更新软件包
* NSIS装完后，需要在环境变量中加入相应的路径，保证编译期可以访问到

***
### 源码

* [下载地址](https://gitee.com/tju070/pul-monitor.git)
* 进入源码目录运行 **`python -m venv venv`**, 创建本项目虚拟环境
* 激活本地虚拟环境, 
  * Linux | MacOS: `source ./venv/bin/activate`
  * Windows: **`./venv/bin/activate.bat`**
* 在命令行更新pip版本,运行 **`python -m pip install --upgrade pip`**
* Python软件包:

    ```bash
    pip install xlrd sqlalchemy beautifulsoup4  HTMLParser configparser gbxmlparser bs4 lxml  apscheduler pymysql pyodbc requests PyQt5==5.9.2 fbs pywin32 pypiwin32
    ```

* 此软件包只是安装在本项目中，不影响Python的其他项目使用

***
### 配置

1.配置文件: 源码目录/src/main/resources/base/settings.ini  
2.配置文件节点

***
#### 通配置
* db:数据库类型，可选值为 **mysql** | **mssql**
* mssql: SQLServer的配置
* mysql: MySQL的配置
* app: 需要抓取的域名, **不需要更改**
* login: login地址及用户名密码,**不需要更改**
* query: 数据查询地址及参数, before是提交几天，after是当前时间往后几天, **据需求定义**
* schedule:是定时任务，interval指每几分钟执行一次, **据需求定义**
* close: 是退出时需要输入的密码， pwd是密码md5后的字串, 当前为yizitshanghai,**可自行设自密码，将MD5值填写pwd后面**
  * title是程序标题，**可换**
  * icon是程序图, **可换**
  * grid是日志表格的标题, 遇到空格会换行,**可换**
  
***
### 数据库

#### 表

* **pul_master**,是单据主表，从网站拉到的除所有信息都存在其中
* **pul_detail**,是主表中明细数据，主要是物料信息
* **pul_log**，是每次执行抓取的事件记录
* **xls_header** 从excel文件中读取的表头
* **xls_item** 从excel文件中读取的数据细项

#### 说明
* 系统在运行时会检查这三个数据表是否存在，不存在，将自动创建
* 以**pul**开头的表的数据都来自于json
* 以**xls**开头的表数据都来自于excel内容的解析
* pul_log主要记录本次获取的数据总数(**Total**)，被标为**Delivered**的数量，修订版本未变动量(**Revision Duplicated**)，变动量(**Revision Changed**)，新进数据(**Fresh Items**)
* pul_master与pul_detail字段名与数据库对应关系在**model.py**的文件中进行改动， 如:
  * **`Id = Column('id', String(36), index=True, primary_key=True)`**, 表示数据库中的表栏位id， I为小写
  * **`trans_time = Column(DateTime)`** ，trans_time的类属性名与数据库中字段名一致
* **xls_header** 与 **pul_master**是一对一的关系，在数据库中通过 **pu_master_id**建立关联，主表为 pul_master
* **xls_item** 是xls_header的从表

***
### 编译

* 运行：在源码目录下执行 **`fbs run`**
* 测试: **`fbs freeeze --debug`**, 测试通过, 无异常产生，可进行下一步
* 打包: **`fbs freeze`** 
* 安装: **`freeze installer`**

***
### 日志
* 文件名与路径在 PROJECT_ROOT/src/main/python/env.py中配置
* log_name是系统定义的log名称，不需要更改
* log_file是log文件存储的路径，可更改,新文件名，**中间需要留有 {0}**, 用于格式当前时间.
***
### 窗口

* 最小化后，会在托盘生成一个图标
* 托盘图标有两个菜单:
  * 显示主窗口
  * 退出程序， 退出时需要输入密码
  
***
### Changes Log

#### 2019-11-09

* 邮件发送，网易邮箱测试通过，不同邮件服务器会有不同的限制，请自行调试 
* 原则上网易不让发这样的邮件，需要在账号里面设置白名单，并将自己加到邮件列表中(CC)

#### 2019-11-08

* 增加了是否保存至本地的配置，
* setting.ini -> excel -> local = 1 保存至本地; path 是本地路径设置
* 文件名是当前pul单的 shipmentId.
* 增加了系统启动时，界面位于屏幕中间的功能

***
#### 2019-11-07

* *增加了 xls_header 与 xls_item 两个数据表*
* xls_header 对应 excel的表头, 其中 mv表示 MasterVendor, mv_1是MasterVendor下面第一行，mv_2是第二行；后面类推
* excel表头部分，过滤了 Master Vendor #的字串， 还有后面三个
* Excel的由于是异步生成，下载时间会有延迟，系统会每隔500毫秒查询一次文档是否生成, 查询10次后，将抛出异常，本次任务将被中止
* 由于Excel的数据明细，不确定是从47行开始，还是48行，系统做一次检查
* pip install xlrd, 用于处理excel的软件包
* 增加了对任务状态管理，同一时间只能运行一个任务

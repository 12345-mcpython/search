# search

#### 介绍
一个搜索引擎
专为mc(Minecraft)而生！
使用python, flask, mysql, scrapy等写成

#### 安装教程

1.  git clone https://gitee.com/aoligei1111111111/search1/
2.  pip install -r requirement.txt
3.  打开你的mysql
4.  建库, 建表
5.  在.env中配置mysql信息

建表：

CREATE TABLE IF NOT EXISTS `test`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `title` VARCHAR(1000) NOT NULL,
   `url` VARCHAR(4000) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

建库：

CREATE DATABASE so;



#### 使用说明

1.  python run_spider.py运行爬虫(暂时)
2.  python run.py运行flask web界面

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

#### 幕后

搜索组件是用in实现的......
```python
# if q in title:
#     data_.append(Text(url, title))
```
以后会改
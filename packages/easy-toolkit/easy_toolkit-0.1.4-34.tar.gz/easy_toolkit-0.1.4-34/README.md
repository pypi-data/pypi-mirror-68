# convenient_toolkit

#### 介绍
一个常用工具箱的命令行工具集，使用Click开发，配置文件路径为`$HOME/.easy_tools/config.json`，使用`json`字符串的形式。

#### 使用说明
直接运行`easytool`就可以查看命令分组            

#### 当前集成功能
1.github图床  
命令：`easytool gitpic -f your_pic_path`   
要求：配置文件中添加`github_token`或者`github_username`、`github_password`用于认证，同时还要添加事先创建好的仓库`github_reponame`名称（例如python的仓库名为`python/cpython`）          
参数：-f（--file）必须要，-n(--name)或-m(--message)非必须           



# 介绍
`axx-aiapi`是专门给`爱学习AILab`提供项目初始化的工具，通过该工具可以快速地创建一个`Flask`的初始项目/应用。新创建的项目/应用会包含良好的目录结构和基础的项目配置信息，无需再通过手工的方式创建这些基础目录和文件。

# 安装
```bash
pip install AXX-AIAPI 
```

# 快速开始
```bash
axx-aiapp create demo
cd demo
python manage.py 8080
```
使用你喜欢的浏览器访问`http://localhost:8080/demo/api` 你就可以成功访问到demoAPI

# 使用说明
## 单应用项目
项目模板具有以下特点：
- 基于`blueprint`进行`app`的路由和管理
- `app`目录基于`mvc`结构创建
- 集成了`gunicorn`作为正式环境的启动方式
- 集成了日志配置，通过`current_app.logger`对象直接使用
- 集成了通过`DBUtils`进行`MySQL`操作
- 对`app`异常进行了封装
- 提供了统一的`APIResponse`结构

### 创建方式
```bash
axx-aiapp create demo
```
该命令执行完成之后就会在当前目录创建`demo`的项目目录
创建完Flask项目之后，在命令行直接进入到应用的主目录，然后执行启动命令：
```bash
cd demo
python manage.py 8080
# or
python manage.py runserver 8080
```
启动完成之后可以执行访问`http://localhost:8080/demo/api` 来访问项目的示例接口。

### 线上部署
axx-aiapp集成了`gunicorn`来作为生成环境的部署方式，后台以`多进程+gevent`的方式提供并发支持,线上部署时使用如下命令：
```bash
sh startserver.sh
```
默认启动的端口号为`8000`，如果需要修改端口号，可在`config`目录下的`gunicorn.config.py`文件里修改`bind`字段。


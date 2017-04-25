# Django-getting-started

一个简单的使用 Django 的 Python 应用。
可以运行在 LeanEngine Python 运行时环境。

## 一键部署
[![Deploy to LeanEngine](http://ac-32vx10b9.clouddn.com/109bd02ee9f5875a.png)](https://leancloud.cn/1.1/functions/_ops/deploy-button)

## 本地运行

首先确认本机已经安装 [Python](http://python.org/) 运行环境和 [LeanCloud 命令行工具](https://www.leancloud.cn/docs/leanengine_cli.html)，然后执行下列指令：

```
$ git clone git@github.com:leancloud/django-getting-started.git
$ cd django-getting-started
```

### 安装依赖：

```
pip install -r requirements.txt
```

### 修改 settings.py:

修改 settings.py 中的 `SECRET_KEY` 值，确保它是一个足够长度的随机字符串，并且没有被其他人获知。详情参考[这里](https://docs.djangoproject.com/el/1.10/ref/settings/#std:setting-SECRET_KEY)。

修改 settings.py 中的 `ALLOWED_HOSTS` 值，确保它是**只**包含你即将部署的云引擎应用的域名的 `list`（本地调试期间可以暂时忽略）。详情参考[这里](https://docs.djangoproject.com/el/1.10/ref/settings/#allowed-hosts)。

### 关联应用：

```
lean app add origin <appId>
```

这里的 appId 填上你在 LeanCloud 上创建的某一应用的 appId 即可。origin 则有点像 Git 里的 remote 名称。

### 启动项目：

```
lean up
```

应用即可启动运行：[localhost:3000](http://localhost:3000)

## 部署到 LeanEngine

部署到预备环境（若无预备环境则直接部署到生产环境）：
```
lean deploy
```

将预备环境的代码发布到生产环境：
```
lean publish
```

## 相关文档

* [LeanEngine 指南](https://leancloud.cn/docs/leanengine_guide.html)
* [Python SDK 指南](https://leancloud.cn/docs/python_guide.html)
* [Python SDK API](https://leancloud.cn/docs/api/python/index.html)
* [命令行工具详解](https://leancloud.cn/docs/cloud_code_commandline.html)
* [LeanEngine FAQ](https://leancloud.cn/docs/cloud_code_faq.html)

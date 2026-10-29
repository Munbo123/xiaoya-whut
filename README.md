# <center>xiaoya-whut</center>
# <div align=right><font size=4 face="仿宋">武汉理工大学小雅脚本</font></div>

### 一：使用说明：
- [点击这里](https://github.com/Munbo123/xiaoya-video-watcher/releases/tag/v1.1)下载程序可执行文件，双击运行后，输入账号密码，等待自动下载driver并登录，选择任务进行完成即可 *(请等待“登录成功”出现后再进行操作)*
(有时候会出现bug，请试试看关掉重试几遍)


### 二：说明

#### 接口示例与登录凭据

- `api/auto_watch/check_task_status.py` 和 `api/auto_watch/commit_duration.py` 从环境变量 `XIAOYA_ACCESS_TOKEN` 读取登录 token；未设置时会退出。运行示例前，在本机 PowerShell 中设置 `$env:XIAOYA_ACCESS_TOKEN = '<your-access-token>'`，将占位符替换为自己的 token。不要把实际值提交到仓库或分享终端记录。
- token 来自自己登录后 Cookie 中的 `WT-prd-access-token`；它和学校标识 `school_id` 是不同字段。学校标识的获取方法见 [用户信息接口文档](api/user_info/user_info.md)。
- 如果曾公开真实 token，请撤销对应登录会话或通过平台支持的方式使旧凭据失效，再重新登录获取 token。修改当前文件不会删除 Git 历史或下游副本中的旧值；下游维护者需要各自清理。

- 目前程序还不是很完善，只是自己做来用的，后面会逐渐更新,萌新自己乱写的代码，也十分欢迎大佬pr，有问题也可以提出issue
- *待更新内容*：
  - [x] GUI界面
  - [x] 自动检测浏览器环境并下载驱动
  - [x] 打包成exe文件发布release
  - [ ] 用PyQt制作更好看的GUI
  - [ ] 尝试爬取课件
  - [ ] 下载到指定位置
  - [ ] 多线程下载
  - [ ] 下载进度条
  - [ ] 全部下载完成提示
  - [ ] 下载视频
  - [ ] 过滤掉对作业的下载
  - [ ] 让GUI更好看


### 三：感谢：
- 项目中用到的完成任务的API来自开源项目[Xiaoya-Script](https://github.com/ChrisKimZHT/Xiaoya-Script),感谢大佬开源







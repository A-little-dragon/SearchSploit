# SearchSploit (原ExploitDB)

## 项目介绍

原官方版本只能运行在Linux系统上，因此我将其重构为Python版本，解决了exploitdb在非Linux系统上的运行问题。通过重新编写和优化，我成功地使这个工具可以在Windows、Linux和Mac OS上流畅运行。我希望通过这个项目，更多的安全专业人员和爱好者能够轻松地使用exploitdb的功能，共同推进安全领域的发展。

## 参数说明

```jsx
[不带参数]
searchsploit.py value1 vulue2 vulue3 ...  返回模糊匹配参数值后的内容

[带参数]
searchsploit.py -t 模糊匹配标题内容  支持多值
searchsploit.py -p 指定端口号  支持多值
searchsploit.py -m [filename] [savepath] 下载漏洞利用程序脚本到指定路径
```

## 环境及依赖

| 环境 | 版本 |
| --- | --- |
| python | version > 3.8 |
| colorama | 0.4.6 |
| prettytable | 3.9.0 |

## 贡献者

| Author | GitHub | B站 | 身份 |
| --- | --- | --- | --- |
| 一条’小龍龙 | https://github.com/A-little-dragon | https://space.bilibili.com/645839191 | 主要贡献者 |

## 程序截图
https://www.notion.so/a-little-dragon/SearchSploit-ExploitDB-b45738cd36d04991a57627d2b97687dc?pvs=4#823ee5974e9a4544801768710158da01
![823ee5974e9a4544801768710158da01](https://www.notion.so/a-little-dragon/SearchSploit-ExploitDB-b45738cd36d04991a57627d2b97687dc?pvs=4#823ee5974e9a4544801768710158da01)

![251b35f0cb2143b7a4abd197627ed5b6](https://www.notion.so/a-little-dragon/SearchSploit-ExploitDB-b45738cd36d04991a57627d2b97687dc?pvs=4#251b35f0cb2143b7a4abd197627ed5b6)

![cab668e0384b458195a36008ba20bd5a](https://www.notion.so/a-little-dragon/SearchSploit-ExploitDB-b45738cd36d04991a57627d2b97687dc?pvs=4#cab668e0384b458195a36008ba20bd5a)

![232009e9b52844b6b67f33f901e2c1e6](https://www.notion.so/a-little-dragon/SearchSploit-ExploitDB-b45738cd36d04991a57627d2b97687dc?pvs=4#232009e9b52844b6b67f33f901e2c1e6)

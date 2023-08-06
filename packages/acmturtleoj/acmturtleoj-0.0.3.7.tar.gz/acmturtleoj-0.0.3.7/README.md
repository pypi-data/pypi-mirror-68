# OJ Client for Python3 Turtle

一、当遇到questype=9的题型时，需要访问(GET)：`https://myproxy.acmcoder.com:4443/run`

如果返回：
```
{result: "pong"}
```
则表示客户端已经启动。

否则：

提示：请按照如下步骤启动客户端：
1、安装Python3
2、打开命令行，输入：pip3 install --upgrade acmturtleoj && python -c "import acmturtleoj;acmturtleoj.main()"
3、回车，当360提示是否阻止该操作时，一定要选允许该操作
4、保持窗口不关闭
5、切换到考试界面继续答题。

二、往后端提交完代码后，需要访问(GET)：`https://myproxy.acmcoder.com:4443/run?user_id=abc&guid=def&solution_id=3`
其中：
user_id：考生端为Cands.id；报告端为生成的guid；
guid：考生端为Cands.guid；报告端为生成的guid；
solution_id：考生端如果有，则加上，如果没有，则为0；报告端为solutionId。
如果成功，则返回：
```
{result: "ok"}
```
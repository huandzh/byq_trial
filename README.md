# byq_trial

[![Build Status](https://travis-ci.org/huandzh/byq_trial.svg?branch=master)](https://travis-ci.org/huandzh/byq_trial)

百度舆情试用相关代码(codes for baidu yuqing trials)，`byq_trial.SimpleAuth`和`byq_trial.APICall`提供了快速利用百度舆情API的python调用方式。

注意：`byq_trial`**不是**百度舆情官方的调用方式，也不能起到SDK的作用，请向百度舆情咨询相关情况。

## 准备环境

`byq_trial`在`Python3.6`环境下开发，没有经过跨环境测试，但应该兼容`Python3`的各个版本。

### 安装python

为了方便试用，推荐安装[anaconda-python3.6](https://www.anaconda.com/download/)，这个发行版会包括多数会用到的科学计算包。

### 安装依赖

目前代码仅依赖`requests`包，如果使用anaconda的话不需要单独安装。

单独安装`requests`：

```shell
pip install requests
```
## 下载byq_trial到本地

使用git clone

```shell
git clone https://github.com/huandzh/byq_trial.git
```

直接下载zip包：点击本项目首页绿色按钮 `clone or download`

## 准备密钥文件

下载如下json格式的测试密匙文件（可由试用管理员处直接获得），并拷贝到byq_trial根目录下。

```json
{"access_key": "<百度云access_key>", "api_secret": "<舆情api_secret，或称user_secret>", "secret_key": "<百度云secret_key>", "api_key": "<舆情api_key，或称user_key>"}
```

如自行申请百度舆情试用，需要准备以上密钥文件：

* 百度云密钥可以从 https://console.bce.baidu.com/ 的安全中心（Security Center）获得
* 舆情试用密钥需要从百度舆情申请

## 测试byq_trial可用

进行单元测试，检查依赖安装和密钥文件准备是否成功。

发起测试：

```shell
python -m unittest
```

查看测试结果

    (byq_trial-OFj9Bl5y) ➜  byq_trial git:(master) ✗ python -m unittest
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.150s

    OK

## 使用代码

推荐在byq_trial根目录启动jupyter notebook，调用byq_trial模块进行百度舆情的试用。

exmaples目录（ https://github.com/huandzh/byq_trial/tree/master/examples ），欢迎参考。

## 如何贡献

您可以通过pull requests提供代码或示例，也可以通过issues提交问题。

* 问题：欢迎通过issues反馈软件包的bug，但百度舆情用法本身请您使用stackoverflaw等其他网站
* 代码：提交pull requests前请进行单元测试和PEP8测试(由于有效的测试需要使用密钥，CI仅提供了pep8的测试）
* 示例：请在代码库中的examples目录下创建新的示例，markdown格式

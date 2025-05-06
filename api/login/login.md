# 武汉理工大学智慧理工登录流程文档

## 概述

本文档详细记录了武汉理工大学智慧理工（理工智课）平台的完整登录请求链过程。整个登录流程涉及多个域名之间的跳转、CAS 单点登录认证以及 OAuth2 授权流程。

## 登录流程详解

### 步骤 1: 初始化会话

**请求类型**: 初始化

**操作**:

- 设置初始 Cookie: `WT-prd-language=zh-CN; WT-prd-teaching-schoolId=0`

### 步骤 2: 启动 CAS 认证流程

**请求类型**: GET

**URL**:

```
https://infra.ai-augmented.com/api/auth/cas/login?school_certify=10497&client_id=xy_client_whut&state=gvmu6k&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback&response_type=code&week_no_login_status=0&scope=&next=https%3A%2F%2Finfra.ai-augmented.com%2Fapp%2Fauth%2Foauth2%2FsecurityNotice%3Fresponse_type%3Dcode%26state%3Dgvmu6k%26client_id%3Dxy_client_whut%26redirect_uri%3Dhttps%3A%2F%2Fwhut.ai-augmented.com%2Fapi%2Fjw-starcmooc%2Fuser%2FauthorCallback%26school%3D10497%26lang%3Dzh_CN&back=https%3A%2F%2Finfra.ai-augmented.com%2Fapp%2Fauth%2Foauth2%2Flogin%3Fresponse_type%3Dcode%26state%3Dgvmu6k%26client_id%3Dxy_client_whut%26redirect_uri%3Dhttps%3A%2F%2Fwhut.ai-augmented.com%2Fapi%2Fjw-starcmooc%2Fuser%2FauthorCallback%26school%3D10497%26lang%3Dzh_CN
```

**响应**:

- 状态码: `302` (重定向)
- 设置 Cookie: `XY_AUTH_SESSION`
- 重定向至学校统一身份认证系统

### 步骤 3: 访问学校统一身份认证系统

**请求类型**: GET

**URL**:

```
http://zhlgd.whut.edu.cn/tpass/login?service=https%3A%2F%2Finfra.ai-augmented.com%2Fapi%2Fauth%2Fcas%2Flogin%3Fschool_certify%3D10497
```

**响应**:

- 状态码: `200`
- 设置 Cookie: 身份认证相关 Cookie
- 获取关键信息: 响应 HTML 中包含表单提交所需的`lt值`、`execution值`和`_eventId值`

### 步骤 4: 获取 RSA 加密公钥

**请求类型**: POST

**URL**:

```
https://zhlgd.whut.edu.cn/tpass/rsa?skipWechat=true
```

**响应**:

- 状态码: `200`
- 返回内容: RSA 公钥信息

### 步骤 5: 提交用户身份认证

**请求类型**: POST

**URL**:

```
https://zhlgd.whut.edu.cn/tpass/login?service=https%3A%2F%2Finfra.ai-augmented.com%2Fapi%2Fauth%2Fcas%2Flogin%3Fschool_certify%3D10497
```

**请求参数**:

- `ul`: 使用 RSA 公钥加密后的用户名
- `pl`: 使用 RSA 公钥加密后的密码
- `lt`: 步骤 3 获取的 lt 值
- `execution`: 步骤 3 获取的 execution 值
- `_eventId`: 步骤 3 获取的\_eventId 值

**响应**:

- 状态码: `302` (重定向)
- 设置 Cookie: 认证相关 Cookie
- 重定向 URL: 包含 CAS 票据(ticket)的 URL

### 步骤 6: 验证 CAS 票据

**请求类型**: GET

**URL**:

```
https://infra.ai-augmented.com/api/auth/cas/login?school_certify=10497&ticket=ST-312017-1GdaGHgVQkKE31nPHW6Y-tpass
```

**响应**:

- 状态码: `302` (重定向)
- 设置 Cookie: 授权相关 Cookie
- 重定向至 OAuth2 安全提示页面

### 步骤 7: 访问安全提示页面

**请求类型**: GET

**URL**:

```
https://infra.ai-augmented.com/app/auth/oauth2/securityNotice?response_type=code&state=glwq59&client_id=xy_client_whut&redirect_uri=https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback&school=10497&lang=zh_CN
```

**响应**:

- 状态码: `200`
- 作用: 安全验证提示页面

### 步骤 8: 身份认证重定向

**请求类型**: GET

**URL**:

```
https://infra.ai-augmented.com/api/auth/oauth/onAccountAuthRedirect
```

**响应**:

- 状态码: `302` (重定向)
- 设置 Cookie: OAuth 相关 Cookie
- 重定向至授权回调地址

### 步骤 9: 授权回调处理

**请求类型**: GET

**URL**:

```
https://whut.ai-augmented.com/api/jw-starcmooc/user/authorCallback?code=SqjV2TJdWTbhjX5516590869&state=glwq59&schoolCode=10497
```

**响应**:

- 状态码: `302` (重定向)
- 设置 Cookie: **多个关键业务 Cookie** (认证成功后的会话标识)
- 重定向至登录成功页面

### 步骤 10: 完成登录

**请求类型**: GET

**URL**:

```
https://whut.ai-augmented.com/auth/loginRedirect
```

**响应**:

- 状态码: `200`
- 作用: 登录成功确认页面

## 总结

该登录流程遵循典型的 CAS 单点登录+OAuth2 授权模式，通过多次重定向完成从统一身份认证到应用授权的全过程。整个过程中，关键点包括:

1. RSA 加密保护用户凭据安全
2. CAS 票据(ticket)验证用户身份
3. OAuth2 授权码(code)获取应用访问权限
4. 多个关键 Cookie 存储会话状态

此文档可用于开发自动化登录脚本或解决登录问题时的参考。

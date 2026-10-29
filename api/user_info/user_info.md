# 小雅平台用户信息 API 文档

本文档描述了小雅平台获取用户信息相关的 API 接口。

所有响应示例均用于说明字段结构，用户、学校、院系和头像标识使用占位符，不能直接作为登录配置使用。`school_id` 是学校标识，不是登录 token。

登录自己的小雅账号后，可在浏览器开发者工具的 Network（网络）面板查看 `currentUserInfo` 请求的响应，从 `result.schoolInfo.id` 获取自己的学校 ID，对应课程响应的 `school_id`。不要复制其他人的标识或公开完整响应、Cookie 和 Authorization 请求头。

## 用户基本信息

### 1. 获取用户 OAuth2 信息

**请求类型**: GET

**URL**:

```
https://whut.ai-augmented.com/api/jx-auth/oauth2/info
```

**请求头**:

```
Authorization: Bearer {access_token}
```

注：`access_token`来自 cookie 中的`WT-prd-access-token`字段

**响应示例**:

```json
{
  "code": 0,
  "success": true,
  "message": "ok",
  "data": {
    "type": "password",
    "client_id": "xiaoya_whut",
    "access_token_expires_in": "2025-05-06T19:49:09.785Z",
    "refresh_token_expires_in": "2025-05-07T08:49:09.785Z",
    "info": {
      "id": "<your-user-id>",
      "username": "张三",
      "mobile": "<your-mobile>",
      "email": "",
      "nickname": "",
      "avatar": "/cloud/file_access/<your-avatar-file-id>",
      "gender": 0,
      "roles": ["user"]
    }
  }
}
```

### 2. 获取当前用户详细信息

**请求类型**: GET

**URL**:

```
https://whut.ai-augmented.com/api/jw-starcmooc/user/currentUserInfo
```

**请求头**:

```
Authorization: Bearer {access_token}
```

**响应示例**:

```json
{
  "code": 200,
  "msg": "操作成功。",
  "result": {
    "id": "<your-account-id>",
    "realname": "张三",
    "nickname": "张三",
    "sex": "男",
    "headImageUrl": "/cloud/file_access/<your-avatar-file-id>",
    "authorId": "<your-user-id>",
    "roleDepartmentList": [
      {
        "id": "<your-department-id>",
        "className": "计算机2202",
        "departmentName": "计算机智能学院",
        "majorName": "计算机"
      }
    ],
    "schoolInfo": {
      "id": "<your-school-id>",
      "schoolName": "武汉理工大学",
      "schoolLogo": "https://aia-publication.oss-cn-shanghai.aliyuncs.com/oss-ccnu/jw/8963db2b7292478e84d16ce4226e9d8e.png"
    }
  }
}
```

**重要字段说明**:

1. 基本信息:

   - `result.id`: 用户 ID
   - `result.authorId`: 作者 ID（用于资源上传）
   - `result.realname`: 真实姓名
   - `result.nickname`: 昵称
   - `result.sex`: 性别（男/女）
   - `result.headImageUrl`: 头像路径

2. 院系信息（`result.roleDepartmentList[0]`）:

   - `id`: 院系记录 ID
   - `className`: 班级名称
   - `departmentName`: 学院名称
   - `majorName`: 专业名称

3. 学校信息（`result.schoolInfo`）:
   - `id`: 学校 ID
   - `schoolName`: 学校名称
   - `schoolLogo`: 学校 Logo URL

**备注**:

1. `roleDepartmentList`中的第一个元素通常是用户最新的院系信息

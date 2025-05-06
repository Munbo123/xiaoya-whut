# 小雅平台用户信息 API 文档

本文档描述了小雅平台获取用户信息相关的 API 接口。

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
      "id": "6248753284220235292",
      "username": "张三",
      "mobile": "13800138000",
      "email": "",
      "nickname": "",
      "avatar": "/cloud/file_access/6077049458644752007",
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
    "id": "88e1ca94320e078a98165fe88354ca3a",
    "realname": "张三",
    "nickname": "张三",
    "sex": "男",
    "headImageUrl": "/cloud/file_access/6077049458644752007",
    "authorId": "6248753284220235292",
    "roleDepartmentList": [
      {
        "id": "49cd631e5f1f4242a58ae102da3b4e7a",
        "className": "计算机2202",
        "departmentName": "计算机智能学院",
        "majorName": "计算机"
      }
    ],
    "schoolInfo": {
      "id": "f8d0cbf5d0d5aed8d698612d4212b7a9",
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

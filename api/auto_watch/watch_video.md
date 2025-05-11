整体思路应该还是先通过
https://whut.ai-augmented.com/api/jx-iresource/vod/duration/6709566608668395476/v2
提交观看记录
这里添加了v2，估计就是防了之前的脚本，做了第二版
负载从原本的
data = {
    "video_id": "0000000000000000000",  # 似乎不重要
    "played": duration,
    "media_type": 1,            # 任务type是9，media_type是'video'，似乎就是对应1
    "duration": duration,
    "watched_duration": duration
}

变成现在的：
message: "{\"video_id\":\"107dcd2a2a2271f088b06733a68f0102\",\"played\":30.16,\"media_type\":1,\"duration\":403.64,\"watched_duration\":30.154322}"
nonce: "e239edfb-d015-44bd-9028-37ee61042380"
signature: "610f8bddfd4391e7d18dc628f055234747b10f20"
timestamp: "1746772507287"

只是把之前的data塞到了message中，然后添加了一次性uuid凭证和疑似是SHA1的签名signature

方法：post 状态：200

响应：
{
    "code": 0,
    "success": true,
    "message": "ok",
    "data": {
        "id": "6711863735251662619",
        "media_type": 1,
        "video_id": "107dcd2a2a2271f088b06733a68f0102",
        "media_id": "6709566608668395476",
        "position_flag": "",
        "duration": "403.64",
        "played": "361.45",
        "watched_duration": "361.42",
        "device_type": 1,
        "user_id": "6248753284220235292",
        "info": {},
        "created_at": "2025-05-09T06:35:07.440Z",
        "updated_at": "2025-05-09T06:40:38.728Z"
    }
}

似乎是为了客户端更新进度条等状态用的，这里应该用不上



==========================隔离==========================

最后，再使用
https://whut.ai-augmented.com/api/jx-iresource/vod/checkTaskStatus
提交观看完成的信息

方法：post，状态：200

这个的负载似乎没有变，还是：
assign_id: "6709567503271470853"
group_id: "6630748513288344594"
media_id: "6709566608668395476"
task_id: "6709567503271470852"


group_id就是课程id
media_id就是任务信息中resource里面的id
task_id就是任务信息中的id
assign_id似乎是来自studentfinishinfo这个api中的，并且和状态无关，就是固定的一个数字

响应信息为：
{'code': 0, 'success': True, 'message': 'ok', 'data': {'status': 1}}
如果status为1，表示没有成功，是因为没有提交观看记录就点击了，重复提交好像也是1
如果status为0，表示成功了



任务信息的url是：
https://whut.ai-augmented.com/api/jx-iresource/resource/queryResource?node_id=6709566682538483312
方法：get 状态：200

其中的node_id似乎就是资源id

返回结果是：
{
    "code": 0,
    "success": true,
    "message": "ok",
    "data": {
        "id": "6709566682538483312",
        "parent_id": "6690295640435459471",
        "path": "6630748513296733203/6690295640435459471/6709566682538483312",
        "level": null,
        "name": "xxxx",
        "type": 9,
        "mimetype": null,
        "creator": "5986462488546262471",
        "group_id": "6630748513288344594",
        "quote_id": "6709566608668395476",
        "del": 1,
        "public": 2,
        "lock": 1,
        "download": 1,
        "copy": 1,
        "property": {
            "task_type": 1
        },
        "created_at": "2025-05-06T02:31:17.420Z",
        "updated_at": "2025-05-06T02:33:01.293Z",
        "sort_position": 3,
        "finish_teaching": 0,
        "published": 1,
        "publish_record_id": "0",
        "tag": null,
        "resource_type": 5,
        "author": "5986462488546262471",
        "resource": {
            "id": "6709566608668395476",
            "media_type": "video",
            "file_name": "xxxx",
            "title": "xxx",
            "video_id": "107dcd2a2a2271f088b06733a68f0102",
            "size": 24204870,
            "duration": "403.6",
            "cover_url": "https://vod.ai-augmented.com/107dcd2a2a2271f088b06733a68f0102/snapshots/a083274ce95a4c20b6256d1d15591789-00005.jpg?auth_key=1746772463-5e7ba0f0cff3489bee74bccdf6af08-0-5211afd62955aee5cf85db4979c44b65",
            "status": "Normal",
            "disk_status": 1
        },
        "task_id": "6709567503271470852",
        "task_type": 1,
        "start_time": "2025-05-06T02:32:45.959Z",
        "end_time": "2025-06-30T15:59:59.999Z",
        "assign_to_type": 3,
        "watch_min_minutes": 2,
        "discussion_task_assign": []
    }
}



studentfinishinfo的api则是如下：

https://whut.ai-augmented.com/api/jx-iresource/resource/task/studenFinishInfo?group_id=6630748513288344594&node_id=6709566682538483312

方法：get，状态：200

group_id和node_id显而易见

响应：
{
    "code": 0,
    "success": true,
    "message": "ok",
    "data": {
        "finish_time": 0,
        "rejected": false,
        "finished": false,
        "assign_id": "6709567503271470853",
        "operator_id": ""
    }
}
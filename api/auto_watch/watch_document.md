观看文件的时间记录似乎是纯前端的，自动完成只需要发一个请求即可
https://whut.ai-augmented.com/api/jx-iresource/resource/finishActivity

方法：post，状态码：200

负载：
group_id: "6630748834572050390"
node_id: "6659161511023400845"
task_id: "6716091695655556237"

这些字段的意义很好理解，在搞视频的时候就搞过了

响应:
{
    "code": 0,
    "success": true,
    "message": "ok",
    "data": {
        "operator_id": "6248753284220235292",
        "answer_record_id": null,
        "group_id": "6630748834572050390",
        "task_id": "6716091695655556237",
        "finish_time": "2025-05-15T14:10:20.131Z",
        "assign_id": "6716091695663944846",
        "status": 1,
        "assign_to_id": "6630748834572050390"
    }
}
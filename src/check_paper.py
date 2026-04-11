import json
from core.xiaoya_login_manager import XiaoyaLoginManager


def check_score(data):
    """传入一个paper数据，输出没有满分的题目"""
    questions = data["data"]["questions"]
    mark_answers = data["data"]["mark_records"][0]["mark_answers"]
    cnt = 1

    for mark_answer in mark_answers:
        question_id = mark_answer["question_id"]
        check_score = mark_answer["check_score"]

        for question in questions:
            if question["id"] == question_id:
                if question["score"] != check_score:
                    content = json.loads(question["title"])
                    print(
                        f"{cnt}.Question Text: {content['blocks'][0]['text']} check_score: {check_score} score: {question['score']}"
                    )
                    cnt += 1

    if cnt == 1:
        print("所有题目都满分！")


def query_stu_paper(group_id, paper_id, login_manager: XiaoyaLoginManager):
    url = f"https://whut.ai-augmented.com/api/jx-iresource/survey/course/queryStuPaper?paper_id={paper_id}&group_id={group_id}"

    headers = login_manager.get_headers()
    session = login_manager.get_session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0:
            return data
        else:
            print(f"Error: {data['message']}")
    else:
        print(f"Request failed with status code: {response.status_code}")


if __name__ == "__main__":
    username = "1023000971"
    password = "nf3039755985"
    login_manager = XiaoyaLoginManager()
    print("正在登录...")
    login_manager.login(username, password)
    print("登录成功！")

    group_id = "6791218493657221017"
    paper_id = "6796838585753460223"

    data = query_stu_paper(group_id, paper_id, login_manager)
    if data:
        check_score(data)

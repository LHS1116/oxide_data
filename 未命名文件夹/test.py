import requests













def create_feishu_doc(title):
    user_access_token = "u-4MLHv2pfVfm8g1W77iv8je"
    folderToken = "fldcnqgDAWCd62h0CDwGx2EfKog"
    type = "sheet"
    url = "https://open.feishu.cn/open-apis/doc/v2/create"
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + user_access_token
    }
    params = {
        # "title": title,
        # "type": type
        # "FolderToken": folderToken,

    }
    r = requests.post(url=url, headers=header, json=params)
    results = r.json()

    return results

res = create_feishu_doc("测试1")
print(res)
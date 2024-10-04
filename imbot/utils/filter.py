import re

def is_complete_sentence(query):
    # 检查是否为完整句子    # 句子必须以字母开头，并且以句号、问号或感叹号结束
    return bool(re.match("^[a-zA-Z].*[.!?]$", query))
# memeapi/utils/params_filter.py
from fastapi import HTTPException

def filter_params(params: dict, allowed_params: list):
    """
    过滤输入参数，移除未被允许的字段。
    
    :param params: 请求参数字典
    :param allowed_params: 允许的参数列表
    :return: 过滤后的字典
    """
    filtered_params = {key: value for key, value in params.items() if key in allowed_params}
    
    # 检查是否有无效的参数
    if len(filtered_params) != len(params):
        invalid_keys = set(params) - set(filtered_params)
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {invalid_keys}")
    
    return filtered_params
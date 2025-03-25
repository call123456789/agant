def clean_code(input_string=''):
    # 去除开头的 'python'''（如果存在）
    if input_string.startswith("```python"):
        input_string = input_string[len("```python"):].lstrip()
    
    # 去除结尾的 '''（如果存在）
    if input_string.endswith("```"):
        input_string = input_string[:-3].rstrip()
    
    return input_string
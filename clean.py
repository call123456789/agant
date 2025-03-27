def clean_code(input_string=''):
    start = "```python"
    end = "```"
    start_index = input_string.find(start)
    end_index = input_string.find(end, start_index + len(start))
    
    if start_index != -1 and end_index != -1:
        return input_string[start_index + len(start):end_index].strip()
    
    return input_string

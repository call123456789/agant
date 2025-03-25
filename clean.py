def clean_code(input_string=''):
    if input_string.startswith("```python"):
        input_string = input_string[len("```python"):].lstrip()
    
    if input_string.endswith("```"):
        input_string = input_string[:-3].rstrip()
    
    return input_string

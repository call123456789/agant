class SensitiveFilter:
    def __init__(self, sensitive_words=None, replace_char='*'):
        """初始化敏感词过滤器"""
        self.replace_char = replace_char
        self.sensitive_tree = self._build_sensitive_tree(sensitive_words or [])
        self.add_word('文化大革命')
        self.add_word('林彪')
    
    def _build_sensitive_tree(self, sensitive_words):
        """构建敏感词树（DFA算法）"""
        tree = {}
        for word in sensitive_words:
            node = tree
            for char in word:
                node = node.setdefault(char, {})
            node['is_end'] = True
        return tree
    
    def add_word(self, word):
        """添加单个敏感词"""
        node = self.sensitive_tree
        for char in word:
            node = node.setdefault(char, {})
        node['is_end'] = True
    
    def add_words(self, words):
        """批量添加敏感词"""
        for word in words:
            self.add_word(word)
    
    def filter(self, text, mode='min_match'):
        """
        过滤文本中的敏感词
        mode: 'min_match'（最小匹配）或 'max_match'（最大匹配）
        """
        if not text or not self.sensitive_tree:
            return text
        
        result = list(text)
        length = len(text)
        i = 0
        
        while i < length:
            match_node = self.sensitive_tree
            match_len = 0
            max_match_len = 0
            
            # 查找从位置i开始的所有可能敏感词
            for j in range(i, length):
                char = text[j]
                if char not in match_node:
                    break
                match_node = match_node[char]
                match_len += 1
                if match_node.get('is_end', False):
                    max_match_len = match_len
            
            # 根据匹配模式处理
            if max_match_len > 0:
                replace_len = max_match_len if mode == 'max_match' else 1
                result[i:i+replace_len] = [self.replace_char] * replace_len
                i += replace_len  # 跳过已替换的部分
            else:
                i += 1
        
        return ''.join(result)

# 使用示例
if __name__ == "__main__":
    # 初始化过滤器
    filter = SensitiveFilter(['敏感词', '测试', '不良信息'])
    
    # 测试过滤功能
    test_text = "这是一段包含敏感词的测试文本，含有不良信息。"
    filtered_text = filter.filter(test_text)
    print(f"原始文本: {test_text}")
    print(f"过滤后: {filtered_text}")
    
    # 添加新的敏感词
    filter.add_word('新增敏感词')
    filtered_text = filter.filter("新增敏感词也会被过滤", mode='max_match')
    print(f"添加新词后: {filtered_text}") 
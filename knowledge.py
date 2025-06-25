from openai import OpenAI
import numpy as np
import json, os, re
from datetime import datetime
from reader import extract_text
def create_embeddings(input):
    with open('set.json', 'r') as file:
        config = json.load(file)
    client = OpenAI(
        base_url=config.get('base_url'),
        api_key=config.get('api_key'),
    )

    resp = client.embeddings.create(
        model=config.get('embedding-model'),
        input=input
    )

    return [np.array(i.embedding) for i in resp.data]

def cosine_similarity(vec1,vec2):
    return np.dot(vec1, vec2.T) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def compute_breakpoints(similarity_scores, threshold=90):
    threshold_value = np.percentile(similarity_scores, threshold)
    return [i for i, score in enumerate(similarity_scores) if score < threshold_value]

def split_into_chunks(sentence_list, break_indices):
    semantic_chunks = []
    current_start_index = 0
    for bp in break_indices:
        semantic_chunks.append(". ".join(sentence_list[current_start_index:bp + 1]) + ".")
        current_start_index = bp + 1
    semantic_chunks.append(". ".join(sentence_list[current_start_index:]))
    return semantic_chunks

def semantic_search(query, k=6):
    text_chunks = []
    embeddings = []
    data_dir = 'resources/knowledge/data'
    
    # 遍历目录下所有json文件
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                text_chunks.extend(data['words'])
                # 在加载 embeddings 处添加类型判断
                embeddings.extend([np.array(emb) for emb in data['embeddings']])
    
    query_embedding = create_embeddings(query)[0]
    similarity_scores = []
    for i, chunk_embedding in enumerate(embeddings):
        score = cosine_similarity(query_embedding.reshape(1, -1), chunk_embedding.reshape(1, -1))[0][0]
        similarity_scores.append((i, score))
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    top_indices = [index for index, _ in similarity_scores[:k]]
    ans_list = [text_chunks[index] for index in top_indices]
    ans_str = '知识库中相关信息如下：\n'
    for i, j in enumerate(ans_list):
        ans_str += str(i+1)+'、' + j + '\n'
    return ans_str


def process_text(text):
    # 去除空字符串和前后空格
    sentences = re.split(r'[。\.\n] ', text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    #生成句子向量
    embeddings = create_embeddings(sentences)
    #计算相似度
    similarities = [cosine_similarity(embeddings[i].reshape(1, -1), embeddings[i + 1].reshape(1, -1))[0][0] for i in range(len(embeddings) - 1)]
    #根据相似度计算分段点
    breakpoints = compute_breakpoints(similarity_scores=similarities, threshold=90)
    #根据分段点进行分段
    chunks = split_into_chunks(sentence_list=sentences, break_indices=breakpoints)
    #为每段生成段落向量
    chunks_embeddings = create_embeddings(chunks)
    #把文本和向量打包
    dict = {'words':chunks ,'embeddings': [emb.tolist() for emb in chunks_embeddings]}
    #存储在本地
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = 'resources/knowledge/data/' + now + '.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(dict, f, ensure_ascii=False, indent=4)

    return filename    


if __name__ == '__main__':
    process_text(extract_text('resources/knowledge/user/2.docx'))
    query = '语文多少分'
    top_chunks = semantic_search(query, k=2)
    print("Query:", query)
    for i, chunk in enumerate(top_chunks): 
        print(f"Context {i + 1}:\n{chunk}\n=====================================")
from fastapi import FastAPI
import json
import requests
import boto3
import re
from openai import OpenAI

import warnings
warnings.filterwarnings("ignore")

from index import load_index
from utils import get_chat_access_token
from request_data import RetrievalRequest, GraphRequest, RagRequest
from config import server_config
from py2neo import Graph, Node, Relationship

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "test"))

app = FastAPI()

# 初始化向量库
index_db = load_index()

AK = server_config.AK
SK = server_config.SK

# AWS 配置
AWS_CONFIG = {
    'service_name': 'bedrock-runtime',
    'region_name': 'us-west-2',
    'aws_access_key_id': '*****************',  # 替换为你的 AWS Access Key ID
    'aws_secret_access_key': '*******************'  # 替换为你的 AWS Secret Access Key
}

# 模型配置
MODEL_CONFIG = {
    'model_id': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
    'max_tokens': 500,  # 设置生成的最大 token 数
    'temperature': 0.7,  # 设置生成文本的随机性（0-1）
    'top_p': 0.9  # 设置 nucleus sampling 的阈值（0-1）
}

# 创建 Boto3 客户端
client = boto3.client(
    service_name=AWS_CONFIG['service_name'],
    region_name=AWS_CONFIG['region_name'],
    aws_access_key_id=AWS_CONFIG['aws_access_key_id'],
    aws_secret_access_key=AWS_CONFIG['aws_secret_access_key']
)

client = OpenAI(
    api_key="************************",
    base_url="https://api.deepseek.com"
)

@app.get("/")
async def root():
    return {"message": "欢迎来到建筑文章生成平台"}

@app.post("/rag_retrieval")
async def rag_retrieval(data: RetrievalRequest):
    query = data.query
    # RAG语料召回
    recall_chunks = index_db.similarity_search(query)
    context = ""
    if len(recall_chunks) > 0:
        for chunk in recall_chunks:
            context += chunk.page_content + "\t"
    #logger.info(f"rag_retrieval info---query: {query}, content: {context}")
    print("rag召回结果:")
    print(context)
    return {"content": context}

@app.post("/graph_retrieval")
async def graph_retrieval(data: GraphRequest):
    query = data.query
    prompt = f"""使用自然语言抽取三元组,已知下列句子,请从句子中抽取出可能的实体、关系,
    所抽取的实体关系必须要在以下分类范围内:
    建筑艺术
    建筑艺术是中轴线的核心艺术形式，包含建筑的主要元素和构成部分。
    - 建筑：建筑本体，包括外观、结构和尺度。
    - 材料：用于建筑的物质，如汉白玉、檀木等，决定美学和稳定性。
    - 构件：建筑的基本组成单元，如柱子、琉璃瓦等。
    - 形制：建筑的形状、结构和比例。
    - 功能：建筑的用途，如祭祀、居住等。

    ---
    装饰艺术（）
    装饰艺术关注中轴线建筑的图案、色彩和工艺，展示装饰元素的艺术表现。
    - 纹样：装饰的基本图案与形状。
    - 色彩：装饰和建筑的色彩设计，影响视觉效果和情感表达。
    - 工艺：装饰或构件创作和制作过程中使用的技术与方法。
    - 题材：装饰艺术的主题分类，如自然、文化等。

    ---
    选址与空间布局
    此部分探讨建筑选址与空间布局艺术，重点是建筑与其环境的关系。
    - 选址：建筑的具体地理位置和抽象位置意义。
    - 布局：建筑的空间安排，如中轴对称等。

    ---
    历史与文化背景
    历史与文化背景关系到北京中轴线的形成与传承，涉及多个方面的外部因素。
    - 生态环境：建筑所处的自然环境及其生态特点。
    - 社会活动：与建筑相关的社会功能和活动。
    - 文化氛围：与建筑艺术关联的文化背景。
    - 政治与经济：影响建筑及空间设计的政治和经济因素。

    ---
    时间维度
    时间维度反映了建筑艺术和文化遗产的历史演变，包括不同历史阶段的时间信息。
    - 历史纪年：不同历史时期使用的纪年方式。
    - 历史阶段：涉及中轴线建筑和文化遗产的历史时期和阶段。

    ---
    角色与组织
    此部分涉及与北京中轴线相关的个人与组织，反映他们在文化遗产中的作用。
    - 个体角色：与中轴线相关的历史人物、建筑师、艺术家等。
    - 组织角色：政府、研究机构、文化单位等团体的角色。

    ---
    文化文献
    文化文献包括与北京中轴线相关的历史文献和经典书籍，承载着历史与文化知识。
    - 历史档案：记录中轴线历史和文化的文献资料。
    - 经典著作：具有文化和学术价值的书籍与文件。

    ---
    文化理念
    文化理念指的是影响北京中轴线设计与艺术表达的哲学观念和思想体系。
    - 哲学思想：与建筑艺术相关的哲学理论。
    - 历史典故：影响建筑和装饰设计的历史故事和象征。

    ---
    所有分类总结如下:
    建筑艺术:建筑, 建筑艺术:材料, 建筑艺术:构件, 建筑艺术:形制, 建筑艺术:功能
    装饰艺术:纹样, 装饰艺术:色彩, 装饰艺术:工艺, 装饰艺术:题材 
    选址与空间布局:选址, 选址与空间布局:布局
    历史与文化背景:生态环境, 历史与文化背景:社会活动, 历史与文化背景:文化氛围, 历史与文化背景:政治与经济
    时间维度:历史纪年, 时间维度:历史阶段
    角色与组织:个体角色, 角色与组织:组织角色
    文化文献:历史档案, 文化文献:经典著作, 文化理念:哲学思想, 文化理念:历史典故

    示例：
    句子：故宫的建筑设计体现了中国古代的哲学思想。
    提取的三元组：(故宫, 体现, 中国古代的哲学思想, 文化理念:哲学思想)

    你可以先识别出实体再判断实体之间的关系,以(头实体,关系,尾实体,关系分类)的形式回答，请尽可能多的返回所有实体关系，不要添加其他任何多余解释信息，保证格式化输出:
    句子：{query}
    提取的三元组："""

    #query = "请生成一篇文章，全面介绍中轴线的核心历史节点（如故宫、天坛、钟鼓楼等）及其文化意义。文章需涵盖中轴线在不同历史时期的演变过程，并突出其作为中华文化象征的重要性。"

    request = prompt
    print(request)


    try:
        # 调用模型
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages = [
                {
                    "role": "user",
                    "content": request
                }
            ],
            temperature=0.1,
            stream = False
        )
        print(response.choices[0].message.content)

        content = response.choices[0].message.content
        triples_temp = content.split("\n")
        triples = []

        for item in triples_temp:
            item = item.strip("(").strip(" ").strip(")").split(",")
            head, relation, tail, relation_category = item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip()
            triples.append((head, relation, tail, relation_category))

        print("当前请求的三元组提取结果:\n")
        print(triples)

        if len(triples) > 0:
            neighbors = []
            for item in triples:
                #print(item)
                #head, relation, tail, relation_category = item["head"], item["relation"], item["tail"], item["relation_category"]
                head, relation, tail, relation_category = item[0], item[1], item[2], item[3]
                #sql =  "MATCH (e1:Building1 {name: '端门'})-[r:位于]->(e2:Building2) where r.位于='选址与空间布局:布局' return e2.name limit 5"
                sql = f"""MATCH (e1:Building1)-[r:{relation}]->(e2:Building2) where e1.name = '{head}' return e2.name limit 5"""
                result = graph.run(sql)
                #print(result)
                for record in result:
                    neighbors.append(record['e2.name'])
            neighbors = list(set(neighbors))
        result = "与文本有关系的其他实体包括：" + ",".join(neighbors)
        print("graph召回结果:")
        print(result)
        return {"content": result}
    except Exception as e:
        print(f"调用模型时出错: {e}")
        return {"content": ""}

@app.post("/rag_chat1")
async def rag_chat1(data: RagRequest):
    query = data.query
    rag_chunks = data.rag_chunks
    graph_chunks = data.graph_chunks
    temperature = data.temperature
    url = server_config.ERNIE_SPEED_8K_URL + get_chat_access_token(AK, SK)
    
    prompt = f'''请你作为化身文章写作专家，我会给你提供相关的背景资料，你需要结合我的背景资料，完成相关的文章创作，文章一定要完成，不能丢失段落。
    参考背景资料如下：\n
    ------------------\n
    {rag_chunks}\n
    {graph_chunks}\n
    ------------------\n
    用户的问题如下: \n
    {query}\n
    ------------------\n
    下面请你根据提供的语料进行文章创作。
    '''

    # 构建请求体
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",  # 指定 Anthropic 版本
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": MODEL_CONFIG['max_tokens'],
        "temperature": MODEL_CONFIG['temperature'],
        "top_p": MODEL_CONFIG['top_p']
    }

    try:
        # 调用模型
        response = client.invoke_model(
            modelId=MODEL_CONFIG['model_id'],
            contentType='application/json',
            accept='application/json',
            body=json.dumps(request_body)
        )

        # 解析响应
        response_body = json.loads(response['body'].read())
        generated_text = response_body['content'][0]['text']
    except:
        generated_text = ""
    print(generated_text)
    return {"content": generated_text}
    
    if response.text:
        answer = json.loads(response.text)
        result = answer["result"]
        #logger.info(f"problem_answer_chat info---query: {query}, retrieval_chunks: {retrieval_cunks}, temperature: {temperature}")
        return {"content": result}
    else:
        return {"content": "抱歉，暂时查询不到信息"}


@app.post("/rag_chat")
async def rag_chat(data: RagRequest):
    query = data.query
    rag_chunks = data.rag_chunks
    graph_chunks = data.graph_chunks
    temperature = data.temperature
    url = server_config.ERNIE_SPEED_8K_URL + get_chat_access_token(AK, SK)
    
    prompt = f'''请你作为化身文章写作专家，我会给你提供相关的背景资料，你需要结合我的背景资料，完成相关的文章创作。
    参考背景资料如下：\n
    ------------------\n
    {rag_chunks}\n
    {graph_chunks}\n
    ------------------\n
    用户的问题如下: \n
    {query}\n
    ------------------\n
    下面请你根据提供的语料进行文章创作。
    '''

    # 调用模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.1,
        stream = False
    )
    #print(response.choices[0].message.content)
    result = response.choices[0].message.content

    if result:
        #logger.info(f"problem_answer_chat info---query: {query}, retrieval_chunks: {retrieval_cunks}, temperature: {temperature}")
        return {"content": result}
    else:
        return {"content": "抱歉，暂时查询不到信息"}
    

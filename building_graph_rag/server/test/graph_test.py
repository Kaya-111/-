import pandas as pd
from py2neo import Graph, Node, Relationship

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "neo4j"))

# 读取 CSV 数据（假设文件名为 data.csv）
df = pd.read_csv('person.csv')
df.columns = df.columns.str.strip()

# 遍历每一行数据并创建图形
for index, row in df.iterrows():
    # 获取实体1、关系、实体2 和关系属性
    entity1 = row['Entity1']
    relationship = row['Relationship']
    entity2 = row['Entity2']
    relationship_property = row['RelationshipProperty']

    # 创建实体1和实体2的节点
    node1 = Node("Person", name=entity1)  # 实体1是Person类型的节点
    node2 = Node("Person", name=entity2)  # 实体2也是Person类型的节点

    # 将节点添加到图中，如果已经存在则跳过
    graph.merge(node1, "Person", "name")
    graph.merge(node2, "Person", "name")

    # 创建关系并设置属性
    rel = Relationship(node1, relationship, node2)
    rel[relationship] = relationship_property  # 设置关系属性

    # 将关系添加到图中
    graph.merge(rel)

print("数据已成功导入到 Neo4j 中！")

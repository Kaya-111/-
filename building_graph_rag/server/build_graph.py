#!/usr/bin/env python3
# coding: utf-8
from py2neo import Graph, Node, Relationship
import pandas as pd
import re
import os


class BuildingGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'neo4j_data/triples_no_duplicates.csv')
        self.graph = Graph("http://localhost:7474", auth=("neo4j", "test"))

    def read_file(self):
        """
        读取文件，获得实体，实体关系
        :return:
        """
        # 实体
        architecture_arts = []  # 建筑艺术
        role_orgs = []  # 角色与组织
        hist_cultures = []  # 历史与文化背景
        temporal_dims = [] # 时间维度
        culture_concepts = [] # 文化理念
        culture_docs = [] # 文化文献
        spatial_arts = [] # 选址与空间布局
        ornamental_arts = [] # 装饰艺术

        building_nodes = []
        material_nodes = []
        goujian_nodes = []
        xingzhi_nodes = []
        function_nodes = []

        all_data = pd.read_csv(self.data_path).loc[:, :].values
        for data in all_data:
            entity1 = data[0]
            rel = data[1]
            entity2 = data[2]
            entity_label = data[3]
            entity_label1 = entity_label.split(":")[0]
            entity_label2 = entity_label.split(":")[1]
            if entity_label1 == "建筑艺术": # architecture_art
                rel_type = "包含"
                if entity_label2 == "建筑":
                    architecture_arts.append("建筑艺术", entity1, rel_type, rel, "建筑", entity2)
                    building_nodes.append(entity2)
                elif entity_label2 == "材料":
                    architecture_arts.append("建筑艺术", entity1, rel_type, rel, "材料", entity2)
                elif entity_label2 == "构件":
                    architecture_arts.append("建筑艺术", entity1, rel_type, rel, "构件", entity2)
                elif entity_label2 == "形制":
                    architecture_arts.append("建筑艺术", entity1, rel_type, rel, "形制", entity2)
                elif entity_label2 == "功能":
                    architecture_arts.append("建筑艺术", entity1, rel_type, rel, "功能", entity2)
                else:
                    pass
            elif entity_label1 == "角色与组织": # role_org
                rel_type = "包含"
                if entity_label2 == "个体角色":
                    role_orgs.append("角色与组织", entity1, rel_type, rel, "个体角色", entity2)
                elif entity_label2 == "组织角色":
                    role_orgs.append("角色与组织", entity1, rel_type, rel, "组织角色", entity2)
                else:
                    pass
            elif entity_label1 == "历史与文化背景": # hist_culture
                rel_type = "包含"
                if entity_label2 == "生态环境":
                    hist_cultures.append("历史文化与背景", entity1, rel_type, rel, "生态环境", entity2)
                elif entity_label2 == "社会生活":
                    hist_cultures.append("历史文化与背景", entity1, rel_type, rel, "社会生活", entity2)
                elif entity_label2 == "文化氛围":
                    hist_cultures.append("历史文化与背景", entity1, rel_type, rel, "文化氛围", entity2)
                elif entity_label2 == "政治与经济":
                    hist_cultures.append("历史文化与背景", entity1, rel_type, rel, "政治与经济", entity2)
                else:
                    pass
            elif entity_label1 == "时间维度": # temporal_dim
                rel_type = "包含"
                if entity_label2 == "历史纪年":
                    temporal_dims.append("时间维度", entity1, rel_type, rel, "历史纪年", entity2)
                elif entity_label2 == "历史阶段":
                    temporal_dims.append("时间维度", entity1, rel_type, rel, "历史阶段", entity2)
                else:
                    pass
            elif entity_label1 == "文化理念": # culture_concept
                rel_type = "包含"
                if entity_label2 == "哲学思想":
                    culture_concepts.append("文化理念", entity1, rel_type, rel, "哲学思想", entity2)
                elif entity_label2 == "历史典故":
                    culture_concepts.append("文化理念", entity1, rel_type, rel, "历史典故", entity2)
                else:
                    pass
            elif entity_label1 == "文化文献": # culture_doc
                rel_type = "包含"
                if entity_label2 == "历史档案":
                    culture_docs.append("文化文献", entity1, rel_type, rel, "历史档案", entity2)
                elif entity_label2 == "经典著作":
                    culture_docs.append("文化文献", entity1, rel_type, rel, "经典著作", entity2)
                else:
                    pass
            elif entity_label1 == "选址与空间布局": # spatial_art
                rel_type = "包含"
                if entity_label2 == "选址":
                    spatial_arts.append("选址与空间布局", entity1, rel_type, rel, "选址", entity2)
                elif entity_label2 == "布局":
                    spatial_arts.append("选址与空间布局", entity1, rel_type, rel, "布局", entity2)
                else:
                    pass
            elif entity_label1 == "装饰艺术": # ornamental_art
                rel_type = "包含"
                if entity_label2 == "纹样":
                    ornamental_arts.append("装饰艺术", entity1, rel_type, rel, "纹样", entity2)
                elif entity_label2 == "色彩":
                    ornamental_arts.append("装饰艺术", entity1, rel_type, rel, "色彩", entity2)
                elif entity_label2 == "工艺":
                    ornamental_arts.append("装饰艺术", entity1, rel_type, rel, "工艺", entity2)
                elif entity_label2 == "题材":
                    ornamental_arts.append("装饰艺术", entity1, rel_type, rel, "题材", entity2)
                else:
                    pass
            else:
                pass

        #return entity1s, rels, entity2s

    def create_node(self, label, nodes):
        """
        创建节点
        :param label: 标签
        :param nodes: 节点
        :return:
        """
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.graph.create(node)
            count += 1
            print(count, len(nodes))
        return

    def create_diseases_nodes(self, disease_info):
        """
        创建疾病节点的属性
        :param disease_info: list(Dict)
        :return:
        """
        count = 0
        for disease_dict in disease_info:
            node = Node("Disease", name=disease_dict['name'], age=disease_dict['age'],
                        infection=disease_dict['infection'], insurance=disease_dict['insurance'],
                        treatment=disease_dict['treatment'], checklist=disease_dict['checklist'],
                        period=disease_dict['period'], rate=disease_dict['rate'],
                        money=disease_dict['money'])
            self.graph.create(node)
            count += 1
            print(count)
        return

    def create_graphNodes(self):
        """
        创建知识图谱实体
        :return:
        """
        disease, symptom, alias, part, department, complication, drug, rel_alias, rel_symptom, rel_part, \
        rel_department, rel_complication, rel_drug, rel_infos = self.read_file()
        self.create_diseases_nodes(rel_infos)
        self.create_node("Symptom", symptom)
        self.create_node("Alias", alias)
        self.create_node("Part", part)
        self.create_node("Department", department)
        self.create_node("Complication", complication)
        self.create_node("Drug", drug)

        return

    def create_graphRels(self):
        disease, symptom, alias, part, department, complication, drug, rel_alias, rel_symptom, rel_part, \
        rel_department, rel_complication, rel_drug, rel_infos = self.read_file()

        self.create_relationship("Disease", "Alias", rel_alias, "ALIAS_IS", "别名")
        self.create_relationship("Disease", "Symptom", rel_symptom, "HAS_SYMPTOM", "症状")
        self.create_relationship("Disease", "Part", rel_part, "PART_IS", "发病部位")
        self.create_relationship("Disease", "Department", rel_department, "DEPARTMENT_IS", "所属科室")
        self.create_relationship("Disease", "Complication", rel_complication, "HAS_COMPLICATION", "并发症")
        self.create_relationship("Disease", "Drug", rel_drug, "HAS_DRUG", "药品")

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        """
        创建实体关系边
        :param start_node:
        :param end_node:
        :param edges:
        :param rel_type:
        :param rel_name:
        :return:
        """
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.graph.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return


import pandas as pd
from py2neo import Graph, Node, Relationship

# 连接到 Neo4j 数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "test"))

# 读取 CSV 数据（假设文件名为 data.csv）
df = pd.read_csv('neo4j_data/triples_no_duplicates.csv')
df.columns = ['Entity1', 'Relationship', 'Entity2', 'RelationshipProperty']
df = df.dropna(axis=0)

# 遍历每一行数据并创建图形
for index, row in df.iterrows():
    # 获取实体1、关系、实体2 和关系属性
    entity1 = row['Entity1']
    relationship = row['Relationship']
    entity2 = row['Entity2']
    relationship_property = row['RelationshipProperty']

    # 创建实体1和实体2的节点
    node1 = Node("Building1", name=entity1)  # 实体1是Person类型的节点
    node2 = Node("Building2", name=entity2)  # 实体2也是Person类型的节点

    # 将节点添加到图中，如果已经存在则跳过
    graph.merge(node1, "Building1", "name")
    graph.merge(node2, "Building2", "name")

    # 创建关系并设置属性
    rel = Relationship(node1, relationship, node2)
    rel[relationship] = relationship_property  # 设置关系属性

    # 将关系添加到图中
    graph.merge(rel)

print("数据已成功导入到 Neo4j 中！")

'''
if __name__ == "__main__":
    handler = BuildingGraph()
    handler.create_graphNodes()
    handler.create_graphRels()
'''


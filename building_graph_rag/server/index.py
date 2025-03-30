import os
import glob
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import DataFrameLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader as uwd
from langchain.document_loaders import UnstructuredPowerPointLoader as upp
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import server_config

def load_index():
    embed_model = HuggingFaceEmbeddings(model_name=server_config.M3E_BASE_MODEL)
    index_db = FAISS.load_local("index/building_rag.faiss", embed_model, allow_dangerous_deserialization=True)
    return index_db

def dump_index(filename):
    pass

def get_all_files_with_glob(root_dir):
    # 使用 glob 查找所有文件
    files = glob.glob(os.path.join(root_dir, '**'), recursive=True)
    
    # 过滤出文件（而非目录）
    files = [f for f in files if os.path.isfile(f)]
    
    return files

def txt_parser():
    files1 = glob.glob("docs/北京中轴线百科数据/*")
    files2 = get_all_files_with_glob("docs/北京中轴线论文数据")
    files3 = glob.glob("docs/raw_data.txt")
    file_list = files1 + files2 + files3
    documents = []
    for file in file_list:
        loader = TextLoader(file_path=file)
        docs = loader.load() # 返回文档对象列表
        documents.extend(docs)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 0,
        separators = ["\n\n", "\n", " ", ",", ".", "?"])

    all_splits = text_splitter.split_documents(documents)

    embedding = HuggingFaceEmbeddings(model_name="m3e-base")
    faiss_file = "building_rag.faiss"

    if not os.path.exists(faiss_file):
        index_db = FAISS.from_documents(all_splits, embedding)
        index_db.save_local(faiss_file)
    else:
        index_db = FAISS.load_local(faiss_file, embeddings = embedding)

if __name__ == "__main__":
    txt_parser()
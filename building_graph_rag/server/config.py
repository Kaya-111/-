class ServerConfig():
    # 大模型调用验证配置
    AK = "**************"
    SK = "*****************"
    ERNIE_SPEED_8K_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed?access_token="
    ERNIE_SPEED_128K_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token="
    ERNIE_LITE_8K_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token="
    ERNIE_TINY_8K_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-tiny-8k?access_token="


    # 语义模型地址
    #M3E_BASE_MODEL = "/User/mi/Desktop/graph_rag/building_graph_rag/server/m3e-base"
    M3E_BASE_MODEL = "/Users/mi/Desktop/graph_rag/building_graph_rag/server/m3e-base"

    # 日志配置相关
    log_path = "./log/"
    log_prefix = "paper_rag_"
    log_rotation = "14:30"
    log_retention = "15 days"
    log_encoding = "utf-8"
    log_backtrace = True
    log_diagnose = True

server_config = ServerConfig()

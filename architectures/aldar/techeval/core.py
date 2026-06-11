from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.aws.compute import Lambda
from diagrams.generic.storage import Storage
from diagrams.generic.network import Router
from diagrams.programming.framework import FastAPI
from diagrams.custom import Custom
from pathlib import Path

_ASSETS = Path(__file__).resolve().parent / "assets"
stack_icon = str(_ASSETS / "stack.png")

with Diagram(
    "Tech Eval Architecture",
    filename="tech_eval_architecture",
    show=True,
    direction="TB",
    graph_attr={
        "splines": "ortho",
        "nodesep": "1.0",
        "ranksep": "1.2",
        "pad": "0.5",
    },
):
    # ==========================================
    # Producer Layer
    # ==========================================
    producer = FastAPI("<<B>Producer</B>>")

    routing_exchange = Router("Routing Exchange")

    rabbitmq = RabbitMQ("RabbitMQ")

    producer >> routing_exchange >> rabbitmq

    # ==========================================
    # Queues
    # ==========================================
    rfp_queue = Storage("<<B>RFP Queue</B>>")
    eval_queue = Storage("Eval Queue")
    queue_state = Redis("Queue State")

    rabbitmq >> rfp_queue
    rabbitmq >> eval_queue
    rabbitmq >> queue_state

    # ==========================================
    # RFP Worker
    # ==========================================
    with Cluster("RFP Worker"):
        RFPworker = Custom("RFP Worker", stack_icon)
        rfp_embedding_1 = Lambda("Embedding")
        rfp_extractor_1 = Lambda("Extractor")
        rfp_downloader_1 = Lambda("Downloader")

    # ==========================================
    # RFP Worker N
    # ==========================================
    with Cluster("RFP Worker N"):
        rfp_embedding_n = Lambda("Embedding")
        rfp_extractor_n = Lambda("Extractor")
        rfp_downloader_n = Lambda("Downloader")

    # ==========================================
    # Evaluation Worker
    # ==========================================
    with Cluster("Evaluation Worker"):
        eval_embedding = Lambda("Embedding")
        eval_extractor = Lambda("Extractor")
        eval_downloader = Lambda("Downloader")

    # ==========================================
    # RFP Queue Connections
    # ==========================================
    rfp_queue >> rfp_embedding_1
    rfp_queue >> rfp_extractor_1
    rfp_queue >> rfp_downloader_1

    rfp_queue >> rfp_embedding_n
    rfp_queue >> rfp_extractor_n
    rfp_queue >> rfp_downloader_n

    # ==========================================
    # Evaluation Queue Connections
    # ==========================================
    eval_queue >> eval_embedding
    eval_queue >> eval_extractor
    eval_queue >> eval_downloader

    queue_state >> Edge(style="dashed") >> eval_extractor

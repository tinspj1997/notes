from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.compute import ComputeOptimizer
from diagrams.onprem.queue import Rabbitmq, RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.aws.database import RDS
from diagrams.aws.analytics import CloudsearchSearchDocuments


with Diagram("Tech Eval Architecture", show=False, direction="TB",outformat="jpg"):
    producer = ComputeOptimizer("Producer")
    RMQQueue = RabbitMQ("Rabbit MQ")

    with Cluster("Evaluation Worker"):
        eval_workers = [
             ECS("Embedding"),
                CloudsearchSearchDocuments("Extractor"),
                ECS("Downloader")
               ]
        
    with Cluster("RFP Worker"):
        rfp_workers = [
             ECS("Embedding"),
                ECS("Extractor"),
                ECS("Downloader")
               ]
        
        


    producer >> RMQQueue >> eval_workers
    producer >> RMQQueue >> rfp_workers
    RMQQueue >> Redis("Queue State")
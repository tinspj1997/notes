from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.compute import ComputeOptimizer
from diagrams.onprem.queue import Rabbitmq, RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.aws.database import RDS
from diagrams.aws.analytics import CloudsearchSearchDocuments
from diagrams.aws.network import ELB
from diagrams.aws.integration import SQS


with Diagram("Tech Eval Architecture", show=False, direction="TB",outformat="jpg"):
    producer = ComputeOptimizer("Producer")
    RMQQueue = RabbitMQ("Rabbit MQ")
    RoutingExchange = ELB("Routing Exchange")
    RFPQueue = SQS("RFP Queue")
    EvalQueue = SQS("Eval Queue")

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
        
        


    producer >> RoutingExchange >>RMQQueue >> EvalQueue >> eval_workers
    producer >> RoutingExchange >> RMQQueue >> RFPQueue >> rfp_workers
    RMQQueue >> Redis("Queue State")
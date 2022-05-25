import grpc
from concurrent import futures
import time

import logging

import insultor_pb2
import insultor_pb2_grpc

import insultor

class Insultor(insultor_pb2_grpc.InsultorServicer):
    
    def AddInsult(self, request, context):
        insultor.addInsult(request.name)
        return insultor_pb2.Empty()

    def GetInsults(self, request, context):
        insults = insultor_pb2.Array()
        insults.value.extend(insultor.getInsults())
        return insults
    
    def InsultMe(self, request, context):
        insult = insultor_pb2.String()
        insult.name = insultor.insultMe()
        return insult


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    insultor_pb2_grpc.add_InsultorServicer_to_server(Insultor(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
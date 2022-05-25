import logging

import grpc
import insultor_pb2
import insultor_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = insultor_pb2_grpc.InsultorStub(channel)

    request = insultor_pb2.String(name="puta")
    
    stub.AddInsult(request)
    

    request = insultor_pb2.Empty()
    

    response = stub.GetInsults(request)
    print("List of insults: ")
    print(response)
    

    response = stub.InsultMe(request)
    print("Insulting you: " + response.name)


if __name__ == '__main__':
    logging.basicConfig()
    run()
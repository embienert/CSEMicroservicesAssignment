import logging

import sys
import grpc
import demo_pb2
import demo_pb2_grpc

if __name__ == "__main__":
    # get port
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = "8080"

    #set server stub
    channel = grpc.insecure_channel('localhost:'+port)
    stub = demo_pb2_grpc.DiscountServiceStub(channel)

    #create requests
    req1S = demo_pb2.UpdateRequest(value = 3)
    req2S = demo_pb2.UpdateRequest(value = 300)

    testitem = demo_pb2.CartItem(product_id = 'testitem_001', quantity = 3)
    req1D = demo_pb2.DisRequest(items = [testitem])

    print("Sending Revenue Requests...")

    response = stub.UpdateSales(req1S)
    print(response.status)

    response = stub.UpdateSales(req2S)
    print(response.status)

    print("Sending Discount Requests...")

    response = stub.GetDiscount(req1D)
    print("Received Discount...")
    print(response.product_id)
    print(response.value)

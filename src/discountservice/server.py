from concurrent import futures
import logging
import time

import grpc
import demo_pb2
import demo_pb2_grpc


class Discount(demo_pb2_grpc.DiscountServiceServicer):

    def __init__(self, revenue):
        self.revenue = revenue

    def UpdateSales(self, request, context):
        val = request.value
        if val == 3.0:
            return demo_pb2.UpdateResponse(status=False)
        else:
            self.revenue = self.revenue + val
            print(self.revenue)
            return demo_pb2.UpdateResponse(status=True)

    def GetDiscount(self, request, context):
        # TODO: Handle empty cart
        # TODO: Random item from cart instead of first?

        cartitems = request.items
        pid = cartitems[0].product_id
        print("Discounted " + pid)
        return demo_pb2.DisResponse(product_id=pid, value=10)


def serve():
    port = '8080'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    service = Discount(0)
    demo_pb2_grpc.add_DiscountServiceServicer_to_server(service, server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    print("Server started, listening on " + port)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

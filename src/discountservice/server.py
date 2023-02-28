from concurrent import futures
import os
import time
import random

import googlecloudprofiler
import grpc
import demo_pb2
import demo_pb2_grpc

from logger import getJSONLogger

logger = getJSONLogger('discount_server')

class Discount(demo_pb2_grpc.DiscountServiceServicer):

    # track running revenue in internal variable
    def __init__(self, revenue, av, bp):
        self.revenue = revenue
        self.disAv = av
        self.disBreakpoint = bp
        random.seed()

    # SalesUpdate rpc communication
    def UpdateSales(self, request, context):
        val = request.value
        # if a negative value is passed return negative status response
        if val < 0:
            logger.info("received negative value")
            return demo_pb2.UpdateResponse(status=False)
        else:
            # update internal revenue tracker and return true status code
            self.revenue = self.revenue + val
            logger.info("updated revenue " + str(self.revenue))
            self.updateAvDiscount();
            return demo_pb2.UpdateResponse(status=True)

    # takes discountrequest als list of cart items
    # returns p_id of discounted item and discount value
    # if no discount is given returns p_id -1
    def GetDiscount(self, request, context):
        cartitems = request.items
        cartSize = len(cartitems)
        # Handle empty cart
        if cartSize <= 0:
            return demo_pb2.DisResponse(product_id='-1', value=0)
        #discounts random cart item by 5% if a discount is available
        if self.disAv:
            pid = random.choice(cartitems).product_id
            #print("Discounted " + pid)
            logger.info("discounted product " + pid)
            self.updateAvDiscount();
            return demo_pb2.DisResponse(product_id=pid, value=5)
        else:
            return demo_pb2.DisResponse(product_id='-1', value=0)

    def updateAvDiscount(self):
        if self.revenue > self.disBreakpoint:
            self.disAv = True
            self.revenue = self.revenue - self.disBreakpoint
            logger.info("discount available")
        self.disAv = True


def serve():
    logger.info("initializing discountservice")
    port = os.environ.get('PORT', "8080")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    service = Discount(revenue=0, av=False, bp=400)
    demo_pb2_grpc.add_DiscountServiceServicer_to_server(service, server)

    server.add_insecure_port('[::]:' + port)
    server.start()

    logger.info("listening on port: " + port)

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

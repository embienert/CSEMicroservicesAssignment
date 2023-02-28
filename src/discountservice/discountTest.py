import unittest
from server import Discount
import coverage

import sys
import grpc
import demo_pb2
import demo_pb2_grpc



class DiscountTest(unittest.TestCase):

    def testUpdateSales(self):
        service = Discount(revenue = 0, av =False, bp=400)
        #test updating ov value
        self.assertFalse(service.UpdateSales(request = demo_pb2.UpdateRequest(value=(-5)), context= True).status)
        self.assertTrue(service.UpdateSales(request = demo_pb2.UpdateRequest(value=3), context= True).status)
        #test updating of disAv
        self.assertTrue(service.UpdateSales(request = demo_pb2.UpdateRequest(value=399), context= True).status)
        testitem = demo_pb2.CartItem(product_id='testitem_001', quantity=3)
        self.assertEqual(5,service.GetDiscount(request= demo_pb2.DisRequest(items=[testitem]), context=True).value)

    def testGetDiscount(self):
        service = Discount(revenue = 0, av =False, bp=400)
        testitem = demo_pb2.CartItem(product_id='testitem_001', quantity=3)
        #test empty cart
        self.assertEqual('-1',service.GetDiscount(request= demo_pb2.DisRequest(items=[]), context=True).product_id)

        #test no available discount
        self.assertEqual('-1',service.GetDiscount(request= demo_pb2.DisRequest(items=[testitem]), context=True).product_id)

        #test available discount
        service.UpdateSales(request = demo_pb2.UpdateRequest(value=600), context= True)
        self.assertEqual(5,service.GetDiscount(request= demo_pb2.DisRequest(items=[testitem]), context=True).value)

    def testMultipleDiscounts(self):
        service = Discount(revenue = 0, av =False, bp=400)
        testitem = demo_pb2.CartItem(product_id='testitem_001', quantity=3)
        #adds enough revenue for multiple discounts
        service.UpdateSales(request = demo_pb2.UpdateRequest(value=900), context= True)
        #try for multiple discounts
        self.assertEqual(5,service.GetDiscount(request= demo_pb2.DisRequest(items=[testitem]), context=True).value)
        self.assertEqual(5,service.GetDiscount(request= demo_pb2.DisRequest(items=[testitem]), context=True).value)

    def testMultipleInputs(self):
        service = Discount(revenue = 0, av =False, bp=400)
        testitem1 = demo_pb2.CartItem(product_id='testitem_001', quantity=3)
        testitem2 = demo_pb2.CartItem(product_id='testitem_002', quantity=1)
        testitem3 = demo_pb2.CartItem(product_id='testitem_003', quantity=1)
        service.UpdateSales(request = demo_pb2.UpdateRequest(value=900), context= True)
        self.assertEqual(5,service.GetDiscount(request= demo_pb2.DisRequest(items=[testitem1,testitem2, testitem3]), context=True).value)

if __name__ == '__main__':

  unittest.main()


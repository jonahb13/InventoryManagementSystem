import grpc
import InventorySystem_pb2
import InventorySystem_pb2_grpc
import xmlrpc.client
import time
import string
import random
import statistics

with grpc.insecure_channel('3.17.130.209:50051') as channel:   
    stub = InventorySystem_pb2_grpc.InventorySystemStub(channel) 

    manufacturers = ['Rio Dan','Jonah', 'jeff','CS dep','moravian food','Pepsi','Mac','KFC M','NY street','Pepsico Inc.',
        '1st in the line Co.','Kraft Foods Inc.','General Electric','fastFood','Tyson Foods Inc.']

    for i in range(500):
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
        start = time.monotonic()
        wholesale = random.uniform(0.10, 70.99)
        response = stub.addNewProduct(InventorySystem_pb2.Product(
            name=name, 
            description=''.join(random.choices(string.ascii_uppercase + string.digits, k = 40)), 
            manufacturer=random.choices(manufacturers)[0], 
            wholesale_cost=wholesale, 
            sale_cost=random.uniform(wholesale, wholesale + 14.99), 
            stock=random.randint(100, 200)
        ))
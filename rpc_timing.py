import grpc
import InventorySystem_pb2
import InventorySystem_pb2_grpc
import xmlrpc.client
import time
import string
import random
import statistics

def main():

    # Dictionaries to store times
    grpc_times = {"Add Product" : [], "Get Product" : [], "Manufacturer" : [], "Update Product" : [], "Get In-stock" : [],
        "Get All" : [], "Create Order" : [], "Get Order" : [], "Amend Order" : [], "Unpaid/Unshipped" : []}
    xmlrpc_times = {"Add Product" : [], "Get Product" : [], "Manufacturer" : [], "Update Product" : [], "Get In-stock" : [],
        "Get All" : [], "Create Order" : [], "Get Order" : [], "Amend Order" : [], "Unpaid/Unshipped" : []}

    # Searching information
    names_to_id = {}
    order_ids = {}
    manufacturers = ['Rio Dan','Jonah', 'jeff','CS dep','moravian food','Pepsi','Mac','KFC M','NY street','Pepsico Inc.',
        '1st in the line Co.','Kraft Foods Inc.','General Electric','fastFood','Tyson Foods Inc.']

    # # gRPC timing
    # with grpc.insecure_channel('3.17.130.209:50051') as channel:   
    #     stub = InventorySystem_pb2_grpc.InventorySystemStub(channel) 

    #     # Initial start time
    #     initial_start = time.monotonic()

    #     # Add product 
    #     for i in range(200):
    #         name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 20))
    #         wholesale = random.uniform(0.10, 70.99)
    #         start = time.monotonic()
    #         response = stub.addNewProduct(InventorySystem_pb2.Product(
    #             name=name, 
    #             description=''.join(random.choices(string.ascii_uppercase + string.digits, k = 40)), 
    #             manufacturer=random.choices(manufacturers)[0], 
    #             wholesale_cost=wholesale, 
    #             sale_cost=random.uniform(wholesale, wholesale + 14.99), 
    #             stock=random.randint(100, 200)
    #         ))
    #         grpc_times["Add Product"].append(time.monotonic() - start)
    #         names_to_id[name] = str(response).split(" ")[1][1:-2]

    #     # Get product
    #     for i in range(100):
    #         start = time.monotonic()
    #         response = stub.getProduct(InventorySystem_pb2.ProductQuery(product_id="-2", product_name=random.choices(list(names_to_id.keys()))[0]))
    #         grpc_times["Get Product"].append(time.monotonic() - start)

    #     # Get manufacturer products
    #     for i in range(50):
    #         start = time.monotonic()
    #         response = stub.getManufacturerProducts(InventorySystem_pb2.Manufacturer(manufacturer=random.choices(manufacturers)[0]))
    #         grpc_times["Manufacturer"].append(time.monotonic() - start)

    #     # Update a product
    #     for i in range(50):
    #         random_name = random.choices(list(names_to_id.keys()))[0]
    #         wholesale = random.uniform(0.10, 70.99)
    #         start = time.monotonic()
    #         response = stub.updateProduct(InventorySystem_pb2.Product(
    #             id_=names_to_id[random_name], 
    #             name=random_name, 
    #             description=''.join(random.choices(string.ascii_uppercase + string.digits, k = 27)),
    #             manufacturer=random.choices(manufacturers)[0], 
    #             wholesale_cost=wholesale, 
    #             sale_cost=random.uniform(wholesale, wholesale + 14.99), 
    #             stock=random.randint(100, 200)
    #         ))
    #         grpc_times["Update Product"].append(time.monotonic() - start)

    #     # Get in-stock products
    #     for i in range(50):
    #         start = time.monotonic()
    #         response = stub.getInStockProducts(InventorySystem_pb2.Empty())
    #         grpc_times["Get In-stock"].append(time.monotonic() - start)

    #     # Get all products
    #     for i in range(50):
    #         start = time.monotonic()
    #         response = stub.getAllProducts(InventorySystem_pb2.Empty())
    #         grpc_times["Get All"].append(time.monotonic() - start)

    #     # Create an order
    #     for i in range(50):
    #         product_list = []
    #         products = {}
    #         for i in range(random.randint(1, 5)):
    #             name = random.choices(list(names_to_id))[0]
    #             stock = random.randint(1, 5)
    #             product_list += ([InventorySystem_pb2.Product(name=name, stock=stock)])
    #             products[name] = stock
    #         start = time.monotonic()
    #         response = stub.createOrder(InventorySystem_pb2.Order(
    #             destination=''.join(random.choices(string.ascii_uppercase + string.digits, k = 20)), 
    #             date=str(random.randint(5, 12)) + "/" + str(random.randint(1, 30)) + "/" + str(2020),
    #             products=product_list,
    #             is_paid=random.choices([True, False])[0], 
    #             is_shipped=random.choices([True, False])[0]
    #         ))
    #         grpc_times["Create Order"].append(time.monotonic() - start)
    #         id_ = str(response).split(" ")[1][1:-2]
    #         order_ids[id_] = products

    #     # Get an order
    #     for i in range(50):
    #         start = time.monotonic()
    #         response = stub.getOrder(InventorySystem_pb2.OrderID(value=random.choices(list(order_ids.keys()))[0]))
    #         grpc_times["Get Order"].append(time.monotonic() - start)

    #     # Amend an order
    #     for i in range(100):
    #         id_ = random.choices(list(order_ids.keys()))[0]
    #         add_products = []
    #         for i in range(random.randint(0, 3)):
    #             add_products += [InventorySystem_pb2.Product(name=random.choices(list(names_to_id.keys()))[0], stock=random.randint(1, 4))]
    #         remove_products = []
    #         for i in range(random.randint(0, 2)):
    #             remove_products += ([InventorySystem_pb2.Product(name=random.choices(list(order_ids[id_]))[0], stock=random.randint(1, 2))])
    #         start = time.monotonic()
    #         response = stub.amendOrder(InventorySystem_pb2.UpdateOrder(
    #             id_=id_, 
    #             destination=''.join(random.choices(string.ascii_uppercase + string.digits, k = 20)),
    #             date=str(random.randint(5, 12)) + "/" + str(random.randint(1, 30)) + "/" + str(2020),
    #             add_products=add_products, 
    #             remove_products = remove_products,
    #             is_paid=random.choices([True, False])[0], 
    #             is_shipped=random.choices([True, False])[0]
    #         ))
    #         grpc_times["Amend Order"].append(time.monotonic() - start)

    #     # Unshipped/unpaid orders 
    #     for i in range(50):
    #         start = time.monotonic()
    #         response = stub.getUnshippedAndOrUnpaidOrders(InventorySystem_pb2.UnshippedAndOrUnpaidQuery(
    #             query_unshipped=random.choices([True, False])[0], query_unpaid=random.choices([True, False])[0]))
    #         grpc_times["Unpaid/Unshipped"].append(time.monotonic() - start)

    #     # Print total time for gRPC
    #     print("Total time for gRPC:", time.monotonic() - initial_start)
    #     print("Median times by RPC call:")
    #     for key, value in grpc_times.items():
    #         print("   " + key + ": " + str(statistics.median(value)))
            

    # XML-RPC timing
    with xmlrpc.client.ServerProxy("http://3.17.130.209:50052/", allow_none=True) as proxy:

        # Initial start time
        initial_start = time.monotonic()

        # Add product
        for i in range(50):
            name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            wholesale = random.uniform(0.10, 70.99)
            start = time.monotonic()
            description = ''.join(random.choices(string.ascii_uppercase + string.digits, k=40))
            manufacturer = random.choices(manufacturers)[0]
            wholesale_cost = wholesale
            sale_cost = random.uniform(wholesale, wholesale + 14.99)
            stock = random.randint(100, 200)
            result = proxy.add_new_product(name, description, manufacturer, wholesale_cost, sale_cost, stock)
            names_to_id[name] = str(result).split(" ")[1][1:-2]
            xmlrpc_times["Add Product"].append(time.monotonic() - start)

        # Get product
        for i in range(10):
            start = time.monotonic()
            result = proxy.get_product("-2", random.choices(list(names_to_id.keys()))[0])
            xmlrpc_times["Get Product"].append(time.monotonic() - start)

        # Get manufacturer products
        for i in range(10):
            start = time.monotonic()
            result = proxy.get_manufacturer_products(random.choices(manufacturers))
            xmlrpc_times["Manufacturer"].append(time.monotonic() - start)

        # Update a product
        for i in range(10):
            random_name = random.choices(list(names_to_id.keys()))[0]
            wholesale = random.uniform(0.10, 70.99)
            start = time.monotonic()
            id_=names_to_id[random_name]
            name=random_name
            description=''.join(random.choices(string.ascii_uppercase + string.digits, k=27))
            manufacturer=random.choices(manufacturers)[0]
            wholesale_cost=wholesale
            sale_cost=random.uniform(wholesale, wholesale + 14.99)
            stock=random.randint(100, 200)
            result = proxy.update_product(id_, name, description, manufacturer, wholesale_cost, sale_cost, stock)
            xmlrpc_times["Update Product"].append(time.monotonic() - start)

        # Get in-stock products
        for i in range(15):
            start = time.monotonic()
            result = proxy.get_instock_products()
            xmlrpc_times["Get In-stock"].append(time.monotonic() - start)

        # Get all products
        for i in range(15):
            start = time.monotonic()
            result = proxy.get_all_products()
            xmlrpc_times["Get All"].append(time.monotonic() - start)

        # Create an order
        for i in range(10):
            products = {}
            for i in range(random.randint(1, 5)):
                name = random.choices(list(names_to_id))[0]
                stock = random.randint(1, 5)
                products[name] = stock
            start = time.monotonic()
            destination=''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            date=str(random.randint(5, 12)) + "/" + str(random.randint(1, 30)) + "/" + str(2020)
            is_paid=random.choices([True, False])[0]
            is_shipped=random.choices([True, False])[0]
            result = proxy.create_order(destination, date, products, is_paid, is_shipped)
            id_ = str(result).split(" ")[1][1:-2]
            order_ids[id_] = products
            xmlrpc_times["Create Order"].append(time.monotonic() - start)

        # Get an order
        for i in range(10):
            start = time.monotonic()
            response = proxy.get_order(random.choices(list(order_ids.keys()))[0])
            xmlrpc_times["Get Order"].append(time.monotonic() - start)

        # Amend an order
        for i in range(10):
            id_ = random.choices(list(order_ids.keys()))[0]
            add_products = {}
            for i in range(random.randint(0, 3)):
                add_products[random.choices(list(names_to_id.keys()))[0]] = random.randint(1, 4)
            remove_products = {}
            for i in range(random.randint(0, 2)):
                remove_products[random.choices(list(order_ids[id_]))[0]] = random.randint(1, 2)
            start = time.monotonic()
            id_=id_
            destination=''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
            date=str(random.randint(5, 12)) + "/" + str(random.randint(1, 30)) + "/" + str(2020)
            is_paid=random.choices([True, False])[0]
            is_shipped=random.choices([True, False])[0]
            result = proxy.amend_order(id_,destination,date,add_products,remove_products,is_paid,is_shipped)
            xmlrpc_times["Amend Order"].append(time.monotonic() - start)

        # Unshipped/unpaid orders
        for i in range(10):
            start = time.monotonic()
            result = proxy.get_unshipped_unpaid_orders(random.choices([True, False])[0],random.choices([True, False])[0])
            xmlrpc_times["Unpaid/Unshipped"].append(time.monotonic() - start)

        # Print total time for gRPC
        print("Total time for XML-RPC:", time.monotonic() - initial_start)
        print("Median times by RPC call:")
        for key, value in xmlrpc_times.items():
            print("   " + key + ": " + str(statistics.median(value)))

if __name__ == '__main__':    
    main()

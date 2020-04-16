"""
Project 02 - RPCs
gRPC Client
Jonah Beers and Riyad Alghamdi 
"""
import grpc
import InventorySystem_pb2
import InventorySystem_pb2_grpc

class ClientgRPC():

    def add_product(self, stub, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        try:
            response = stub.addNewProduct(InventorySystem_pb2.Product(name=name, description=description, 
                manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, stock=stock))
        except grpc.RpcError as e:
            print(e.details())
        else:
            print("New product's ID:", str(response).split(" ")[1][1:-2], end="\n\n")


    def get_product(self, stub, id_, name):
        try:
            response = stub.getProduct(InventorySystem_pb2.ProductQuery(product_id=id_, product_name=name))
        except grpc.RpcError as e:
            print(e.details())
        else:
            print(response)


    def get_manufacturer_products(self, stub, manufacturer):
        response = stub.getManufacturerProducts(InventorySystem_pb2.Manufacturer(manufacturer=manufacturer))
        for product in response:
            print(product)


    def update_product(self, stub, id_, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        try:
            response = stub.updateProduct(InventorySystem_pb2.Product(id_=id_, name=name, description=description,
                manufacturer=manufacturer, wholesale_cost=wholesale_cost, sale_cost=sale_cost, stock=stock))
        except grpc.RpcError as e:
            print(e.details())
        else:
            print(str(response).split(": ", 1)[1][1:-2], end="\n\n")


    def get_instock_items(self, stub):
        response = stub.getInStockProducts(InventorySystem_pb2.Empty())
        for product in response:
            print(product)


    def get_all_products(self, stub):
        response = stub.getAllProducts(InventorySystem_pb2.Empty())
        for product in response:
            print(product)


    def create_order(self, stub, destination, date, product_list, is_paid, is_shipped):
        temp_list = []
        for product, stock in product_list:
            temp_list += [InventorySystem_pb2.Product(name=product, stock=int(stock))]

        try:
            response = stub.createOrder(InventorySystem_pb2.Order(destination=destination, date=date,
                products=temp_list,is_paid=is_paid, is_shipped=is_shipped))
        except grpc.RpcError as e:
            print(e.details())
        else:
            print("New order's ID:", str(response).split(" ")[1][1:-2], end="\n\n")


    def get_order(self, stub, order_id):
        try:
            response = stub.getOrder(InventorySystem_pb2.OrderID(value=order_id))
        except grpc.RpcError as e:
            print(e.details())
        else:
            print(response, end="\n\n")


    def amend_order(self, stub, id_, destination, date, add_products, remove_products, is_paid, is_shipped):
        added_temp_list = []
        if not add_products:
            add_products = added_temp_list
        for product_added, stock in add_products:
            added_temp_list += [InventorySystem_pb2.Product(name=product_added, stock=int(stock))]

        removed_temp_list = []
        if not remove_products:
            remove_products = removed_temp_list
        for product_removed, stock in remove_products:
            removed_temp_list += [InventorySystem_pb2.Product(name=product_removed, stock=int(stock))]
        try:
            response = stub.amendOrder(InventorySystem_pb2.UpdateOrder(id_=id_, destination=destination,
                date=date,add_products=added_temp_list, remove_products = removed_temp_list,
                is_paid=is_paid, is_shipped=is_shipped))
        except grpc.RpcError as e:
            print(e.details())
        else:
            print(str(response).split(" ", 1)[1][1:-2], end="\n\n")


    def get_unshipped_and_or_unpaid_orders(self, stub, query_unshipped, query_unpaid):
        response = stub.getUnshippedAndOrUnpaidOrders(InventorySystem_pb2.UnshippedAndOrUnpaidQuery(
            query_unshipped=query_unshipped, query_unpaid=query_unpaid))
        if query_unshipped and query_unpaid:
            print("Unshipped and Unpaid Orders:", end="\n\n")
        if query_unshipped:
            print("Unshipped Orders:", end="\n\n")
        if query_unpaid:
            print("Unpaid Orders:", end="\n\n")
        for order in response:
                print(order)
        


"""
Project 02 - RPCs
Server containing gRPC and XML-RPC classes/methods.
Jonah Beers and Riyad Alghamdi 
"""
import uuid
import grpc
import pickle
import InventorySystem_pb2
import InventorySystem_pb2_grpc
import InventorySystemFunctions as helpers
from xmlrpc.server import SimpleXMLRPCServer
from concurrent import futures

class InventorySystemManager(InventorySystem_pb2_grpc.InventorySystemServicer):

    def getProductRPCMessage(self, product):
        product = helpers.get_product_from_DB(product)
        return InventorySystem_pb2.Product(id_=product["id"], name=product["name"], description=product["description"],
                                                manufacturer=product["manufacturer"], wholesale_cost=product["wholesale_cost"],
                                                sale_cost=product["sale_cost"], stock=product["stock"]) 
    
    def addNewProduct(self, request, context):
        id_ = helpers.add_product(request.name, request.description, request.manufacturer, request.wholesale_cost, 
            request.sale_cost, request.stock)
        if id_ == -1:
            context.set_details("Invalid name '" + request.name + "': this product already exists!")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return InventorySystem_pb2.ProductID() 
        return InventorySystem_pb2.ProductID(product_id=id_)

    def getProduct(self, request, context):
        product = helpers.get_product(request.product_id, request.product_name)
        if product == -1 or product == -2:
            if product == -2:
                context.set_details("Must provide a product ID or name.")
            else:
                context.set_details("The product you are searching for does not exist!")
            context.set_code(grpc.StatusCode.UNKNOWN)
            return InventorySystem_pb2.Product() 
        return self.getProductRPCMessage(product)

    def updateProduct(self, request, context):
        description = request.description
        manufacturer = request.manufacturer
        product_updated = helpers.update_product((request.id_, request.name), description, manufacturer,
                        request.wholesale_cost, request.sale_cost, request.stock)
        if product_updated:
            return InventorySystem_pb2.UpdateResult(result="Product has been successfully updated!")
        return InventorySystem_pb2.UpdateResult(result="Failure to update product: make sure both ID and name are correct.")

    def getManufacturerProducts(self, request, context):
        products = helpers.get_manufacturer_products(request.manufacturer)
        for product in products:
            yield InventorySystem_pb2.Product(id_=product["id"], name=product["name"], description=product["description"],
                                                manufacturer=product["manufacturer"], wholesale_cost=product["wholesale_cost"],
                                                sale_cost=product["sale_cost"], stock=product["stock"]) 

    def getAllProducts(self, request, context):
        products = helpers.get_all_products()
        for product in products:
            yield InventorySystem_pb2.Product(id_=product["id"], name=product["name"], description=product["description"],
                                                manufacturer=product["manufacturer"], wholesale_cost=product["wholesale_cost"],
                                                sale_cost=product["sale_cost"], stock=product["stock"]) 

    def getInStockProducts(self, request, context):
        products = helpers.get_instock_products()
        for product in products:
            yield InventorySystem_pb2.ProductCount(product_id=product["id"], product_name=product["name"], 
                                                    quantity=product["stock"])

    def createOrder(self, request, context):
        products = {}
        for product in request.products:
            products[product.name] = product.stock
        id_, message = helpers.create_order(request.destination, request.date, products, request.is_paid, request.is_shipped)
        if id_ == -1:
            context.set_details(message)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return InventorySystem_pb2.OrderID()
        elif id_ == -2:
            context.set_details(message)
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return InventorySystem_pb2.OrderID()
        return InventorySystem_pb2.OrderID(value=id_)

    def getOrder(self, request, context):
        order, message = helpers.get_order(request.value)
        products = []
        if order == -1:
            context.set_details(message)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return InventorySystem_pb2.Order()
        for product, stock in order["ordered_products"].items():
            products.append(InventorySystem_pb2.Product(name=product, stock=stock))
        return InventorySystem_pb2.Order(id_=order["id"], destination=order["destination"], date=order["date"], products=products, 
                                        is_paid=order["is_paid"], is_shipped=order["is_shipped"])

    def amendOrder(self, request, context):
        destination = request.destination
        date = request.date

        add_products = {}
        if request.add_products:
            for product in request.add_products:
                add_products[product.name] = product.stock
        remove_products = {}
        if request.remove_products:
            for product in request.remove_products:
                remove_products[product.name] = product.stock
        result = helpers.amend_order(request.id_, destination, date, add_products, remove_products, request.is_paid,
                request.is_shipped)
        return InventorySystem_pb2.UpdateResult(result=result)

    def getUnshippedAndOrUnpaidOrders(self, request, context):
        orders = helpers.get_unshipped_unpaid_orders(request.query_unshipped, request.query_unpaid)
        for order in orders:
            products = []
            for product, stock in order["ordered_products"].items():
                products.append(InventorySystem_pb2.Product(name=product, stock=stock))
            yield InventorySystem_pb2.Order(id_=order["id"], destination=order["destination"], date=order["date"], products=products, 
                                        is_paid=order["is_paid"], is_shipped=order["is_shipped"])


class XMLRPCInventorySystemManager():

    def create_product_string(self, id_, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        return "\nID: " + id_ + "\nName: " + name + "\nDescription: " + description \
                        + "\nManufacturer: " + manufacturer + "\nWholesale Cost: " + str(wholesale_cost) \
                        + "\nSale Cost: " + str(sale_cost) + "\nStock: " + str(stock) + "\n"

    def create_order_string(self, id_, destination, date, products, is_paid, is_shipped):
        product_list = ""
        for product, stock in products.items():
            product_list += product + " - " + str(stock) + ", "
        product_list = product_list[:-2]
        is_shipped_string = "No"
        is_paid_string = "No"
        if is_shipped:
            is_shipped_string = "Yes"
        if is_paid:
            is_paid_string = "Yes"
        return "\nID: " + id_ + "\nDestination: " + destination + "\nDate: " + date + "\nProducts: " \
            + product_list + "\nPaid? " + is_paid_string + "\nShipped? " + is_shipped_string + "\n"
    
    def add_new_product(self, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        """
        Takes name (string), description (string), manufacturer (string), wholesale cost (float), 
        sale cost (float), and stock (integer) as parameters. Returns an error message (as a string) 
        if name exists in the DB, otherwise the ID is returned with a message (as a string). 
        """
        id_ = helpers.add_product(name, description, manufacturer, wholesale_cost, sale_cost, stock)
        if id_ == -1:
            return "\nInvalid name '" + name + "': this product already exists!\n"
        return "\nNew product's ID: " + id_ + "\n"

    def get_product(self, id_, name):
        """
        Takes ID (string) and name (string) as parameters. If both are the default values or if either
        the ID or name is wrong, then an error message is returned (as a string). Otherwise, the id (string)
        name (string), description (string), manufacturer (string), wholesale cost (float), sale cost (float) 
        and stock (integer) are send to a to string function and returned (as a string).
        """
        product = helpers.get_product(id_, name)
        if product == -1 or product == -2:
            if product == -2:
                return "\nMust provide a product ID or name.\n"
            return "\nThe product you are searching for does not exist!\n"
        return self.create_product_string(product.id_, product.name, product.description, product.manufacturer, 
            product.wholesale_cost, product.sale_cost, product.stock)
        
    def update_product(self, id_, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        """
        Takes ID (string), name (string), description (string), manufacturer (string), wholesale_cost (float), 
        sale_cost (float), and stock (integer) as parameters. These parameters are sent to a helper function, 
        a boolean value is checked. If product was updated, a success message is returned (as a string). 
        Otherwise, an error message is returned (as a string).
        """
        product_updated = helpers.update_product((id_, name), description, manufacturer,
                        wholesale_cost, sale_cost, stock)
        if product_updated:
            return "\nProduct has been successfully updated!\n"
        return "\nFailure to update product: make sure both ID and name are correct.\n"

    def get_manufacturer_products(self, manufacturer):
        """
        Takes manufacturer (string) as a parameter. This gets sent to a helper function and a list of product 
        dictionaries are returned that have the specified manufacturer. Each product's attributes are sent to 
        a to string method and that string is appended to a list. This list is then returned. 
        """
        product_list = []
        products = helpers.get_manufacturer_products(manufacturer)
        for product in products:
            product_list.append(self.create_product_string(product["id"], product["name"], product["description"], product["manufacturer"], 
                product["wholesale_cost"], product["sale_cost"], product["stock"]))
        return product_list

    def get_all_products(self):
        """
        This calls a helper function that gets a list of all product dictionaries. Each product's attributes are 
        sent to a to string method and that string is appended to a list. This list is then returned. 
        """
        product_list = []
        products = helpers.get_all_products()
        for product in products:
            product_list.append(self.create_product_string(product["id"], product["name"], product["description"], product["manufacturer"], 
                product["wholesale_cost"], product["sale_cost"], product["stock"]))
        return product_list

    def get_instock_products(self):
        """
        This calls a helper function that gets a list of product dictionaries that have stock. Each product's 
        attributes are sent to a to string method and that string is appended to a list. This list is then returned. 
        """
        product_list = []
        products = helpers.get_instock_products()
        for product in products:
            product_list.append("\nID: " + product["id"] + "\nName: " + product["name"] + "\nStock: " + str(product["stock"]) + "\n")
        return product_list

    def create_order(self, destination, date, products, is_paid, is_shipped):
        """
        Takes destination (string), date (string), products (dictionary of product : quantity)
        is_paid (boolean), and is_shipped (boolean) as parameters. These are sent to a helper 
        function that creates the order and returns an ID and message. If some error occured 
        when creating the order, the message is returned. Otherwise, the new ID is returned. 
        """
        id_, message = helpers.create_order(destination, date, products, is_paid, is_shipped)
        if id_ == -1 or id_ == -2:
            return "\n" + message + "\n"
        return "\nNew order's ID: " + id_ + "\n"

    def get_order(self, id_):
        """ 
        Takes order ID (string) as a parameter. This is passed to a helper function and the
        order and message is returned. If an error occured, then the message is returned 
        (as a string). Otherwise, the order is sent to a to string method and returns the string.
        """
        order, message = helpers.get_order(id_)
        if order == -1:
            return "\n" + message + "\n"
        return self.create_order_string(order["id"], order["destination"], order["date"], order["ordered_products"],
                order["is_paid"], order["is_shipped"])        

    def amend_order(self, id_, destination, date, add_products, remove_products, is_paid, is_shipped):
        """
        Takes ID (string), destination (string), date (string), products to add (dictionary), 
        products to remove (dictionary), is paid (boolean), and is shipped (boolean) as parameters. 
        These are sent to a helper function and a result (if update was successful or not) is returned 
        as a string.
        """
        result = helpers.amend_order(id_, destination, date, add_products, remove_products, is_paid, is_shipped)
        return "\n" + result + "\n"

    def get_unshipped_unpaid_orders(self, query_unshipped, query_unpaid):
        """
        Takes unshipped query (boolean) and unpaid query (boolean) as parameters. These are passed
        to a helper function to get the orders with the desired shipped/paid status. These orders
        are sent to a to string method and appended to a list and returned (as list of strings).
        """
        orders = helpers.get_unshipped_unpaid_orders(query_unshipped, query_unpaid)
        order_list = []
        for order in orders:
            order_list.append(self.create_order_string(order["id"], order["destination"], order["date"], 
                order["ordered_products"], order["is_paid"], order["is_shipped"]))
        return order_list


def main():
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    InventorySystem_pb2_grpc.add_InventorySystemServicer_to_server(InventorySystemManager(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    with SimpleXMLRPCServer(("", 50052)) as xmlrpc_server:
        xmlrpc_server.register_introspection_functions()
        xmlrpc_server.register_multicall_functions()
        xmlrpc_server.register_instance(XMLRPCInventorySystemManager())
        try:
            try:
                helpers.read_file()
            except EOFError:
                print("Inventory System database is empty.")
            except FileNotFoundError:
                print("Inventory System database does not exist, so one will be created.")
            xmlrpc_server.serve_forever()
            grpc_server.wait_for_termination()
        except KeyboardInterrupt:
            helpers.save_file()


if __name__ == '__main__':
    main()
"""
Project 02 - RPCs
XML-RPC Client
Jonah Beers and Riyad Alghamdi 
"""

class ClientXMLRPC():

    def add_product(self, proxy, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        try:
            result = proxy.add_new_product(name, description, manufacturer, wholesale_cost, sale_cost, stock)
            print(result)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def get_product(self, proxy, id_, name):
        try:
            result = proxy.get_product(id_, name)
            print(result)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def update_product(self, proxy, id_, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        try:
            result = proxy.update_product(id_, name, description, manufacturer, wholesale_cost, sale_cost, stock)
            print(result)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def get_manufacturer_products(self, proxy, manufacturer):
        try:
            result = proxy.get_manufacturer_products(manufacturer)
            for product in result:
                print(product)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def get_all_products(self, proxy):
        try:
            result = proxy.get_all_products()
            for product in result:
                print(product)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def get_instock_products(self, proxy):
        try:
            result = proxy.get_instock_products()
            for product in result:
                print(product)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def create_order(self, proxy, destination, date, products, is_paid, is_shipped):
        try:
            ordered_products = {}
            for product in products:
                ordered_products[product[0]] = int(product[1])
            result = proxy.create_order(destination, date, ordered_products, is_paid, is_shipped)
            print(result)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def get_order(self, proxy, id_):
        try:
            result = proxy.get_order(id_)
            print(result)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


    def amend_order(self, proxy, id_, destination, date, add_products, remove_products, is_paid, is_shipped):
        try:
            products_to_add = {}
            products_to_remove = {}
            for product in add_products:
                products_to_add[product[0]] = int(product[1])
            for product in remove_products:
                products_to_remove[product[0]] = int(product[1])
            result = proxy.amend_order(id_, destination, date, products_to_add, products_to_remove, is_paid, is_shipped)
            print(result)
        except Exception as e:
            print(e)
            print("\nError occured while accessing the Inventory System.\n")


    def get_unshipped_unpaid_orders(self, proxy, query_unshipped, query_unpaid):
        try:
            result = proxy.get_unshipped_unpaid_orders(query_unshipped, query_unpaid)
            for order in result:
                print(order)
        except Exception:
            print("\nError occured while accessing the Inventory System.\n")


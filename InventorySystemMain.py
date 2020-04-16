"""
Project 02 - RPCs
Main Client: Argparse and Client Selector
Jonah Beers and Riyad Alghamdi 
"""
import argparse
import grpc
from InventorySystem_gRPC_Client import ClientgRPC
import InventorySystem_pb2_grpc
from InventorySystem_XMLRPC_Client import ClientXMLRPC
import xmlrpc.client

def parse_grpc(args):
    """
    Function is called if user wants to connect to 
    server using gRPC. Calls gRPC methods based off 
    other arguments provided in the command line.
    """
    with grpc.insecure_channel('3.17.130.209:50051') as channel:        
        stub = InventorySystem_pb2_grpc.InventorySystemStub(channel) 
        client = ClientgRPC()
        if args.rpc == 'add_product':
            client.add_product(stub, args.name, args.description, args.manufacturer,
                        args.wholesale_cost, args.sale_cost, args.stock)
        if args.rpc == 'get_product':
            client.get_product(stub, args.product_id, args.name)
        if args.rpc == 'get_manufacturer_products':
            client.get_manufacturer_products(stub, args.manufacturer)
        if args.rpc == 'update_product':
            client.update_product(stub, args.id, args.name, args.description, args.manufacturer,
                        args.wholesale_cost, args.sale_cost, args.stock)
        if args.rpc == 'get_instock':
            client.get_instock_items(stub)
        if args.rpc == 'get_all':
            client.get_all_products(stub)
        if args.rpc == 'create_order':
            client.create_order(stub, args.destination, args.date, args.product_list, args.paid, args.shipped)
        if args.rpc == 'get_order':
            client.get_order(stub, args.id)
        if args.rpc == 'amend_order':
            client.amend_order(stub, args.id, args.destination, args.date, args.add_products, args.remove_products,
                        args.paid, args.shipped)
        if args.rpc == 'orders_status':
            client.get_unshipped_and_or_unpaid_orders(stub, args.unshipped, args.unpaid)

def parse_xmlrpc(args):
    """
    Function is called if user wants to connect to 
    server using XML-RPC. Calls XML-RPC methods based 
    off other arguments provided in the command line.
    """
    with xmlrpc.client.ServerProxy("http://3.17.130.209:50052/", allow_none=True) as proxy:
        client = ClientXMLRPC()
        if args.rpc == 'add_product':
            client.add_product(proxy, args.name, args.description, args.manufacturer,
                        args.wholesale_cost, args.sale_cost, args.stock)
        if args.rpc == 'get_product':
            client.get_product(proxy, args.product_id, args.name)
        if args.rpc == 'get_manufacturer_products':
            client.get_manufacturer_products(proxy, args.manufacturer)
        if args.rpc == 'update_product':
            client.update_product(proxy, args.id, args.name, args.description, args.manufacturer,
                        args.wholesale_cost, args.sale_cost, args.stock)
        if args.rpc == 'get_instock':
            client.get_instock_products(proxy)
        if args.rpc == 'get_all':
            client.get_all_products(proxy)
        if args.rpc == 'create_order':
            client.create_order(proxy, args.destination, args.date, args.product_list, args.paid, args.shipped)
        if args.rpc == 'get_order':
            client.get_order(proxy, args.id)
        if args.rpc == 'amend_order':
            client.amend_order(proxy, args.id, args.destination, args.date, args.add_products, args.remove_products,
                        args.paid, args.shipped)
        if args.rpc == 'orders_status':
            client.get_unshipped_unpaid_orders(proxy, args.unshipped, args.unpaid)

def main():
    # Create argument parser and subparsers
    parser = argparse.ArgumentParser(description='Interact with the Inventory System Server using gRPC or XML-RPC.')

    # Argument for which RPC framework to use
    rpc_framework = parser.add_argument('framework', type=str, choices=['grpc', 'xmlrpc'],
        help='rpc framework for server/client')

    subparsers = parser.add_subparsers(title='remote procedure calls', dest='rpc', required=True)
    # Parser and arguments for adding a product
    add_product = subparsers.add_parser(name='add_product', description='Add a new product to the Inventory System')
    add_product.add_argument('name', type=str, help='name of the product to add')
    add_product.add_argument('description', type=str, help='description of the product to add')
    add_product.add_argument('manufacturer', type=str, help='manufacturer of the product to add')
    add_product.add_argument('wholesale_cost', type=float, help='wholesale cost of the product')
    add_product.add_argument('sale_cost', type=float, help='sale cost of the product')
    add_product.add_argument('stock', type=int, help='quantity of the product')

    # Parser and arguments for getting a product
    get_product = subparsers.add_parser(name='get_product', description='Get a product\'s information from the Inventory System')
    get_product.add_argument('-id', '--product_id', type=str, default='-2', help='the id number of the post to get')
    get_product.add_argument('-n', '--name', type=str, default='#', help='the name of the post to get')

    # Parser and argument for getting products by a manufacturer
    get_manufacturer = subparsers.add_parser(name='get_manufacturer_products', 
        description= 'Get manufacturer products by given manufacturer name')
    get_manufacturer.add_argument('manufacturer', type=str, help='the manufacturer name of the products')

    # Parser and arguments for updating a product
    update_product = subparsers.add_parser(name='update_product', description='Update a product in the Inventory System')
    update_product.add_argument('id', type=str, help='the id of the product to update')
    update_product.add_argument('name', type=str, help='the name of the product to update')
    update_product.add_argument('-d', '--description', type=str, default='#',help='the description of the product to update')
    update_product.add_argument('-m', '--manufacturer', type=str, default='#', help='the manufacturer of the product to update')
    update_product.add_argument('-wc', '--wholesale_cost', type=float, default=-1, help='the wholesale cost of the product')
    update_product.add_argument('-sc', '--sale_cost', type=float, default=-1, help='the sale cost of the product')
    update_product.add_argument('-s', '--stock', type=int, default=-1, help='the quantity of the product')

    # Parser for getting in-stock products
    subparsers.add_parser(name='get_instock', description='List all in-stock products in the Inventory System')

    # Parser for getting all products
    subparsers.add_parser(name='get_all', description='List all products in the Inventory System')

    # Parser and arguments for creating an order
    create_order = subparsers.add_parser(name='create_order', description='Create a new order')
    create_order.add_argument('destination', type=str, help='the description of the order to create')
    create_order.add_argument('date', type=str, help='the data of creation of order')
    create_order.add_argument('paid', choices=[True, False], type=bool, default=False, 
        help='True if order has been paid, otherwise False')
    create_order.add_argument('shipped', choices=[True, False], type=bool, default=False, 
        help='True if order has been shipped, otherwise False')
    create_order.add_argument('product_list', nargs='+', type=lambda s: [ product for product in s.split(',')] , 
        help='list of products to add to the order')

    # Parser and argument for getting an order
    get_order = subparsers.add_parser(name='get_order', description='Get an existing order')
    get_order.add_argument('id', type=str, help='the order id to get')

    # Parser and arguments for amending/updating an order
    amend_order = subparsers.add_parser(name='amend_order', description='Amend an order')
    amend_order.add_argument('id', type=str, help='the order id to update')
    amend_order.add_argument('-d', '--destination', default="#", type=str, help='the description of the order to create')
    amend_order.add_argument('--date', default="#", type=str, help='the creation date of order')
    amend_order.add_argument('-p', '--paid', default=False, choices=[True, False], type=bool, nargs='?',
        help='True if order has been paid, otherwise False')
    amend_order.add_argument('-s', '--shipped', default=False, choices=[True, False], type=bool, nargs='?',
        help='True if order has been shipped, otherwise False')
    amend_order.add_argument('-a', '--add_products', default=[], nargs='+', type=lambda s: [ product for product in s.split(',')] ,
        help='the list of product to be added')
    amend_order.add_argument('-r', '--remove_products', default=[], nargs='+', type=lambda s: [ product for product in s.split(',')], 
        help='the list of product to be removed')

    # Parser and argument for getting unpaid/unshipped orders
    orders_status = subparsers.add_parser(name='orders_status', description='Get unshipped and/or unpaid orders')
    orders_status.add_argument('-us', '--unshipped', choices=[True, False], type=bool, default=False, 
        help='specify if querying for unshipped orders')
    orders_status.add_argument('-up', '--unpaid', choices=[True, False], type=bool, default=False, 
        help='specify if querying for unpaid orders')

    # Parse args
    args = parser.parse_args()

    # User chooses to use gRPC
    if args.framework == "grpc":
        parse_grpc(args)

    # User chooses to use XML-RPC
    if args.framework == "xmlrpc":
        parse_xmlrpc(args)


if __name__ == '__main__':    
    main()

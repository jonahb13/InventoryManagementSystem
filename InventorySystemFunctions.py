"""
Project 02 - RPCs
Helper functions for gRPC and XML-RPC server.
Jonah Beers and Riyad Alghamdi 
"""
import uuid
import pickle

PRODUCTS_DB = {}
ORDERS_DB = {}
ID_TO_NAME = {}
NAME_TO_ID = {}

class Product():
    
    def __init__(self, id_, name, description, manufacturer, wholesale_cost, sale_cost, stock):
        """
        Product initializer. 
        """
        self.id_ = id_ 
        self.name = name 
        self.description = description 
        self.manufacturer = manufacturer
        self.wholesale_cost = wholesale_cost
        self.sale_cost = sale_cost
        self.stock = stock


class Order():

    def __init__(self, id_, destination, date, products, is_paid, is_shipped):
        """
        Order initializer. 
        """
        self.id_ = id_
        self.destination = destination
        self.date = date
        self.products = products 
        self.is_paid = is_paid
        self.is_shipped = is_shipped


def get_product_from_DB(product):
    """
    Gets a product from the DB. Takes a Product object as a
    parameter and returns a dictionary of the product's attributes.
    """
    id_ = product.id_
    name = product.name
    description = product.description
    manufacturer = product.manufacturer
    wholesale_cost = product.wholesale_cost
    sale_cost = product.sale_cost
    stock = product.stock
    return {"id" : id_, "name" : name, "description" : description, "manufacturer" : manufacturer,
        "wholesale_cost" : wholesale_cost, "sale_cost" : sale_cost, "stock" : stock}

def get_order_information(id_):
    """
    Gets an order from the DB. Takes an Order object as a
    parameter and returns a dictionary of the orders's attributes.
    """
    destination = ORDERS_DB[id_].destination
    date = ORDERS_DB[id_].date
    ordered_products = ORDERS_DB[id_].products
    is_paid = ORDERS_DB[id_].is_paid
    is_shipped = ORDERS_DB[id_].is_shipped
    return {"id" : id_, "destination" : destination, "date" : date,
        "ordered_products" : ordered_products, "is_paid" : is_paid, "is_shipped" : is_shipped}

def add_product(name, description, manufacturer, wholesale_cost, sale_cost, stock):
    """
    Adds a new product to the DB. If the product name already exists,
    returns an error code (names are not case sensitive). Otherwise,
    save attributes as a Product object.
    """
    id_ = str(uuid.uuid4())
    while id_ in ID_TO_NAME.keys():
        id_ = str(uuid.uuid4())
    for product_name in NAME_TO_ID.keys(): # compare against all existing product names
        if name.lower() == product_name.lower(): # not case sensitive
            return -1
    if wholesale_cost <= 0: # if field is not valid
        wholesale_cost = 1.0
    if sale_cost <= 0: # if field is not valid
        sale_cost = 1.0
    if stock < 0: # if field is not valid
        stock = 0
    PRODUCTS_DB[(id_, name)] = Product(id_, name, description, manufacturer, wholesale_cost, sale_cost, stock)
    ID_TO_NAME[id_] = name
    NAME_TO_ID[name] = id_
    return id_

def get_product(id_, name):
    """
    Gets a Product object from the DB. Takes product ID and name as
    a parameter. Since clients can look up a product by ID or name,
    default for ID is -2 and default for name is "#".
    """
    product_identifier = ()
    if id_ == '-2' and name == "#":
        return -2
    if id_ != '-2': # default (used name to get product) is -2
        if id_ in ID_TO_NAME.keys(): # product ID exists
            product_identifier = (id_, ID_TO_NAME[id_])
    elif name != "#": # default (used ID to get product) is "#"
        if name in NAME_TO_ID.keys(): # product name exists
            product_identifier = (NAME_TO_ID[name], name)
    else:
        return -1
    return PRODUCTS_DB[product_identifier]

def update_product(product_identifier, description, manufacturer, wholesale_cost, sale_cost, stock):
    """
    Updates a product in the DB. Takes the product identifier and the
    other product attributes as parameters. If the client wants fields
    updated (default values are not used), Product in the DB is updated.
    """
    if product_identifier in PRODUCTS_DB: # make sure ID and name match to an existing product
        if description != "#": # default (don't want it changed) is "#"
            PRODUCTS_DB[product_identifier].description = description
        if manufacturer != "#": # default (don't want it changed) is "#"
            PRODUCTS_DB[product_identifier].manufacturer = manufacturer
        if wholesale_cost > 0: # default (don't want it changed) is -1.0
            PRODUCTS_DB[product_identifier].wholesale_cost = wholesale_cost
        if sale_cost > 0: # default (don't want it changed) is -1.0
            PRODUCTS_DB[product_identifier].sale_cost = sale_cost
        if stock >= 0: # default (don't want it changed) is -1
            PRODUCTS_DB[product_identifier].stock = stock
        return True
    return False

def get_manufacturer_products(manufacturer):
    """
    Gets all products from the DB that were manufactured by the
    manufacturer that the client specified.
    """
    for product_identifier in PRODUCTS_DB.keys(): # loop over all products
        if PRODUCTS_DB[product_identifier].manufacturer == manufacturer:
            yield get_product_from_DB(PRODUCTS_DB[product_identifier])

def get_all_products():
    """
    Gets all products from the DB.
    """
    for product_identifier in PRODUCTS_DB.keys(): # loop over all products
        yield get_product_from_DB(PRODUCTS_DB[product_identifier])

def get_instock_products():
    """
    Gets all products from the DB that have a stock greater than 0.
    """
    for product_identifier in PRODUCTS_DB.keys(): # loop over all products
        if PRODUCTS_DB[product_identifier].stock > 0:
            yield get_product_from_DB(PRODUCTS_DB[product_identifier])

def create_order(destination, date, products, is_paid, is_shipped):
    """
    Creates a new order and adds it to the DB as an Order object.
    Order will only be created if all products can be added. Otherwise,
    a message will be returned depending on the error that occurred.
    """
    id_ = str(uuid.uuid4())
    message = ""
    while id_ in ID_TO_NAME.keys():
        id_ = str(uuid.uuid4())
    products_to_order = products
    products = {}
    for product in products_to_order.keys():
        if product not in NAME_TO_ID.keys(): # if the product does not exist
            message = product + ": this product does not exist!"
            return -1, message
        # if the client wants more than what is available in the stock
        elif PRODUCTS_DB[(NAME_TO_ID[product], product)].stock - products_to_order[product] < 0:
            tense = ""
            if PRODUCTS_DB[(NAME_TO_ID[product], product)].stock == 1: # change tense if 1 product
                tense = " is"
            else: # change tense if != 1 product
                tense = "s are"
            message = str(PRODUCTS_DB[(NAME_TO_ID[product], product)].stock) + " " + product + \
            tense + " left in stock but you requested to order " + str(products_to_order[product]) + "."
            return -2, message
        else: # adds the product to the list of products to order
            products[product] = products_to_order[product]
    for product in products: # removes products from stock since all products can be added to the order
        PRODUCTS_DB[(NAME_TO_ID[product], product)].stock -= products[product]
    ORDERS_DB[id_] = Order(id_, destination, date, products, is_paid, is_shipped)
    return id_, message

def get_order(id_):
    """
    Gets an order from the DB. Takes Order ID as a parameter. If the
    ID does not exist, an error message is returned.
    """
    message = ""
    if id_ not in ORDERS_DB.keys(): # if the order ID does not exist
        message = id_ + ": this Order ID does not exist."
        return -1, message
    order = get_order_information(id_)
    return order, message

def check_add_products_to_order(add_products, products):
    """
    Checks if all products can successfully be added to an order.
    If any error occurrs, message is returned to the client and no
    products may be added. Otherwise, products/quantities are returned.
    """
    message = ""
    products_to_add = {}
    if len(add_products) != 0:
        for product in add_products.keys():
            if product not in products: # if there is no amount of the product in the order already
                if product in NAME_TO_ID.keys(): # if the product name exists
                    if PRODUCTS_DB[(NAME_TO_ID[product], product)].stock - add_products[product] >= 0:
                        products_to_add[product] = add_products[product]
                        continue
                else:
                    message = product + ": this product does not exist!"
                    return -2, message, products_to_add
            else: # if there is at least one of the product in the order already
                if PRODUCTS_DB[(NAME_TO_ID[product], product)].stock - add_products[product] >= 0:
                    products_to_add[product] = add_products[product]
                    continue
            message = "There are not enough " + product + "s in stock! Available stock: " + \
            str(PRODUCTS_DB[(NAME_TO_ID[product], product)].stock)
            return -2, message, products_to_add
    return -1, message, products_to_add

def add_products_to_order(current_products, products_to_add):
    """
    Adds products to an order if all products are able to be added
    or removed from an order.
    """
    # Removes products from stock since all products can be added/removed to or from the order
    for product in products_to_add.keys():
        if product in current_products:
            current_products[product] += products_to_add[product]
        else:
            current_products[product] = products_to_add[product]
        PRODUCTS_DB[(NAME_TO_ID[product], product)].stock -= products_to_add[product]

def check_remove_products_from_order(remove_products, products):
    """
    Checks if all products can successfully be removed from an order.
    If any error occurrs, message is returned to the client and no
    products may be removed. Otherwise, products/quantities are returned.
    """
    message = ""
    products_to_remove = {}
    if len(remove_products) != 0:
        for product in remove_products.keys():
            if product in NAME_TO_ID.keys():
                if product in products: # if product exists in the order
                    difference = products[product] - remove_products[product]
                    if difference < 0: # if they are requesting to remove more than was ordered
                        message = "There are not enough " + product + "s in the order to remove! " + \
                        "Available " + product + "s to remove: " + str(products[product])
                        return -2, message, products_to_remove
                    else:
                        products_to_remove[product] = remove_products[product]
                else: # product is not in the order
                    message = product + " is not in the order, but you are trying to remove it!"
                    return -2, message, products_to_remove
            else: # if product name does not exist
                message = product + ": this product does not exist!"
                return -2, message, products_to_remove
    return -1, message, products_to_remove

def remove_products_from_order(current_products, products_to_remove):
    """
    Removes products from an order if all products are able to be added
    or removed from an order.
    """
    # Adds products to stock since all products can be added/removed to or from the order
    for product in products_to_remove.keys():
        if current_products[product] - products_to_remove[product] > 0:
            current_products[product] -= products_to_remove[product]
        else:
            del current_products[product]
        PRODUCTS_DB[(NAME_TO_ID[product], product)].stock += products_to_remove[product]

def amend_order(id_, destination, date, add_products, remove_products, is_paid, is_shipped):
    """
    Updates (amends) an order in the DB. If order ID exists and no errors
    arise, then attributes of Order object are updated and a confirmation
    message is returned. Otherwise, some error message is returned.
    """
    if id_ in ORDERS_DB.keys():
        products = ORDERS_DB[id_].products
        return_code, message, products_to_add = check_add_products_to_order(add_products, products)
        if return_code == -2: # some product is not able to be added
            return message
        return_code, message, products_to_remove = check_remove_products_from_order(remove_products, products)
        if return_code == -2: # some product is not able to be removed
            return message
        add_products_to_order(products, products_to_add) # actually add products and update stock
        remove_products_from_order(products, products_to_remove) # actually remove products and update stock
        if destination != "#":
            ORDERS_DB[id_].destination = destination
        if date != "#":
            ORDERS_DB[id_].date = date
        if is_paid:
            ORDERS_DB[id_].is_paid = is_paid
        if is_shipped:
            ORDERS_DB[id_].is_shipped = is_shipped
        return "Order has been successfully updated!"
    return "Failure to update the order: order ID does not exist!"

def get_unshipped_unpaid_orders(is_unshipped, is_unpaid):
    """
    Returns all orders that are unshipped, unpaid, or
    unshipped and unpaid, depending what the client wants.
    """
    if is_unshipped and is_unpaid: # query for unshipped and unpaid orders
        for order in ORDERS_DB.values():
            if not order.is_shipped and not order.is_paid:
                yield get_order_information(order.id_)
        return
    if is_unpaid: # query for unpaid orders
        for order in ORDERS_DB.values():
            if not order.is_paid:
                yield get_order_information(order.id_)
    if is_unshipped: # query for unshipped orders
        for order in ORDERS_DB.values():
            if not order.is_shipped:
                yield get_order_information(order.id_)


def save_file():
    """
    Saves DBs to a file upon server shutting down.
    """
    with open("inventory_system.bin", "wb",) as f:
        print("\nWriting data to the file...")
        pickle.dump(PRODUCTS_DB, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(ORDERS_DB, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(ID_TO_NAME, f, protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(NAME_TO_ID, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Databases saved. Server is closed.")

def read_file():
    """
    Sets DBs to the data stored in a file when server starts.
    """
    global PRODUCTS_DB
    global ORDERS_DB
    global ID_TO_NAME
    global NAME_TO_ID
    with open("inventory_system.bin", "rb") as f:
        print("Reading data from the file...")
        PRODUCTS_DB = pickle.load(f)
        ORDERS_DB = pickle.load(f)
        ID_TO_NAME = pickle.load(f)
        NAME_TO_ID = pickle.load(f)
        print("Databases are uploaded. Server is ready.")
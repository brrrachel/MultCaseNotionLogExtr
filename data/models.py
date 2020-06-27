class Address:
    def __init__(self, id, street, number, city, post_code):
        self.id = id
        self.street = street
        self.number = number
        self.city = city
        self.post_code = post_code


class Brand:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Customer:
    def __init__(self, id, store_id, firstname, lastname, email, address_id):
        self.id = id
        self.shop_id = shop_id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.address_id = address_id


class Equipment:
    def __init__(self, id, name, information, year, brand_id, rental_rate, replacement_cost, special_features):
        self.id = id
        self.name = name
        self.information = information
        self.year = year
        self.brand_id = brand_id
        self.rental_rate = rental_rate
        self.replacement_cost = replacement_cost
        self.special_features = special_features
        
        
class Inventory:
    def __init__(self, id, equipment_id, store_id):
        self.id = id
        self.equipment_id = equipment_id
        self.store_id = store_id
        
        
class Staff:
    def __init__(self, id, firstname, lastname, address_id, email, store_id):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.address_id = address_id
        self.email = email
        self.store_id = store_id
        
        
class Store:
    def __init__(self, id, manager_id, address_id):
        self.id = id
        self.manager_id = manager_id
        self.address_id = address_id
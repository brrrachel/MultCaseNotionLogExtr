import datetime
import random
import pandas as pd
import numpy as np

'''
Processes:

create_rental -> create_payment -> confirm_payment -> confirm_rental -> cancel_equipment
create_rental -> create_payment -> confirm_payment -> confirm_rental -> lend_equipment -> return_equipment -> inspect_equipment
create_rental -> create_payment -> confirm_payment -> confirm_rental -> lend_equipment -> return_equipment -> inspect_equipment -> create_payment -> confirm_payment

'''

class ProcessSimulator:

    def __init__(self):
        path = 'availableData/'

        # load available data
        self.address = pd.read_csv(path + 'address.csv', index_col=0)
        self.brand = pd.read_csv(path + 'brand.csv', index_col=0)
        self.customer = pd.read_csv(path + 'customer.csv', index_col=0)
        self.equipment = pd.read_csv(path + 'equipment.csv', index_col=0)
        self.inventory = pd.read_csv(path + 'inventory.csv', index_col=0)
        self.staff = pd.read_csv(path + 'staff.csv', index_col=0)
        self.store = pd.read_csv(path + 'store.csv', index_col=0)

        # create additional tables
        self.rental_orders = pd.DataFrame(columns=['inventory_id', 'costumer_id', 'created_date', 'confirmed_date'])
        self.lended_equipments = pd.DataFrame(columns=['rental_id', 'inventory_id', 'cancel_date', 'lend_date', 'return_date', 'inspection_id'])
        self.inspections = pd.DataFrame(columns=['inspector_id', 'date', 'payment_id']) # inspector == staff
        self.payments = pd.DataFrame(columns=['rental_id', 'customer_id', 'value', 'created_date', 'confirmed_date'])

    '''
        Helper Methods
    '''

    def __get_costumer_ids__(self) -> []:
        return self.customer.index.tolist()

    def __get_store_of_customer__(self, customer_id):
        return self.customer.iloc[customer_id]['store_id']

    def __get_inventory_ids_for_store__(self, store_id) -> []:
        return self.inventory.loc[(self.inventory['store_id'] == store_id)].index.tolist()

    def __get_overall_lended_inventory_ids__(self, date) -> []:
        return self.lended_equipments.loc[(self.lended_equipments['return_date'] <= date) & (self.lended_equipments['inspection_id'] == False)].index.tolist()

    '''
        Costumer Methods
    '''

    def select_available_equipment_from_store(self, store_id, rental_date, count=2):
        # available = inventory_id in lended_equipments table where return_date is before rental_date and inspection_id is not False
        inventory_of_store = self.__get_inventory_ids_for_store__(store_id)
        currently_lended_inventory = self.__get_overall_lended_inventory_ids__(rental_date)
        available_inventory = list(set(inventory_of_store).difference(currently_lended_inventory))
        return list(set(random.choices(available_inventory, k=count)))


    '''
        Defining activities
    '''

    def create_rental(self, costumer_id, inventory_id_list):

        return None

    def create_payment(self):
        return None

    def confirm_payment(self):
        return None

    def confirm_rental(self):
        return None

    def cancel_equipment(self):
        return None

    def lend_equipment(self):
        return None

    def return_equipment(self):
        return None

    def inspect_equipment(self):
        return None

    def simulate_process(self, start_time):

        current_time = start_time

        for c in self.__get_costumer_ids__():
            belonging_store_id = self.__get_store_of_customer__(c)

            rental_date = current_time + datetime.timedelta(days=3)
            selected_equipment = self.select_available_equipment_from_store(belonging_store_id, rental_date)
            print('Costumer with id ' + str(c) + ' has selected inventory with id(s) ' + str(selected_equipment) + ' from store id ' + str(belonging_store_id))

            c.create_rental(c, rental_date)

    def save_table_to_csv(self):
        path = 'generatedData/'

        self.rental_orders.to_csv(path + 'rental_orders.csv')
        self.lended_equipments.to_csv(path + 'lended_equipments.csv')
        self.inspections.to_csv(path + 'inspections.csv')
        self.payments.to_csv(path + 'payments.csv')

if __name__ == '__main__':

    ps = ProcessSimulator()
    start = datetime.datetime(year=2020, month=1, day=1)
    ps.simulate_process(start)

    #ps.save_table_to_csv()

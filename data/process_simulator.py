import datetime
import random
import pandas as pd

'''
Processes:

create_rental -> confirm_payment -> confirm_rental -> cancel_equipment
create_rental -> confirm_payment -> confirm_rental -> lend_equipment -> return_equipment -> inspect_equipment
create_rental -> confirm_payment -> confirm_rental -> lend_equipment -> return_equipment -> inspect_equipment -> create_payment -> confirm_payment

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
        self.rental_orders = pd.DataFrame(columns=['costumer_id', 'created_date', 'confirmed_date'])
        self.lended_inventory = pd.DataFrame(columns=['rental_id', 'inventory_id', 'created_date', 'cancel_date', 'lend_date', 'return_date', 'inspection_id'])
        self.inspections = pd.DataFrame(columns=['inspector_id', 'date', 'payment_id']) # inspector == staff
        self.payments = pd.DataFrame(columns=['rental_id', 'value', 'created_date', 'confirmed_date'])

    '''
        Helper Methods
    '''

    def __get_costumer_ids__(self) -> list:
        return self.customer.index.tolist()

    def __get_store_of_customer__(self, customer_id: int):
        return self.customer.iloc[customer_id-1]['store_id']

    def __get_inventory_ids_for_store__(self, store_id: int) -> list:
        return self.inventory.loc[(self.inventory['store_id'] == store_id)].index.tolist()

    def __get_rental_rate_for_inventory_id__(self, inventory_id: int) -> float:
        equipment_id = self.inventory.iloc[inventory_id-1]['equipment_id']
        return self.equipment.iloc[equipment_id-1]['rental_rate'].item()

    def __get_overall_lended_inventory_ids__(self) -> list:
        return list(self.lended_inventory[self.lended_inventory['inspection_id'].isna() & self.lended_inventory['cancel_date'].isna()]['inventory_id'])

    '''
        Costumer Activities
    '''

    def select_available_equipment_from_store(self, store_id: int, date: datetime.datetime, count=2) -> list:
        # lended = inventory_id in lended inventory table where inspection_id and cancel_date are not defined
        inventory_of_store = self.__get_inventory_ids_for_store__(store_id)
        currently_lended_inventory = self.__get_overall_lended_inventory_ids__()
        available_inventory = list(set(inventory_of_store).difference(currently_lended_inventory))
        return list(set(random.choices(available_inventory, k=count)))

    '''
        Defining Activities
    '''

    def create_rental(self, customer_id: int, inventory_ids_list: list, date: datetime.datetime) -> (int, list):

        # create rental
        new_rental = {'customer_id': customer_id, 'created_date': date}
        self.rental_orders = self.rental_orders.append(new_rental, ignore_index=True)
        rental_id = self.rental_orders.index.max()
        print('Customer ' + str(customer_id) + ' created rental ' + str(rental_id) + ' on ' + date.__str__())

        # create entry for each inventory to lend
        lended_inventory_ids = []
        for inventory_id in inventory_ids_list:
            new_lended_inventory = {'rental_id': rental_id, 'inventory_id': inventory_id, 'created_date': date}
            self.lended_inventory = self.lended_inventory.append(new_lended_inventory, ignore_index=True)
            lended_inventory_ids.append(self.lended_inventory.index.max())
        return rental_id, lended_inventory_ids

    def create_payment(self, rental_id: int, inventory_ids_list: list, date) -> int:
        total_payment = []
        for inventory_id in inventory_ids_list:
            total_payment.append(self.__get_rental_rate_for_inventory_id__(inventory_id))

        new_payment = {'rental_id': rental_id, 'value': round(sum(total_payment), 2), 'created_date': date}
        self.payments = self.payments.append(new_payment, ignore_index=True)
        payment_id = self.payments.index.max()
        print('Payment ' + str(payment_id) + ' with value ' + str(round(sum(total_payment), 2)) + ' created for rental ' + str(rental_id) + ' including inventory ids ' + str(inventory_ids_list))
        return payment_id

    def confirm_payment(self, rental_id: int, date: datetime.datetime) -> int:
        self.payments.loc[(self.payments['rental_id'] == rental_id)]['confirmed_date'] = date
        payment_id = self.payments.loc[(self.payments['rental_id'] == rental_id)].index.max()
        print('Payment ' + str(payment_id) + ' received on ' + date.__str__())
        return payment_id

    def confirm_rental(self, rental_id: int, date: datetime.datetime) -> int:
        self.rental_orders.iloc[rental_id-1]['confirmed_date'] = date
        print('Rental ' + str(rental_id) + ' confirmed on ' + date.__str__())
        return rental_id

    def cancel_inventory(self, lended_inventory_id: int, date: datetime.datetime) -> int:
        self.lended_inventory.iloc[lended_inventory_id-1]['cancel_date'] = date
        print('Lended inventory order ' + str(lended_inventory_id) + ' has been canceled on ' + date.__str__())
        return lended_inventory_id

    def lend_inventory(self, lended_inventory_ids: list, date: datetime.datetime):
        for li in lended_inventory_ids:
            self.lended_inventory.iloc[li-1]['cancel_date'] = date
        print('Lended inventory ids ' + str(lended_inventory_ids) + ' are/were picked up on ' + date.__str__())
        return lended_inventory_ids

    def return_inventory(self):
        return None

    def inspect_inventory(self):
        return None

    def simulate_process(self, start_time):

        current_time = start_time

        for c in self.__get_costumer_ids__():
            belonging_store_id = self.__get_store_of_customer__(c)
            selected_inventory = self.select_available_equipment_from_store(belonging_store_id, current_time)

            rental_id, lended_inventory_ids = self.create_rental(c, selected_inventory, current_time)
            payment_id = self.create_payment(rental_id, selected_inventory, current_time)
            payment_id = self.confirm_payment(rental_id, current_time)
            rental_id = self.confirm_rental(rental_id, current_time)

    def save_table_to_csv(self):
        path = 'generatedData/'

        self.rental_orders.to_csv(path + 'rental_orders.csv')
        self.lended_inventory.to_csv(path + 'lended_inventory.csv')
        self.inspections.to_csv(path + 'inspections.csv')
        self.payments.to_csv(path + 'payments.csv')

if __name__ == '__main__':

    ps = ProcessSimulator()
    ps.simulate_process(datetime.datetime(year=2020, month=1, day=1))

    #ps.save_table_to_csv()

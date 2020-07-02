import datetime
import random
import pandas as pd
import numpy as np

'''
Processes:

create_rental -> confirm_payment -> confirm_rental -> cancel_inventory
create_rental -> confirm_payment -> confirm_rental -> lend_inventory -> return_inventory -> inspect_inventory
create_rental -> confirm_payment -> confirm_rental -> lend_inventory -> return_inventory -> inspect_inventory -> create_payment -> confirm_payment

'''


class ProcessSimulator:

    def __init__(self):
        path = 'availableData/'
        print(pd.__version__)

        # load available data
        self.address = pd.read_csv(path + 'address.csv', index_col=0)
        self.brand = pd.read_csv(path + 'brand.csv', index_col=0)
        self.customer = pd.read_csv(path + 'customer.csv', index_col=0)
        self.equipment = pd.read_csv(path + 'equipment.csv', index_col=0)
        self.inventory = pd.read_csv(path + 'inventory.csv', index_col=0)
        self.staff = pd.read_csv(path + 'staff.csv', index_col=0)
        self.store = pd.read_csv(path + 'store.csv', index_col=0)

        # create additional tables
        self.rental_orders = pd.DataFrame(columns=['rowid', 'customer_id', 'rental_created_date', 'rental_confirmed_date'])
        self.lended_inventory = pd.DataFrame(columns=['rowid', 'rental_id', 'inventory_id', 'li_created_date', 'li_cancel_date', 'li_lend_date', 'li_return_date', 'inspection_id'])
        self.inspections = pd.DataFrame(columns=['rowid', 'inspector_id', 'inspection_date', 'payment_id']) # inspector == staff
        self.payments = pd.DataFrame(columns=['rowid', 'rental_id', 'value', 'pay_created_date', 'pay_confirmed_date'])

    '''
        Helper Methods
    '''

    def __get_new_id_for_table__(self, list) -> int:
        return 0 if list.index.max() is np.nan else list.index.max()+1

    def __get_customer_ids__(self) -> list:
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
        
    def __get_staff_id_for_inspection__(self, inventory_id: int) -> int:
        store_id = self.inventory.iloc[inventory_id]['store_id']
        staff_ids = self.staff.loc[(self.staff['store_id'] == store_id)].index.tolist()
        return random.choice(staff_ids)

    def select_available_equipment_from_store(self, store_id: int, date: datetime.datetime, count=2) -> list:
        # lended = inventory_id in lended inventory table where inspection_id and cancel_date are not defined
        inventory_of_store = self.__get_inventory_ids_for_store__(store_id)
        #currently_lended_inventory = self.__get_overall_lended_inventory_ids__()
        #available_inventory = list(set(inventory_of_store).difference(currently_lended_inventory))
        return list(set(random.choices(inventory_of_store, k = count)))

    '''
        Defining Activities
    '''

    def create_rental(self, customer_id: int, inventory_ids: list, date: datetime.datetime) -> (int, list):

        # create rental
        rental_id = self.__get_new_id_for_table__(self.rental_orders)
        new_rental = {'rowid': rental_id, 'customer_id': int(customer_id), 'rental_created_date': date}
        self.rental_orders = self.rental_orders.append(new_rental, ignore_index=True)
        print('Customer ' + str(customer_id) + ' created rental ' + str(rental_id) + ' on ' + date.__str__())

        # create entry for each inventory to lend
        lended_inventory_ids = []
        for inventory_id in inventory_ids:
            li_id = self.__get_new_id_for_table__(self.lended_inventory)
            new_lended_inventory = {'rowid': li_id,'rental_id': rental_id, 'inventory_id': inventory_id, 'li_created_date': date}
            self.lended_inventory = self.lended_inventory.append(new_lended_inventory, ignore_index=True)
            lended_inventory_ids.append(li_id)
        return rental_id, lended_inventory_ids

    def create_payment(self, rental_id: int, inventory_ids: list, date: datetime.datetime) -> int:
        total_payment = []
        for inventory_id in inventory_ids:
            total_payment.append(self.__get_rental_rate_for_inventory_id__(inventory_id))

        payment_id = self.__get_new_id_for_table__(self.payments)
        new_payment = {'rowid': payment_id, 'rental_id': rental_id, 'value': round(sum(total_payment), 2), 'pay_created_date': date}
        self.payments = self.payments.append(new_payment, ignore_index=True)
        print('Payment ' + str(payment_id) + ' with value ' + str(round(sum(total_payment), 2)) + ' created for rental ' + str(rental_id) + ' including inventory ids ' + str(inventory_ids))
        return payment_id

    def confirm_payment(self, payment_id: int, date: datetime.datetime):
        self.payments.iloc[payment_id, self.payments.columns.get_loc('pay_confirmed_date')] = date
        print('Payment ' + str(payment_id) + ' received on ' + date.__str__())

    def confirm_rental(self, rental_id: int, date: datetime.datetime):
        self.rental_orders.iloc[rental_id, self.rental_orders.columns.get_loc('rental_confirmed_date')] = date
        print('Rental ' + str(rental_id) + ' confirmed on ' + date.__str__())

    def cancel_inventory(self, inventory_id: int, date: datetime.datetime):
        self.lended_inventory.iloc[inventory_id, self.lended_inventory.columns.get_loc('li_cancel_date')] = date
        print('Lended inventory order ' + str(inventory_id) + ' has been canceled on ' + date.__str__())

    def lend_inventory(self, inventory_ids: list, date: datetime.datetime):
        for inventory_id in inventory_ids:
            self.lended_inventory.iloc[inventory_id, self.lended_inventory.columns.get_loc('li_lend_date')] = date
        print('Lended inventory ids ' + str(inventory_ids) + ' were picked up on ' + date.__str__())

    def return_inventory(self, rental_id: int, inventory_ids: list, date: datetime.datetime):
        additional_payment_ids = []
        print('Lended inventory ids ' + str(inventory_ids) + ' were returned up on ' + date.__str__() + '.')
        for inventory_id in inventory_ids:
            inspection_id, payment_id = self.inspect_inventory(rental_id, inventory_id, date)
            if payment_id != -1:
                additional_payment_ids.append(payment_id)
            self.lended_inventory.iloc[inventory_id, self.lended_inventory.columns.get_loc('li_return_date')] = date
            self.lended_inventory.iloc[inventory_id, self.lended_inventory.columns.get_loc('inspection_id')] = inspection_id
        return additional_payment_ids

    def inspect_inventory(self, rental_id: int, inventory_id: int, date: datetime.datetime):
        inspector_id = self.__get_staff_id_for_inspection__(inventory_id)
        payment_id = -1
        inspection_id = self.__get_new_id_for_table__(self.inspections)
        if random.uniform(0, 1) < 0.05:
            payment_id = self.create_payment(rental_id, [inventory_id], date)
            new_inspection = {'rowid': inspection_id, 'inspector_id': inspector_id, 'inspection_date': date, 'payment_id': payment_id}
            print('Lended inventory id ' + str(inventory_id) + ' was inspected up on ' + date.__str__() + '. Due to damage of the equipment an additional payment was created.')
        else:
            new_inspection = {'rowid': inspection_id, 'inspector_id': inspector_id, 'inspection_date': date}
            print('Lended inventory id ' + str(inventory_id) + ' was inspected up on ' + date.__str__() + '.')
        self.inspections = self.inspections.append(new_inspection, ignore_index=True)
        return inspection_id, payment_id

    def simulate_process(self, start_time):

        current_time = start_time

        for c in self.__get_customer_ids__():
            current_time_process = current_time

            belonging_store_id = self.__get_store_of_customer__(c)
            selected_inventory = self.select_available_equipment_from_store(belonging_store_id, current_time_process)

            rental_id, lended_inventory_ids = self.create_rental(c, selected_inventory, current_time_process)

            current_time_process += datetime.timedelta(seconds=random.randint(30,100))
            payment_id = self.create_payment(rental_id, selected_inventory, current_time_process)

            current_time_process += datetime.timedelta(hours=random.randint(0,24), minutes=random.randint(0,59))
            self.confirm_payment(payment_id, current_time_process)

            current_time_process += datetime.timedelta(seconds=random.randint(30,100))
            self.confirm_rental(rental_id, current_time_process)

            # somehow an rental request for an inventory is beeing canceled
            if random.uniform(0, 1) < 0.2:
                current_time_process += datetime.timedelta(hours=random.randint(0,24), minutes=random.randint(0,59), seconds=random.randint(30,100))
                inventory_id_to_cancel = list(set(random.choices(lended_inventory_ids, k=1)))[0]
                self.cancel_inventory(inventory_id_to_cancel, current_time)
                lended_inventory_ids.remove(inventory_id_to_cancel)

            if len(lended_inventory_ids) > 0:

                current_time_process += datetime.timedelta(days=random.randint(0,1), hours=random.randint(0,72), minutes=random.randint(0,59))
                self.lend_inventory(lended_inventory_ids, current_time_process)

                current_time_process += datetime.timedelta(hours=random.randint(0,72), minutes=random.randint(0,59))
                additional_payment_ids = self.return_inventory(rental_id, lended_inventory_ids, current_time_process)

                for additional_payment_id in additional_payment_ids:
                    current_time = current_time_process + datetime.timedelta(minutes=random.randint(0,59), seconds=random.randint(30,100))
                    self.confirm_payment(additional_payment_id, current_time_process)

    def save_table_to_csv(self):
        path = 'generatedData/'

        self.rental_orders.to_csv(path + 'rental_orders.csv')
        self.lended_inventory.to_csv(path + 'lended_inventory.csv')
        self.inspections.to_csv(path + 'inspections.csv')
        self.payments.to_csv(path + 'payments.csv')


if __name__ == '__main__':

    ps = ProcessSimulator()
    ps.simulate_process(datetime.datetime(year=2020, month=1, day=1))

    ps.save_table_to_csv()

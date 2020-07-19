import datetime
import random
import pandas as pd
from tqdm import tqdm

'''
Processes:

create_rental -> confirm_invoice -> confirm_rental -> cancel_inventory
create_rental -> confirm_invoice -> confirm_rental -> lend_inventory -> return_inventory -> inspect_inventory
create_rental -> confirm_invoice -> confirm_rental -> lend_inventory -> return_inventory -> inspect_inventory -> create_invoice -> confirm_invoice

'''


class ProcessSimulator:

    def __init__(self):
        self.path = 'generatedData/'

        # load available data
        self.address = pd.read_csv(self.path + 'address.csv', index_col=0)
        self.brand = pd.read_csv(self.path + 'brand.csv', index_col=0)
        self.customer = pd.read_csv(self.path + 'customer.csv', index_col=0)
        self.equipment = pd.read_csv(self.path + 'equipment.csv', index_col=0)
        self.inventory = pd.read_csv(self.path + 'inventory.csv', index_col=0)
        self.staff = pd.read_csv(self.path + 'staff.csv', index_col=0)
        self.store = pd.read_csv(self.path + 'store.csv', index_col=0)

        # create additional tables
        self.rental_orders = pd.DataFrame(columns=['customer_id', 'created_date', 'confirmed_date'])
        self.lended_inventory = pd.DataFrame(columns=['rental_id', 'inventory_id', 'created_date', 'cancel_date', 'lend_date', 'return_date'])
        self.inspections = pd.DataFrame(columns=['inspector_id', 'inspection_date', 'lended_inventory_id']) # inspector == staff
        self.invoices = pd.DataFrame(columns=['rental_id', 'value', 'created_date', 'payed_date', 'confirmed_date', 'staff'])

        # create table log
        self.tableLog = pd.DataFrame(columns=['activity','timestamp','rental','inventory','customer','staff','inspection','invoice','lifecycle'])

    '''
        Helper Methods
    '''

    def __get_random_customer_id__(self) -> int:
        return random.choice(self.customer.index.tolist())

    def __get_customer_of_rental__(self, rental_id):
        return self.rental_orders.loc[rental_id]['customer_id']

    def __get_store_of_customer__(self, customer_id: int) -> int:
        return self.customer.loc[customer_id]['store_id']
        
    def __get_store_of_inventory__(self, inventory_id: int) -> int:
        return self.inventory.loc[inventory_id]['store_id']

    def __get_inventory_ids_for_store__(self, store_id: int) -> list:
        return self.inventory.loc[(self.inventory['store_id'] == store_id)].index.tolist()

    def __get_rental_rate_for_inventory_id__(self, inventory_id: int) -> float:
        equipment_id = self.inventory.loc[inventory_id,'equipment_id']
        return self.equipment.loc[equipment_id]['rental_rate'].item()

    def __get_staff_id_for_inventory__(self, inventory_id: int) -> int:
        store_id = self.inventory.loc[inventory_id]['store_id']
        staff_ids = self.staff.loc[(self.staff['store_id'] == store_id)].index.tolist()
        return random.choice(staff_ids)

    def select_inventory_from_store(self, store_id: int, count=2) -> list:
        inventory_of_store = self.__get_inventory_ids_for_store__(store_id)
        return list(set(random.choices(inventory_of_store, k=count)))

    def __create_entry_for_table_log__(self, activity: str, timestamp: datetime.datetime, rental='EMPTY', inventory='EMPTY', customer='EMPTY', staff='EMPTY', inspection='EMPTY', invoice='EMPTY', lifecycle='complete'):
        new_entry = {'activity': activity,
                     'timestamp': timestamp,
                     'rental': str(rental),
                     'inventory': inventory,
                     'customer': customer,
                     'staff': staff,
                     'inspection': inspection,
                     'invoice': invoice,
                     'lifecycle': lifecycle
                     }
        self.tableLog = self.tableLog.append(new_entry, ignore_index=True)

    '''
        Defining Activities
    '''

    def create_rental(self, customer_id: int, inventory_ids: list, date: datetime.datetime):

        # create rental
        new_rental = {'customer_id': customer_id, 'created_date': date}
        self.rental_orders = self.rental_orders.append(new_rental, ignore_index=True)
        rental_id = self.rental_orders.index.max()
        # print('Customer ' + str(customer_id) + ' created rental ' + str(rental_id) + ' on ' + date.__str__())
        self.__create_entry_for_table_log__('create_rental', date, rental=rental_id, inventory=inventory_ids, customer=customer_id)

        # create entry for each inventory to lend
        lended_inventory_ids = []
        for inventory_id in inventory_ids:
            new_lended_inventory = {'rental_id': rental_id, 'inventory_id': inventory_id, 'created_date': date}
            self.lended_inventory = self.lended_inventory.append(new_lended_inventory, ignore_index=True)
            lended_inventory_ids.append(self.lended_inventory.index.max())
        return rental_id, lended_inventory_ids

    def create_invoice(self, rental_id: int, inventory_ids: list, date: datetime.datetime):
        total_invoice = []
        for inventory_id in inventory_ids:
            total_invoice.append(self.__get_rental_rate_for_inventory_id__(inventory_id))

        staff_id = self.__get_staff_id_for_inventory__(inventory_ids[0])
        new_invoice = {'rental_id': rental_id, 'value': round(sum(total_invoice), 2), 'created_date': date, 'staff': staff_id}
        self.invoices = self.invoices.append(new_invoice, ignore_index=True)
        invoice_id = self.invoices.index.max()
        self.__create_entry_for_table_log__('create_invoice', date, rental=rental_id, staff=staff_id, invoice=invoice_id)
        # print('invoice ' + str(invoice_id) + ' with value ' + str(round(sum(total_invoice), 2)) + ' created for rental ' + str(rental_id) + ' including inventory ids ' + str(inventory_ids))
        return invoice_id
        
    def pay_invoice(self, rental_id: int, invoice_id: int, date: datetime.datetime):
        self.invoices.loc[invoice_id, self.invoices.columns.get_loc('payed_date')] = date
        customer_id = self.__get_customer_of_rental__(rental_id)
        self.__create_entry_for_table_log__('pay_invoice', date, rental= rental_id, invoice=invoice_id, customer=customer_id)

    def confirm_invoice(self, rental_id: int, invoice_id: int, date: datetime.datetime, inventory_id: int):
        staff_id = self.__get_staff_id_for_inventory__(inventory_id)
        self.invoices.loc[invoice_id, self.invoices.columns.get_loc('confirmed_date')] = date
        customer_id = self.__get_customer_of_rental__(rental_id)
        self.__create_entry_for_table_log__('confirm_invoice', date, rental= rental_id, invoice=invoice_id, staff=staff_id)
        # print('invoice ' + str(invoice_id) + ' received on ' + date.__str__())

    def confirm_rental(self, rental_id: int, date: datetime.datetime):
        self.rental_orders.loc[rental_id, self.rental_orders.columns.get_loc('confirmed_date')] = date
        inventory_id = self.lended_inventory.loc[(self.lended_inventory['rental_id'] == rental_id)]['inventory_id'].iloc[0]
        staff_id = self.__get_staff_id_for_inventory__(inventory_id)
        customer_id = self.__get_customer_of_rental__(rental_id)
        self.__create_entry_for_table_log__('confirm_rental', date, rental=rental_id, staff=staff_id)
        # print('Rental ' + str(rental_id) + ' confirmed on ' + date.__str__())

    def cancel_inventory(self, rental_id: int, lended_inventory_id: int, date: datetime.datetime, customer_id: int):
        self.lended_inventory.loc[lended_inventory_id, self.lended_inventory.columns.get_loc('cancel_date')] = date
        inventory_id = self.lended_inventory.loc[lended_inventory_id]['inventory_id']
        store_id = self.__get_store_of_inventory__(inventory_id)
        self.__create_entry_for_table_log__('cancel_inventory', date, rental=rental_id, inventory=[inventory_id].__str__(), customer= customer_id)
        # print('Inventory order ' + str(inventory_id) + ' has been canceled on ' + date.__str__())

    def lend_inventory(self, lended_inventory_ids: list, date: datetime.datetime, customer_id: int):
        inventory_ids = []
        for lended_inventory_id in lended_inventory_ids:
            self.lended_inventory.loc[lended_inventory_id, self.lended_inventory.columns.get_loc('lend_date')] = date
            inventory_ids.append(self.lended_inventory.loc[lended_inventory_id]['inventory_id'])

        rental_id = self.lended_inventory.loc[lended_inventory_ids[0]]['rental_id']
        store_id = self.__get_store_of_inventory__(inventory_ids[0])
        staff_id = self.__get_staff_id_for_inventory__(inventory_ids[0])
        self.__create_entry_for_table_log__('lend_inventory', date, rental=rental_id, inventory=inventory_ids.__str__(), customer= customer_id, staff=staff_id)
        # print('Inventory ids ' + str(inventory_ids) + ' were picked up on ' + date.__str__())

    def return_inventory(self, rental_id: int, lended_inventory_ids: list, date: datetime.datetime, customer: str):
        inventory_ids_for_additional_invoice = []
        # print('Inventory ids ' + str(lended_inventory_ids) + ' were returned up on ' + date.__str__() + '.')
        for lended_inventory_id in lended_inventory_ids:
            inventory_id = self.lended_inventory.loc[lended_inventory_id,'inventory_id']
            store_id = self.__get_store_of_inventory__(inventory_id)
            staff_id = self.__get_staff_id_for_inventory__(inventory_id)
            self.__create_entry_for_table_log__('return_inventory', date, rental=rental_id, inventory=[inventory_id].__str__(), customer=customer, staff=staff_id)
            date += datetime.timedelta(seconds=random.randint(30,100))
            inspection_id, inventory_broken, date = self.inspect_inventory(rental_id, lended_inventory_id, date)
            if inventory_broken:
                inventory_ids_for_additional_invoice.append(inventory_id)
            self.lended_inventory.loc[lended_inventory_id, self.lended_inventory.columns.get_loc('return_date')] = date
            date += datetime.timedelta(seconds=random.randint(30,100))
        return inventory_ids_for_additional_invoice, date

    def inspect_inventory(self, rental_id: int, lended_inventory_id: int, date: datetime.datetime):
        inventory_id = self.lended_inventory.loc[lended_inventory_id]['inventory_id']
        inspector_id = self.__get_staff_id_for_inventory__(inventory_id)
        new_inspection = {'inspector_id': inspector_id, 'inspection_date': date, 'lended_inventory_id': lended_inventory_id}
        invoice_id = -1
        self.inspections = self.inspections.append(new_inspection, ignore_index=True)
        inspection_id = self.inspections.index.max()
        store_id = self.__get_store_of_inventory__(inventory_id)
        self.__create_entry_for_table_log__('inspect_inventory', date, rental=rental_id, inventory=[inventory_id].__str__(), staff=inspector_id, inspection=inspection_id, lifecycle='start')
        date += datetime.timedelta(minutes=random.randint(10,30))
        self.__create_entry_for_table_log__('inspect_inventory', date, rental=rental_id, inventory=[inventory_id].__str__(), staff=inspector_id, inspection=inspection_id)
        if random.uniform(0, 1) < 0.1:
            state = True
        else:
            state = False
            # print('Inventory id ' + str(inventory_id) + ' was inspected up on ' + date.__str__() + '.')
        return inspection_id, state, date

    def simulate_process(self, start_time):

        current_time = start_time

        for i in tqdm(range(0,200)):
            customer = self.__get_random_customer_id__()
            current_time_process = current_time

            belonging_store_id = self.__get_store_of_customer__(customer)
            selected_inventory = self.select_inventory_from_store(belonging_store_id)

            rental_id, lended_inventory_ids = self.create_rental(customer, selected_inventory, current_time_process)

            current_time_process += datetime.timedelta(seconds=random.randint(30,100))
            invoice_id = self.create_invoice(rental_id, selected_inventory, current_time_process)
            
            current_time_process += datetime.timedelta(hours=random.randint(0,24), minutes=random.randint(0,59))
            self.pay_invoice(rental_id, invoice_id, current_time_process)

            current_time_process += datetime.timedelta(hours=random.randint(0,24), minutes=random.randint(0,59))
            self.confirm_invoice(rental_id, invoice_id, current_time_process, selected_inventory[0])

            current_time_process += datetime.timedelta(seconds=random.randint(30,100))
            self.confirm_rental(rental_id, current_time_process)

            # somehow an rental request for an inventory is beeing canceled
            if random.uniform(0, 1) < 0.1:
                current_time_process += datetime.timedelta(hours=random.randint(0,24), minutes=random.randint(0,59), seconds=random.randint(30,100))
                lended_inventory_id_to_cancel = list(set(random.choices(lended_inventory_ids, k=2)))[0]
                self.cancel_inventory(rental_id, lended_inventory_id_to_cancel, current_time_process, customer)
                lended_inventory_ids.remove(lended_inventory_id_to_cancel)

            if len(lended_inventory_ids) > 0:

                current_time_process += datetime.timedelta(days=random.randint(0,1), hours=random.randint(0,72), minutes=random.randint(0,59))
                self.lend_inventory(lended_inventory_ids, current_time_process, customer)

                current_time_process += datetime.timedelta(hours=random.randint(0,72), minutes=random.randint(0,59))
                inventory_ids_for_additional_invoice, current_time_process = self.return_inventory(rental_id, lended_inventory_ids, current_time_process, customer)

                if inventory_ids_for_additional_invoice:
                    current_time = current_time_process + datetime.timedelta(minutes=random.randint(0,5), seconds=random.randint(30,100))
                    additional_invoice_id = self.create_invoice(rental_id, inventory_ids_for_additional_invoice, current_time_process)
                    current_time = current_time_process + datetime.timedelta(minutes=random.randint(0,5), seconds=random.randint(30,100))
                    self.pay_invoice(rental_id, additional_invoice_id, current_time_process)
                    current_time = current_time_process + datetime.timedelta(minutes=random.randint(0,1), seconds=random.randint(30,100))
                    self.confirm_invoice(rental_id, additional_invoice_id, current_time_process, selected_inventory[0])
            
            current_time += datetime.timedelta(hours=random.randint(0,24), minutes=random.randint(0,59), seconds=random.randint(30,100))
                
    def save_table_to_csv(self):
        self.rental_orders.to_csv(self.path + 'rental_orders.csv')
        self.lended_inventory.to_csv(self.path + 'lended_inventory.csv')
        self.inspections.to_csv(self.path + 'inspections.csv')
        self.invoices.to_csv(self.path + 'invoices.csv')
        
        self.tableLog = self.tableLog.sort_values(by=['timestamp'])
        self.tableLog = self.tableLog.reset_index(drop=True)
        self.tableLog.to_csv('tableLog.csv', index=False)


if __name__ == '__main__':
    ps = ProcessSimulator()
    ps.simulate_process(datetime.datetime(year=2020, month=1, day=1))
    ps.save_table_to_csv()


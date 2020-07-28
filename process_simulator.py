import datetime
import random
import pandas as pd
import numpy as np
import progressbar

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
        self.table_log = pd.DataFrame(columns=['event_id', 'activity', 'timestamp', 'rental', 'inventory', 'customer', 'staff', 'inspection', 'invoice', 'store'])
        self.extended_table_log = pd.DataFrame(columns=['event_id', 'activity','timestamp','rental','inventory','customer','staff','inspection','invoice','store'])
        self.event_id_counter: int = 0

        # simulation time
        self.current_time: datetime.datetime

    '''
        Helper Methods
    '''

    def __get_customer_ids__(self) -> list:
        return self.customer.index.tolist()

    def __get_store_ids__(self):
        return self.store.index.tolist()

    def __get_store_of_customer__(self, customer_id: int) -> int:
        return self.customer.loc[customer_id]['store_id']

    def __get_lended_inventory_ids_of_customer__(self, customer_id) -> pd.DataFrame:
        '''

        :param customer_id: the customer
        :return: the dataframe of lended_inventory_id for a customer (all lended_inventory_ids not only the currently lended ones)
        '''
        rentals_of_customer = self.rental_orders[(self.rental_orders['customer_id'] == customer_id)].index.tolist()
        lended_inventory_of_customer = self.lended_inventory[self.lended_inventory['rental_id'].isin(rentals_of_customer)]
        return lended_inventory_of_customer

    def __get_rentals_without_invoice_from_store__(self, store_id: int) -> pd.DataFrame:
        rental_inventory_invoices_mapping = pd.merge(self.lended_inventory, self.invoices, left_on='rental_id', right_on='rental_id', how='left')
        rental_inventory_invoices_store_mapping = pd.merge(rental_inventory_invoices_mapping, self.inventory, left_on='inventory_id', right_index=True, how='left')
        open_invoices_of_store = rental_inventory_invoices_store_mapping[(rental_inventory_invoices_store_mapping['store_id'] == store_id) & (pd.isna(rental_inventory_invoices_store_mapping['value']))]
        return open_invoices_of_store

    def __get_rental_rate_for_inventory_id__(self, inventory_id: int) -> float:
        equipment_id = self.inventory.loc[inventory_id, 'equipment_id']
        return self.equipment.loc[equipment_id, 'rental_rate']

    def __get_invoices_rental_mapping__(self) -> pd.DataFrame:
        return pd.merge(self.invoices, self.rental_orders, left_on='rental_id', right_index=True, how='left')

    def __get_lended_inventory_ids_of_store__(self, store_id):
        li_inventory_mapping = pd.merge(self.lended_inventory, self.inventory, left_on='inventory_id', right_index=True, how='outer')
        return li_inventory_mapping[(li_inventory_mapping['store_id'] == store_id)]

    def __get_rentals_of_store__(self, store_id):
        rentals_store_mapping = pd.merge(self.rental_orders, self.customer, left_on='customer_id', right_index=True, how='left')
        return rentals_store_mapping[(rentals_store_mapping['store_id'] == store_id)]

    def __get_invoices_of_store__(self, store_id):
        invoices_rental_mapping = self.__get_invoices_rental_mapping__()
        invoices_rental_store_mapping = pd.merge(invoices_rental_mapping, self.customer, left_on='customer_id', right_index=True, how='left')
        return invoices_rental_store_mapping[(invoices_rental_store_mapping['store_id'] == store_id)]

    def __get_random_staff_id_for_store__(self, store_id: int) -> int:
        staff_of_store = self.staff[self.staff['store_id'] == store_id]
        return random.choice(staff_of_store.index.tolist())

    def select_available_inventory_from_store(self, store_id: int, count=2) -> list:
        inventory_of_store_ids = self.inventory[(self.inventory['store_id'] == store_id)].index.tolist()
        currently_inventories_lended_ids = self.lended_inventory[(pd.isna(self.lended_inventory['cancel_date']) & (pd.isna(self.lended_inventory['return_date'])))]['inventory_id'].values.tolist()
        available_inventory = [inventory for inventory in inventory_of_store_ids if inventory not in currently_inventories_lended_ids]
        if len(available_inventory) > 0:
            return list(set(random.choices(available_inventory, k=count)))
        else:
            return []

    def calculate_payment_for_inventory_ids(self, inventory_ids: list) -> float:
        total_invoice = []
        for inventory_id in inventory_ids:
            total_invoice.append(self.__get_rental_rate_for_inventory_id__(inventory_id))
        return round(sum(total_invoice), 2)

    def get_open_invoices_to_pay(self, customer_id):
        invoices_rental_mapping = self.__get_invoices_rental_mapping__()
        open_invoices_of_customer = invoices_rental_mapping[(invoices_rental_mapping['customer_id'] == customer_id) & (pd.isna(invoices_rental_mapping['payed_date']))]
        return open_invoices_of_customer.index.tolist()

    def select_lended_inventory_id_to_cancel(self, customer, count=1):
        lended_inventory_ids_of_customer = self.__get_lended_inventory_ids_of_customer__(customer)
        confirmed_rentals = self.rental_orders[pd.notna(self.rental_orders['confirmed_date'])].index.tolist()
        confirmed_li = lended_inventory_ids_of_customer[lended_inventory_ids_of_customer['rental_id'].isin(confirmed_rentals)]
        available_to_be_canceled = confirmed_li[(pd.isna(confirmed_li['lend_date'])) & (pd.isna(confirmed_li['cancel_date']))]
        if len(available_to_be_canceled) > 0:
            return random.choices(available_to_be_canceled.index.tolist(), k=count)
        return []

    def __create_entry_for_table_log__(self, activity: str, timestamp: datetime.datetime, store, rental='EMPTY', inventory='EMPTY', customer='EMPTY', staff='EMPTY', inspection='EMPTY', invoice='EMPTY'):
        new_entry = {'event_id': self.event_id_counter,
                     'activity': activity,
                     'timestamp': timestamp,
                     'rental': rental if len(rental) > 0 else 'EMPTY',
                     'inventory': inventory if len(inventory) > 0 else 'EMPTY',
                     'customer': customer,
                     'staff': staff,
                     'inspection': inspection if len(inspection) > 0 else 'EMPTY',
                     'invoice': invoice if len(invoice) > 0 else 'EMPTY',
                     'store': store,
                     }
        self.table_log = self.table_log.append(new_entry, ignore_index=True)

    def __create_entry_for_extended_table_log__(self, activity: str, timestamp: datetime.datetime, store, rental='EMPTY', inventory='EMPTY', customer='EMPTY', staff='EMPTY', inspection='EMPTY', invoice='EMPTY'):
        new_entry = {'event_id': self.event_id_counter,
                     'activity': activity,
                     'timestamp': timestamp,
                     'rental': rental,
                     'inventory': inventory,
                     'customer': customer,
                     'staff': staff,
                     'inspection': inspection,
                     'invoice': invoice,
                     'store': store,
                     }
        self.extended_table_log = self.extended_table_log.append(new_entry, ignore_index=True)

    def __update_progress_bar__(self):
        # updates the visualization in the terminal
        self.progressbar_widgets[1] = self.current_time.__str__()

    '''
        Defining Activities
    '''

    def create_rental(self, customer_id: int, inventory_ids: list):

        # if there are no inventories available
        if len(inventory_ids) == 0:
            return

        # create rental
        new_rental = {'customer_id': customer_id, 'created_date': self.current_time, 'confirmed_date': np.NaN}
        self.rental_orders = self.rental_orders.append(new_rental, ignore_index=True)
        rental_id = int(self.rental_orders.index.max())
        # print('Customer ' + str(customer_id) + ' created rental ' + str(rental_id) + ' on ' + date.__str__())

        store_id = self.__get_store_of_customer__(customer_id)
        for inventory in inventory_ids:
            self.__create_entry_for_extended_table_log__('create_rental', self.current_time, store_id, rental=rental_id, inventory=inventory, customer=customer_id)
        self.__create_entry_for_table_log__('create_rental', self.current_time, store_id, rental=[rental_id], inventory=inventory_ids, customer=customer_id)
        self.event_id_counter += 1

        # create entry for each inventory to lend
        for inventory_id in inventory_ids:
            new_lended_inventory = {'rental_id': rental_id, 'inventory_id': inventory_id, 'created_date': self.current_time, 'cancel_date': np.NaN, 'lend_date': np.NaN, 'return_date': np.NaN}
            self.lended_inventory = self.lended_inventory.append(new_lended_inventory, ignore_index=True)

        #print('Created rental: ' + str(rental_id) + ' by customer ' + str(customer_id))

    def create_invoice(self, store_id: int, df: pd.DataFrame, delay=datetime.timedelta(seconds=0)):

        # if there are no invoices to create
        if len(df) == 0:
            return

        staff_id = self.__get_random_staff_id_for_store__(store_id)
        time = self.current_time + delay
        invoice_ids = []
        rental_ids = set()

        rental_lended_ids_groups = df.groupby('rental_id')['inventory_id'].apply(list).reset_index()
        for index, row in rental_lended_ids_groups.iterrows():

            rental_id = row['rental_id']
            inventory_ids = row['inventory_id']
            total_invoice = self.calculate_payment_for_inventory_ids(inventory_ids)

            # create invoice
            new_invoice = {'rental_id': rental_id, 'value': total_invoice, 'created_date': time, 'staff': staff_id, 'payed_date': np.NaN, 'confirmed_date': np.NaN}
            self.invoices = self.invoices.append(new_invoice, ignore_index=True)

            invoice_id = self.invoices.index.max()
            invoice_ids.append(invoice_id)
            rental_ids.add(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('create_invoice', time, store_id, rental=rental_id, staff=staff_id, invoice=invoice_id)

        self.__create_entry_for_table_log__('create_invoice', time, store_id, rental=list(rental_ids), staff=staff_id, invoice=invoice_ids)
        self.event_id_counter += 1

        #print('Confirmed invoices: ' + str(inventory_ids) + ' by staff ' + str(staff_id))

    def pay_invoices(self, customer_id: int, invoices: list):

        # if there are no open invoices the customer has to pay
        if len(invoices) == 0:
            return

        # pay each invoice
        store_id = self.__get_store_of_customer__(customer_id)
        rental_ids = set()
        for invoice in invoices:
            self.invoices.at[invoice, 'payed_date'] = self.current_time
            rental_id = self.invoices.iloc[invoice]['rental_id']
            rental_ids.add(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('pay_invoice', self.current_time, store_id, rental=rental_id, invoice=invoice, customer=customer_id)

        self.__create_entry_for_table_log__('pay_invoice', self.current_time, store_id, rental=list(rental_ids), invoice=invoices, customer=customer_id)
        self.event_id_counter += 1

        #print('Payed invoices: ' + str(invoices) + ' by customer ' + str(customer_id))

    def confirm_invoice(self, store_id: int):
        invoices_of_store = self.__get_invoices_of_store__(store_id)
        payed_invoices_of_store = invoices_of_store[(pd.notna(invoices_of_store['payed_date']) & (pd.isna(invoices_of_store['confirmed_date_x'])))]
        invoices = payed_invoices_of_store.index.tolist()
        rental_ids = set()

        # if there is nothing to confirm
        if len(invoices) == 0:
            return

        # confirm each invoice
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        for invoice in invoices:
            self.invoices.at[invoice, 'confirmed_date'] = self.current_time
            rental_id = self.invoices.loc[invoice]['rental_id']
            rental_ids.add(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('confirm_invoice', self.current_time, store_id, rental=rental_id, invoice=invoice, staff=staff_id)

        #TODO: does it makes sense, that the staff confirms a invoice although this is not saved in the tables
        self.__create_entry_for_table_log__('confirm_invoice', self.current_time, store_id, rental=list(rental_ids), invoice=invoices, staff=staff_id)
        self.event_id_counter += 1

        #print('Confirmed invoice: ' + str(invoices) + ' by staff ' + str(staff_id))

    def confirm_rentals(self, store_id: int):
        rentals = self.__get_rentals_of_store__(store_id)
        rentals_not_confirmed = rentals[pd.isna(rentals['confirmed_date'])].index.tolist()
        confirmed_invoices_rental_ids = self.invoices[pd.notna(self.invoices['confirmed_date'])]['rental_id'].values.tolist()

        # if rental is not confirmed yet, but the invoice is confirmed
        rentals_to_confirm = [rental_id for rental_id in rentals_not_confirmed if rental_id in confirmed_invoices_rental_ids]

        # if there is nothing to confirm
        if len(rentals_to_confirm) == 0:
            return

        # confirm rentals
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        for rental in rentals_to_confirm:
            self.rental_orders.at[rental, 'confirmed_date'] = self.current_time

            # save activity in table log
            self.__create_entry_for_extended_table_log__('confirm_rental', self.current_time, store_id, rental=rental, staff=staff_id)

        #TODO: does it make sense, that the staff confirms a rental although this is not saved in the tables
        self.__create_entry_for_table_log__('confirm_rental', self.current_time, store_id, rental=rentals_to_confirm, staff=staff_id)
        self.event_id_counter += 1

        #print('Confirmed rentals: ' + str(rentals_ids) + ' by staff ' + str(staff_id))

    def cancel_inventory(self, customer_id: int, lended_inventory_ids: list):

        # if there are no lended_inventory_id to cancel
        if len(lended_inventory_ids) == 0:
            return

        inventory_ids = []
        rental_ids = []
        store_id = self.__get_store_of_customer__(customer_id)
        for lended_inventory_id in lended_inventory_ids:
            # set cancel date
            self.lended_inventory.at[lended_inventory_id, 'cancel_date'] = self.current_time

            # get information for table log entry
            inventory_id = self.lended_inventory.loc[lended_inventory_id, 'inventory_id']
            inventory_ids.append(inventory_id)
            rental_id = self.lended_inventory.loc[lended_inventory_id, 'rental_id']
            rental_ids.append(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('cancel_inventory', self.current_time, store_id, rental=rental_id, inventory=inventory_id, customer=customer_id)

        self.__create_entry_for_table_log__('cancel_inventory', self.current_time, store_id, rental=rental_ids, inventory=inventory_ids, customer=customer_id)
        self.event_id_counter += 1

        #print('Cancled inventory: ' + str(lended_inventory_id) + ' by customer ' + str(customer_id))

    def lend_inventory(self, customer_id: int):
        li = self.__get_lended_inventory_ids_of_customer__(customer_id)
        li_not_picked_up_yet = li[(pd.isna(li['lend_date']) & pd.isna(li['cancel_date']))]

        confirmed_rentals_ids = self.rental_orders[(pd.notna(self.rental_orders['confirmed_date']) & (self.rental_orders['customer_id'] == customer_id))].index.tolist()
        li_confirmed_ids = li_not_picked_up_yet[li_not_picked_up_yet['rental_id'].isin(confirmed_rentals_ids)].index.tolist()

        # if there is nothing to pick up
        if len(li_confirmed_ids) == 0:
            return

        # the customer picks everything upx
        store_id = self.__get_store_of_customer__(customer_id)
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        rental_ids = set()
        inventory_ids = []
        for lended_inventory_id in li_confirmed_ids:
            self.lended_inventory.at[lended_inventory_id, 'lend_date'] = self.current_time

            rental_id = self.lended_inventory.loc[lended_inventory_id]['rental_id']
            rental_ids.add(rental_id)
            inventory_id = self.lended_inventory.loc[lended_inventory_id]['inventory_id']
            inventory_ids.append(inventory_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('lend_inventory', self.current_time, store_id, rental=rental_id, inventory=inventory_id, customer=customer_id, staff=staff_id)

        #TODO: does it makes sense, that the staff lends inventory although this is not saved in the tables
        self.__create_entry_for_table_log__('lend_inventory', self.current_time, store_id, rental=list(rental_ids), inventory=inventory_ids, customer=customer_id, staff=staff_id)
        self.event_id_counter += 1

        #print('Lended inventory: ' + str(inventory_ids) + ' by customer ' + str(customer_id))

    def return_inventory(self, customer_id: int):
        # the customer brings everything back
        li_ids = self.__get_lended_inventory_ids_of_customer__(customer_id)
        li_to_return_up = li_ids[(pd.isna(li_ids['return_date']) & pd.notna(li_ids['lend_date'])) & ((pd.notna(li_ids['lend_date']) & pd.isna(li_ids['cancel_date'])))]
        li_to_return_ids = li_to_return_up.index.tolist()

        # if there are no inventories to return
        if len(li_to_return_ids) == 0:
            return

        store_id = self.__get_store_of_customer__(customer_id)
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        rental_ids = set()
        inventory_ids = []
        for lended_inventory_id in li_to_return_ids:
            self.lended_inventory.at[lended_inventory_id, 'return_date'] = self.current_time

            rental_id = self.lended_inventory.loc[lended_inventory_id]['rental_id']
            rental_ids.add(rental_id)
            inventory_id = self.lended_inventory.loc[lended_inventory_id]['inventory_id']
            inventory_ids.append(inventory_id)

            # create entry for future inspection
            new_inspection = {'lended_inventory_id': lended_inventory_id, 'inspector_id': np.NaN, 'inspection_date': np.NaN}
            self.inspections = self.inspections.append(new_inspection, ignore_index=True)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('return_inventory', self.current_time, store_id, rental=rental_id, inventory=inventory_id, customer=customer_id, staff=staff_id)

        self.__create_entry_for_table_log__('return_inventory', self.current_time, store_id, rental=list(rental_ids), inventory=inventory_ids, customer=customer_id, staff=staff_id)
        self.event_id_counter += 1

    def inspect_inventory(self, store_id: int) -> list:

        # all returned inventories are going to be inspected
        lended_inventory = self.__get_lended_inventory_ids_of_store__(store_id)
        returned_lended_inventory_ids = lended_inventory[(pd.notna(lended_inventory['return_date']))].index.tolist()
        inspection_ids = self.inspections[(pd.isna(self.inspections['inspection_date'])) & (self.inspections['lended_inventory_id'].isin(returned_lended_inventory_ids))].index.tolist()

        # if there are no inspections to do
        if len(inspection_ids) == 0:
            return []

        inspector_id = self.__get_random_staff_id_for_store__(store_id)
        rental_ids = set()
        inventory_ids = []

        addtional_invoices_lended_inventory_ids = []

        for inspection_id in inspection_ids:
            self.inspections.at[inspection_id, 'inspection_date'] = self.current_time

            lended_inventory_id = self.inspections.loc[inspection_id, 'lended_inventory_id']
            rental_id = self.lended_inventory.loc[lended_inventory_id, 'rental_id']
            inventory_id = self.lended_inventory.loc[lended_inventory_id, 'inventory_id']
            inventory_ids.append(inventory_id)
            rental_ids.add(rental_id)

            if random.uniform(0, 1) < 0.5:
                # inventory is brocken, additional payment is requested
                addtional_invoices_lended_inventory_ids.append(lended_inventory_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('inspect_inventories', self.current_time, store_id, rental=rental_id, inventory=inventory_id, staff=inspector_id, inspection=inspection_id)

        self.__create_entry_for_table_log__('inspect_inventories', self.current_time, store_id, rental=list(rental_ids), inventory=inventory_ids, staff=inspector_id, inspection=inspection_ids)
        self.event_id_counter += 1

        # list with rental & inventory for additional invoices
        return addtional_invoices_lended_inventory_ids

    def simulate_process(self, start_time: datetime.datetime, end_time: datetime.datetime, step: datetime.timedelta):

        self.current_time = start_time
        self.step = step
        self.small_step = (end_time - start_time).total_seconds() / step.total_seconds()
        self.progressbar_widgets = [
            ' (Simulation Time: ', self.current_time.__str__(), '/', end_time.__str__(), ') ',
            progressbar.Bar(marker='#'), progressbar.SimpleProgress(),
        ]

        print('--------------------------------------------------------------------------')
        self.bar = progressbar.ProgressBar(maxval=self.small_step, redirect_stdout=True, widgets=self.progressbar_widgets)
        self.bar.start()

        while self.current_time <= end_time:

            # iterate over list of customers
            customers = self.__get_customer_ids__()
            random.shuffle(customers)

            for customer in customers:
                decision = random.uniform(0, 1)

                if decision <= 0.1:
                    # customer selects inventory from a store to rent
                    belonging_store_id = self.__get_store_of_customer__(customer)
                    selected_inventory = self.select_available_inventory_from_store(belonging_store_id)
                    self.create_rental(customer, selected_inventory)
                elif (0.1 < decision) & (decision <= 0.35):
                    # customer pays all his open invoices
                    open_invoices = self.get_open_invoices_to_pay(customer)
                    self.pay_invoices(customer, open_invoices)
                elif (0.35 < decision) & (decision <= 0.65):
                    # somehow an rental request for an inventory is beeing canceled
                    lended_inventory_to_cancel = self.select_lended_inventory_id_to_cancel(customer)
                    self.cancel_inventory(customer, lended_inventory_to_cancel)
                else:
                    # when the customer is in the store and wants to return inventory and propably picks up other requested inventory
                    self.return_inventory(customer)
                    self.lend_inventory(customer)

            self.current_time += datetime.timedelta(seconds=self.step.total_seconds()/(len(self.store) + len(self.customer)))

        # iterate over the list of stores
            stores = self.__get_store_ids__()
            random.shuffle(stores)

            for store in stores:
                decision = random.uniform(0, 1)

                if decision <= 0.3:
                    # creating invoices for all received rental requests
                    rentals_inventory_without_invoice = self.__get_rentals_without_invoice_from_store__(store)
                    self.create_invoice(store, rentals_inventory_without_invoice)
                elif (0.3 < decision) & (decision <= 0.5):
                    self.confirm_invoice(store)
                elif (0.5 < decision) & (decision <= 0.7):
                    self.confirm_rentals(store)
                else:
                    additional_invoices_list = self.inspect_inventory(store)
                    if len(additional_invoices_list) > 0:
                        dataframe_additionnal_invoices = self.lended_inventory[(self.lended_inventory.index.isin(additional_invoices_list))]
                        self.create_invoice(store, dataframe_additionnal_invoices, delay=datetime.timedelta(minutes=1))

                self.current_time += datetime.timedelta(seconds=self.step.total_seconds()/(len(self.store) + len(self.customer)))

        self.__update_progress_bar__()
        self.bar.finish()
        
    def save_table_to_csv(self):
        self.rental_orders.to_csv(self.path + 'rental_orders.csv')
        self.lended_inventory.to_csv(self.path + 'lended_inventory.csv')
        self.inspections.to_csv(self.path + 'inspections.csv')
        self.invoices.to_csv(self.path + 'invoices.csv')

        self.table_log = self.table_log.sort_values(by=['timestamp'])
        self.table_log = self.table_log.reset_index(drop=True)
        self.table_log['event_id'] = self.table_log['event_id'].astype(int)
        self.table_log.to_csv('tableLogs/tableLog.csv', index=False)

        self.extended_table_log = self.extended_table_log.sort_values(by=['timestamp'])
        self.extended_table_log = self.extended_table_log.reset_index(drop=True)
        self.extended_table_log['event_id'] = self.extended_table_log['event_id'].astype(int)
        self.extended_table_log.to_csv('tableLogs/extended_tableLog.csv', index=False)


if __name__ == '__main__':

    start = datetime.datetime(year=2020, month=1, day=1, hour=8)
    end = datetime.datetime(year=2020, month=1, day=2, hour=1)
    step = datetime.timedelta(hours=1)

    ps = ProcessSimulator()
    ps.simulate_process(start, end, step)
    ps.save_table_to_csv()



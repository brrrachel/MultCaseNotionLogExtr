import datetime
import random
from optparse import OptionParser
import numpy as np
import pandas as pd
from colorama import init, Fore

init()  # for coloring the outputs


class ProcessSimulator:

    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime, step_size: datetime.timedelta):
        self.path = 'generatedData/'

        # load available data
        self.address = pd.read_csv(self.path + 'address.csv', index_col=0)
        self.brand = pd.read_csv(self.path + 'brand.csv', index_col=0)
        self.customer = pd.read_csv(self.path + 'customer.csv', index_col=0)
        self.equipment = pd.read_csv(self.path + 'equipment.csv', index_col=0)
        self.inventory = pd.read_csv(self.path + 'inventory.csv', index_col=0)
        self.staff = pd.read_csv(self.path + 'staff.csv', index_col=0)
        self.store = pd.read_csv(self.path + 'store.csv', index_col=0)

        # set time related variables
        self.current_time: datetime.datetime = start_time
        self.step: datetime.timedelta = step_size
        self.end_time: datetime.datetime = end_time
        self.current_time: datetime.datetime

        # create additional tables
        self.rental_orders = pd.DataFrame(columns=['customer_id', 'created_date', 'confirmed_date', 'confirmed_staff'])
        self.loaned_inventory = pd.DataFrame(
            columns=['rental_id', 'inventory_id', 'created_date', 'cancel_date', 'lend_date', 'lend_staff',
                     'return_date', 'return_staff'])
        self.inspections = pd.DataFrame(
            columns=['inspector', 'inspection_date', 'loaned_inventory_id'])  # inspector == staff
        self.invoices = pd.DataFrame(
            columns=['rental_id', 'value', 'created_date', 'created_staff', 'payed_date', 'confirmed_date',
                     'confirmed_staff'])

        # create table log
        self.table_log = pd.DataFrame(
            columns=['event_id', 'activity', 'timestamp', 'rental', 'inventory', 'customer', 'staff', 'inspection',
                     'invoice'])
        self.extended_table_log = pd.DataFrame(
            columns=['event_id', 'activity', 'timestamp', 'rental', 'inventory', 'customer', 'staff', 'inspection',
                     'invoice'])
        self.event_id_counter: int = 0

    """
        Helper Methods
    """

    def __get_customer_ids__(self) -> list:
        return self.customer.index.tolist()

    def __get_store_ids__(self) -> list:
        return self.store.index.tolist()

    def __get_store_of_customer__(self, customer_id: int) -> int:
        return self.customer.loc[customer_id]['store_id']

    def __get_loaned_inventory_ids_of_customer__(self, customer_id) -> pd.DataFrame:
        """
        :return: Dataframe with all inventories for the requested customer.
        """
        rentals_of_customer = self.rental_orders[(self.rental_orders['customer_id'] == customer_id)].index.tolist()
        loaned_inventory_of_customer = self.loaned_inventory[
            self.loaned_inventory['rental_id'].isin(rentals_of_customer)]
        return loaned_inventory_of_customer

    def __get_rentals_without_invoice_from_store__(self, store_id: int) -> pd.DataFrame:
        """
        :return: Dataframe with all invoices which have to be created for the requested store.
        """
        rental_inventory_invoices_mapping = pd.merge(self.loaned_inventory, self.invoices, left_on='rental_id',
                                                     right_on='rental_id', how='left')
        rental_inventory_invoices_store_mapping = pd.merge(rental_inventory_invoices_mapping, self.inventory,
                                                           left_on='inventory_id', right_index=True, how='left')
        open_invoices_of_store = rental_inventory_invoices_store_mapping[
            (rental_inventory_invoices_store_mapping['store_id'] == store_id) & (
                pd.isna(rental_inventory_invoices_store_mapping['value']))]
        return open_invoices_of_store

    def __get_rental_rate_for_inventory_id__(self, inventory_id: int) -> float:
        equipment_id = self.inventory.loc[inventory_id, 'equipment_id']
        return self.equipment.loc[equipment_id, 'rental_rate']

    def __get_random_staff_id_for_store__(self, store_id: int) -> int:
        staff_of_store = self.staff[self.staff['store_id'] == store_id]
        return random.choice(staff_of_store.index.tolist())

    def __get_loaned_inventory_ids_of_store__(self, store_id) -> pd.DataFrame:
        """
        :return: Dataframe with all inventories of the requested which are lended currently.
        """
        li_inventory_mapping = pd.merge(self.loaned_inventory, self.inventory,
                                        left_on='inventory_id', right_index=True, how='outer')
        return li_inventory_mapping[(li_inventory_mapping['store_id'] == store_id)]

    def __get_rentals_of_store__(self, store_id) -> pd.DataFrame:
        """
        :return: Dataframe with all rentals for the requested store.
        """
        rentals_store_mapping = pd.merge(self.rental_orders, self.customer,
                                         left_on='customer_id', right_index=True, how='left')
        return rentals_store_mapping[(rentals_store_mapping['store_id'] == store_id)]

    def __get_invoices_rental_mapping__(self) -> pd.DataFrame:
        """
        :return: Merged dataframe, where we map from each invoice to their rental entry.
        """
        return pd.merge(self.invoices, self.rental_orders, left_on='rental_id', right_index=True, how='left')

    def __get_invoices_of_store__(self, store_id) -> pd.DataFrame:
        """
        :return: Merged dataframe, where we map invoice with their rental information and add the customer information.
        """
        invoices_rental_mapping = self.__get_invoices_rental_mapping__()
        invoices_rental_store_mapping = pd.merge(invoices_rental_mapping, self.customer,
                                                 left_on='customer_id', right_index=True, how='left')
        return invoices_rental_store_mapping[(invoices_rental_store_mapping['store_id'] == store_id)]

    def select_available_inventory_from_store(self, store_id: int, count=2) -> list:
        inventory_of_store_ids = self.inventory[(self.inventory['store_id'] == store_id)].index.tolist()
        not_inspected_loaned_inventories = self.inspections[pd.isna(self.inspections['inspection_date'])][
            'loaned_inventory_id'].values.tolist()
        currently_inventories_loaned_ids = self.loaned_inventory[
            ((pd.isna(self.loaned_inventory['cancel_date']) & pd.isna(self.loaned_inventory['return_date'])) |
             (pd.notna(self.loaned_inventory['return_date']) & self.loaned_inventory.index.isin(
                 not_inspected_loaned_inventories)))][
            'inventory_id'].values.tolist()
        available_inventory = [inventory for inventory in inventory_of_store_ids if
                               inventory not in currently_inventories_loaned_ids]
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
        open_invoices_of_customer = invoices_rental_mapping[
            (invoices_rental_mapping['customer_id'] == customer_id) & (pd.isna(invoices_rental_mapping['payed_date']))]
        return open_invoices_of_customer.index.tolist()

    def select_loaned_inventory_id_to_cancel(self, customer, count=1):
        loaned_inventory_ids_of_customer = self.__get_loaned_inventory_ids_of_customer__(customer)
        confirmed_rentals = self.rental_orders[pd.notna(self.rental_orders['confirmed_date'])].index.tolist()
        confirmed_li = loaned_inventory_ids_of_customer[
            loaned_inventory_ids_of_customer['rental_id'].isin(confirmed_rentals)]
        available_to_be_canceled = confirmed_li[
            (pd.isna(confirmed_li['lend_date'])) & (pd.isna(confirmed_li['cancel_date']))]
        if len(available_to_be_canceled) > 0:
            return random.choices(available_to_be_canceled.index.tolist(), k=count)
        return []

    def __get_total_number_of_loaned_inventories__(self) -> int:
        return len(self.loaned_inventory)

    def __get_total_number_of_cancelled_inventories(self) -> int:
        return len(self.loaned_inventory[pd.notna(self.loaned_inventory['cancel_date'])])

    def __get_total_number_of_inspected_inventories__(self) -> int:
        return len(self.inspections[pd.notna(self.inspections['inspection_date'])])

    def __rentals_finished__(self) -> bool:
        return self.__get_total_number_of_loaned_inventories__() == (
                self.__get_total_number_of_cancelled_inventories() + self.__get_total_number_of_inspected_inventories__())

    def __invoices_confirmed__(self) -> bool:
        return len(self.invoices[pd.notna(self.invoices['confirmed_date'])]) == len(self.invoices)

    """
        Methods to create the table representation of an XOC log.
    """

    def __create_entry_for_table_log__(self, activity: str, timestamp: datetime.datetime, rental='EMPTY',
                                       inventory='EMPTY', customer='EMPTY', staff='EMPTY', inspection='EMPTY',
                                       invoice='EMPTY'):
        """
        A XOC Log represented as a table.
        """
        new_entry = {'event_id': self.event_id_counter,
                     'activity': activity,
                     'timestamp': timestamp,
                     'rental': rental if len(rental) > 0 else 'EMPTY',
                     'inventory': inventory if len(inventory) > 0 else 'EMPTY',
                     'customer': customer,
                     'staff': staff,
                     'inspection': inspection if len(inspection) > 0 else 'EMPTY',
                     'invoice': invoice if len(invoice) > 0 else 'EMPTY'
                     }
        self.table_log = self.table_log.append(new_entry, ignore_index=True)

    def __create_entry_for_extended_table_log__(self, activity: str, timestamp: datetime.datetime, rental='EMPTY',
                                                inventory='EMPTY', customer='EMPTY', staff='EMPTY', inspection='EMPTY',
                                                invoice='EMPTY'):
        """
        An extended table log is where each line in the table has exactly one value. Events where multiple objects are
        involved have multiple enntries within the dataframe. This extended table log makes it easier for deriving the
        different case notions using the object type projection. This representation is just used for internal work.
        """
        new_entry = {'event_id': self.event_id_counter,
                     'activity': activity,
                     'timestamp': timestamp,
                     'rental': rental,
                     'inventory': inventory,
                     'customer': customer,
                     'staff': staff,
                     'inspection': inspection,
                     'invoice': invoice
                     }
        self.extended_table_log = self.extended_table_log.append(new_entry, ignore_index=True)

    """
        Defining Activities
    """

    def create_rental(self, customer_id: int, inventory_ids: list):

        # if there are no inventories available
        if len(inventory_ids) == 0:
            return

        # create rental
        new_rental = {'customer_id': customer_id, 'created_date': self.current_time, 'confirmed_date': np.NaN}
        self.rental_orders = self.rental_orders.append(new_rental, ignore_index=True)
        rental_id = int(self.rental_orders.index.max())

        # save event also in the table log
        for inventory in inventory_ids:
            self.__create_entry_for_extended_table_log__('create_rental', self.current_time, rental=str(rental_id),
                                                         inventory=inventory, customer=str(customer_id))
        self.__create_entry_for_table_log__('create_rental', self.current_time, rental=str([rental_id]),
                                            inventory=str(inventory_ids), customer=str(customer_id))
        self.event_id_counter += 1

        # create entry for each inventory to lend
        for inventory_id in inventory_ids:
            new_loaned_inventory = {'rental_id': rental_id, 'inventory_id': inventory_id,
                                    'created_date': self.current_time, 'cancel_date': np.NaN, 'lend_date': np.NaN,
                                    'return_date': np.NaN}
            self.loaned_inventory = self.loaned_inventory.append(new_loaned_inventory, ignore_index=True)

    def create_invoice(self, store_id, df: pd.DataFrame, delay=datetime.timedelta(seconds=0)):

        # if there are no invoices to create
        if len(df) == 0:
            return

        staff_id = self.__get_random_staff_id_for_store__(store_id)
        time = self.current_time + delay
        invoice_ids = []
        rental_ids = set()

        rental_loaned_ids_groups = df.groupby('rental_id')['inventory_id'].apply(list).reset_index()
        for index, row in rental_loaned_ids_groups.iterrows():
            rental_id = row['rental_id']
            inventory_ids = row['inventory_id']
            total_invoice = self.calculate_payment_for_inventory_ids(inventory_ids)

            # create invoice
            new_invoice = {'rental_id': rental_id, 'value': total_invoice, 'created_date': time,
                           'created_staff': staff_id, 'payed_date': np.NaN, 'confirmed_date': np.NaN,
                           'confirmed_staff': np.NaN}
            self.invoices = self.invoices.append(new_invoice, ignore_index=True)

            invoice_id = self.invoices.index.max()
            invoice_ids.append(invoice_id)
            rental_ids.add(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('create_invoice', time, rental=rental_id, staff=str(staff_id),
                                                         invoice=invoice_id)

        self.__create_entry_for_table_log__('create_invoice', time, rental=str(list(rental_ids)), staff=str(staff_id),
                                            invoice=str(invoice_ids))
        self.event_id_counter += 1

    def pay_invoices(self, customer_id: int, invoices: list):

        # if there are no open invoices the customer has to pay
        if len(invoices) == 0:
            return

        # pay each invoice
        rental_ids = set()
        for invoice in invoices:
            self.invoices.at[invoice, 'payed_date'] = self.current_time
            rental_id = self.invoices.iloc[invoice]['rental_id']
            rental_ids.add(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('pay_invoice', self.current_time, invoice=invoice,
                                                         customer=str(customer_id))

        self.__create_entry_for_table_log__('pay_invoice', self.current_time, invoice=str(invoices),
                                            customer=str(customer_id))
        self.event_id_counter += 1

    def confirm_invoice(self, store_id: int):
        invoices_of_store = self.__get_invoices_of_store__(store_id)
        payed_invoices_of_store = invoices_of_store[
            (pd.notna(invoices_of_store['payed_date']) & (pd.isna(invoices_of_store['confirmed_date_x'])))]
        invoices = payed_invoices_of_store.index.tolist()
        rental_ids = set()

        # if there is nothing to confirm
        if len(invoices) == 0:
            return

        # confirm each invoice
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        for invoice in invoices:
            self.invoices.at[invoice, 'confirmed_date'] = self.current_time
            self.invoices.at[invoice, 'confirmed_staff'] = staff_id
            rental_id = self.invoices.loc[invoice]['rental_id']
            rental_ids.add(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('confirm_invoice', self.current_time, invoice=invoice,
                                                         staff=str(staff_id), rental=str(rental_id))

        self.__create_entry_for_table_log__('confirm_invoice', self.current_time, invoice=invoices, staff=str(staff_id))
        self.event_id_counter += 1

    def confirm_rentals(self, store_id: int):
        rentals = self.__get_rentals_of_store__(store_id)
        rentals_not_confirmed = rentals[pd.isna(rentals['confirmed_date'])].index.tolist()
        confirmed_invoices_rental_ids = self.invoices[pd.notna(self.invoices['confirmed_date'])][
            'rental_id'].values.tolist()

        # if rental are not confirmed yet, but the invoice is confirmed
        rentals_to_confirm = [rental_id for rental_id in rentals_not_confirmed if
                              rental_id in confirmed_invoices_rental_ids]

        # if there is nothing to confirm
        if len(rentals_to_confirm) == 0:
            return

        # confirm rentals
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        for rental in rentals_to_confirm:
            self.rental_orders.at[rental, 'confirmed_date'] = self.current_time
            self.rental_orders.at[rental, 'confirmed_staff'] = staff_id

            # save activity in table log
            self.__create_entry_for_extended_table_log__('confirm_rental', self.current_time, rental=rental,
                                                         staff=str(staff_id))

        self.__create_entry_for_table_log__('confirm_rental', self.current_time, rental=str(rentals_to_confirm),
                                            staff=str(staff_id))
        self.event_id_counter += 1

    def cancel_inventory(self, customer_id: int, loaned_inventory_ids: list):

        # if there are no inventories to cancel
        if len(loaned_inventory_ids) == 0:
            return

        inventory_ids = []
        rental_ids = []
        for loaned_inventory_id in loaned_inventory_ids:
            # set cancel date
            self.loaned_inventory.at[loaned_inventory_id, 'cancel_date'] = self.current_time

            # get information for table log entry
            inventory_id = self.loaned_inventory.loc[loaned_inventory_id, 'inventory_id']
            inventory_ids.append(inventory_id)
            rental_id = self.loaned_inventory.loc[loaned_inventory_id, 'rental_id']
            rental_ids.append(rental_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('cancel_inventory', self.current_time, rental=rental_id,
                                                         inventory=inventory_id, customer=str(customer_id))

        self.__create_entry_for_table_log__('cancel_inventory', self.current_time, rental=str(rental_ids),
                                            inventory=str(inventory_ids), customer=str(customer_id))
        self.event_id_counter += 1

    def lend_inventory(self, customer_id: int):
        li = self.__get_loaned_inventory_ids_of_customer__(customer_id)
        li_not_picked_up_yet = li[(pd.isna(li['lend_date']) & pd.isna(li['cancel_date']))]

        confirmed_rentals_ids = self.rental_orders[(pd.notna(self.rental_orders['confirmed_date']) & (
                self.rental_orders['customer_id'] == customer_id))].index.tolist()
        li_confirmed_ids = li_not_picked_up_yet[
            li_not_picked_up_yet['rental_id'].isin(confirmed_rentals_ids)].index.tolist()

        # if there is nothing to pick up
        if len(li_confirmed_ids) == 0:
            return

        # the customer picks everything upx
        store_id = self.__get_store_of_customer__(customer_id)
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        rental_ids = set()
        inventory_ids = []
        for loaned_inventory_id in li_confirmed_ids:
            # mark the inventory as loaned
            self.loaned_inventory.at[loaned_inventory_id, 'lend_date'] = self.current_time
            self.loaned_inventory.at[loaned_inventory_id, 'lend_staff'] = staff_id

            rental_id = self.loaned_inventory.loc[loaned_inventory_id]['rental_id']
            rental_ids.add(rental_id)
            inventory_id = self.loaned_inventory.loc[loaned_inventory_id]['inventory_id']
            inventory_ids.append(inventory_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('lend_inventory', self.current_time, rental=rental_id,
                                                         inventory=inventory_id, customer=str(customer_id),
                                                         staff=str(staff_id))

        self.__create_entry_for_table_log__('lend_inventory', self.current_time, rental=str(list(rental_ids)),
                                            inventory=str(inventory_ids), customer=str(customer_id),
                                            staff=str(staff_id))
        self.event_id_counter += 1

    def return_inventory(self, customer_id: int):
        # the customer brings not everything back
        li_ids = self.__get_loaned_inventory_ids_of_customer__(customer_id)
        li_to_return_up = li_ids[(pd.isna(li_ids['return_date']) & pd.notna(li_ids['lend_date'])) & (
            (pd.notna(li_ids['lend_date']) & pd.isna(li_ids['cancel_date'])))]
        li_to_return_ids = li_to_return_up.index.tolist()
        li_to_return_ids = [li for li in li_to_return_ids if random.uniform(0, 1) < 0.5]

        # if there are no inventories to return
        if len(li_to_return_ids) == 0:
            return

        store_id = self.__get_store_of_customer__(customer_id)
        staff_id = self.__get_random_staff_id_for_store__(store_id)
        rental_ids = set()
        inventory_ids = []
        for loaned_inventory_id in li_to_return_ids:
            # mark an inventory as returned
            self.loaned_inventory.at[loaned_inventory_id, 'return_date'] = self.current_time
            self.loaned_inventory.at[loaned_inventory_id, 'return_staff'] = staff_id

            rental_id = self.loaned_inventory.loc[loaned_inventory_id]['rental_id']
            rental_ids.add(rental_id)
            inventory_id = self.loaned_inventory.loc[loaned_inventory_id]['inventory_id']
            inventory_ids.append(inventory_id)

            # create entry for future inspection
            new_inspection = {'loaned_inventory_id': loaned_inventory_id, 'inspector_id': np.NaN,
                              'inspection_date': np.NaN}
            self.inspections = self.inspections.append(new_inspection, ignore_index=True)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('return_inventory', self.current_time, rental=rental_id,
                                                         inventory=inventory_id, customer=str(customer_id),
                                                         staff=str(staff_id))
        self.__create_entry_for_table_log__('return_inventory', self.current_time, rental=str(list(rental_ids)),
                                            inventory=str(inventory_ids), customer=str(customer_id),
                                            staff=str(staff_id))
        self.event_id_counter += 1

    def inspect_inventory(self, store_id: int) -> list:

        # all returned inventories are going to be inspected
        loaned_inventory = self.__get_loaned_inventory_ids_of_store__(store_id)
        returned_loaned_inventory_ids = loaned_inventory[(pd.notna(loaned_inventory['return_date']))].index.tolist()
        inspection_ids = self.inspections[(pd.isna(self.inspections['inspection_date'])) & (
            self.inspections['loaned_inventory_id'].isin(returned_loaned_inventory_ids))].index.tolist()

        # if there are no inspections to do
        if len(inspection_ids) == 0:
            return []

        inspector_id = self.__get_random_staff_id_for_store__(store_id)
        rental_ids = set()
        inventory_ids = []

        additional_invoices_loaned_inventory_ids = []

        for inspection_id in inspection_ids:

            # mark an inventory as inspected
            self.inspections.at[inspection_id, 'inspection_date'] = self.current_time
            self.inspections.at[inspection_id, 'inspector'] = inspection_id

            loaned_inventory_id = self.inspections.loc[inspection_id, 'loaned_inventory_id']
            rental_id = self.loaned_inventory.loc[loaned_inventory_id, 'rental_id']
            inventory_id = self.loaned_inventory.loc[loaned_inventory_id, 'inventory_id']
            inventory_ids.append(inventory_id)
            rental_ids.add(rental_id)

            if random.uniform(0, 1) < 0.5:
                # inventory is broken, additional payment is requested
                additional_invoices_loaned_inventory_ids.append(loaned_inventory_id)

            # save activity in table log
            self.__create_entry_for_extended_table_log__('inspect_inventories', self.current_time, rental=rental_id,
                                                         inventory=inventory_id, staff=str(inspector_id),
                                                         inspection=inspection_id)
        self.__create_entry_for_table_log__('inspect_inventories', self.current_time, rental=str(list(rental_ids)),
                                            inventory=str(inventory_ids), staff=str(inspector_id),
                                            inspection=inspection_ids)
        self.event_id_counter += 1

        # list with rental & inventory for additional invoices
        return additional_invoices_loaned_inventory_ids

    def __proceed_time__(self):
        self.current_time += datetime.timedelta(
            seconds=int(self.step.total_seconds() / (len(self.store) + len(self.customer))))

    def simulate_process(self):

        while (self.current_time > self.end_time and not (
                self.__rentals_finished__() and self.__invoices_confirmed__())) or (self.current_time <= self.end_time):
            print('(Simulation Time: {0}/{1})'.format(self.current_time, self.end_time), end="\r")

            # iterate over list of customers
            customers = self.__get_customer_ids__()
            random.shuffle(customers)

            for customer in customers:
                decision = random.uniform(0, 1)

                if decision <= 0.1 and self.current_time <= self.end_time:
                    # customer selects inventory from a store to rent
                    belonging_store_id = self.__get_store_of_customer__(customer)
                    selected_inventory = self.select_available_inventory_from_store(belonging_store_id)
                    self.create_rental(customer, selected_inventory)
                elif (0.1 < decision) & (decision <= 0.35):
                    # customer pays all his open invoices
                    open_invoices = self.get_open_invoices_to_pay(customer)
                    self.pay_invoices(customer, open_invoices)
                elif (0.35 < decision) & (decision <= 0.65):
                    # somehow an rental request for an inventory is being canceled
                    loaned_inventory_to_cancel = self.select_loaned_inventory_id_to_cancel(customer)
                    self.cancel_inventory(customer, loaned_inventory_to_cancel)
                else:
                    # when the customer is in the store and wants to return inventory and probably picks up
                    # other requested inventory
                    self.return_inventory(customer)
                    self.lend_inventory(customer)

                self.__proceed_time__()

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
                    # confirm all payed invoices
                    self.confirm_invoice(store)
                elif (0.5 < decision) & (decision <= 0.7):
                    # confirm all confirmed invoices
                    self.confirm_rentals(store)
                else:
                    # inspect all recently returned inventories and create if necessary additional invoices
                    additional_invoices_list = self.inspect_inventory(store)
                    if len(additional_invoices_list) > 0:
                        data_frame_additional_invoices = self.loaned_inventory[
                            (self.loaned_inventory.index.isin(additional_invoices_list))]
                        self.create_invoice(store, data_frame_additional_invoices, delay=datetime.timedelta(seconds=1))

                self.__proceed_time__()

    def save_table_to_csv(self):
        self.rental_orders.to_csv(self.path + 'rental_orders.csv')
        self.loaned_inventory.to_csv(self.path + 'loaned_inventory.csv')
        self.inspections.to_csv(self.path + 'inspections.csv')
        self.invoices.to_csv(self.path + 'invoices.csv')
        print(Fore.GREEN, 'Finished: database tables can be found here: ', 'generatedData/')

        self.table_log = self.table_log.sort_values(by=['timestamp'])
        self.table_log = self.table_log.reset_index(drop=True)
        self.table_log['event_id'] = self.table_log['event_id'].astype(int)
        self.table_log.to_csv('tableLogs/tableLog.csv', index=False)

        self.extended_table_log = self.extended_table_log.sort_values(by=['timestamp'])
        self.extended_table_log = self.extended_table_log.reset_index(drop=True)
        self.extended_table_log['event_id'] = self.extended_table_log['event_id'].astype(int)
        self.extended_table_log.to_csv('tableLogs/extended_tableLog.csv', index=False)

        print(Fore.GREEN, 'Finished: table logs can be found here: ', 'tableLogs/')


if __name__ == '__main__':
    # declare all options
    parser = OptionParser()
    parser.add_option("-i", dest="interval", help="Interval steps for simulation [Hours], default = 1 h", default=1,
                      type="int", action="store")
    parser.add_option("-s", "--start", dest="start",
                      help="Set Start date to limit data [YYYY/MM/DD hh:mm], default = 2020/01/01 08:00",
                      action="store", default="2020/01/01 08:00", type="str")
    parser.add_option("-e", "--end", dest="end",
                      help="Set Start date to limit data [YYYY/MM/DD hh:mm], default = 2020/01/31 17:00",
                      action="store", default="2020/01/31 17:00", type="str")
    (options, args) = parser.parse_args()

    # parse options
    start = datetime.datetime.strptime(options.start, "%Y/%m/%d %H:%M")
    end = datetime.datetime.strptime(options.end, "%Y/%m/%d %H:%M")
    step = datetime.timedelta(hours=options.interval)

    print('Start Time:', start)
    print('End Time:', end)
    print('Step Size', step)

    # start simulator
    ps = ProcessSimulator(start, end, step)
    ps.simulate_process()
    ps.save_table_to_csv()

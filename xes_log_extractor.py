import warnings
import pandas as pd
import sys
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.objects.log.log import EventLog
from pm4py.util import constants
from tqdm import tqdm
from colorama import init, Fore
warnings.filterwarnings("ignore", category=DeprecationWarning)
init()


class XESLogExtractor:

    def __init__(self, case_notion_columns):
        self.event_log: EventLog = self.__create_xes_file__(case_notion_columns)
        self.case_notion: str = ''.join(case_notion_columns)

    def get_case_ids(self, log, column) -> list:
        return list(set(log[column].values.tolist()))

    def merge_event_attributes(self, log, case_notion):
        case_ids = self.get_case_ids(log, case_notion)

        merged_log = pd.DataFrame(columns=log.columns)
        for case in tqdm(case_ids):
            event_ids = list(set(log[(log[case_notion] == case)]['event_id'].values.tolist()))
            for event in event_ids:
                event_attributes = self.get_case_attributes(log, case_notion, event, case)
                merged_log = merged_log.append(event_attributes, ignore_index=True, sort=True)
        return merged_log

    def get_case_attributes(self, log, case_notion, event_id, case_id) -> dict:
        filtered = log[(log['event_id'] == event_id) & (log[case_notion] == case_id)]
        if len(filtered) == 1:
            event_attributes = filtered.reset_index(drop=True).to_dict('records')[0]
            return event_attributes
        else:
            event_attributes = {}
            for column in filtered.columns:
                if column in ['event_id', 'activity', 'timestamp', case_notion]:
                    event_attributes[column] = filtered.iloc[0][column]
                else:
                    # get all involved objects of the event
                    column_value = list(set(filtered[column].values.tolist()))
                    event_attributes[column] = str(column_value) if len(column_value) > 1 else column_value[0]
            return event_attributes

    def __create_xes_file__(self, case_notion_columns,
                            extended_table_log_path='tableLogs/extended_tableLog.csv') -> EventLog:

        # load extended table log
        self.extended_table_log = csv_import_adapter.import_dataframe_from_path(extended_table_log_path, sep=",")

        # if there were not enough columns selected or to much
        if (len(case_notion_columns) > 2) or (len(case_notion_columns) == 0):
            print(Fore.RED + 'Error: It is necessary to select one or two object types in order to be able to derive a XES '
                             'Log file.')
            print(Fore.RED + 'You need to choose them from the following list:',
                  self.extended_table_log.columns.tolist()[3:])
            exit(0)

        # the final log in form of a pandas DataFrame
        log = pd.DataFrame(columns=self.extended_table_log.columns)

        def is_slice_in_list(list1, list2):
            return all(elem in list2 for elem in list1)

        # check weather all column names exist in the table
        if not is_slice_in_list(case_notion_columns, self.extended_table_log.columns):
            print(Fore.RED + 'Error: (Some) Object type may not exist.')
            print(Fore.RED + 'You need to choose them from the following list:',
                  self.extended_table_log.columns.tolist()[3:])
            exit(0)

        if len(case_notion_columns) > 1:  # if multiple columns should be considered as one case notion
            print(Fore.YELLOW, 'Info: You are using the multiple object type projection.')
            print(Fore.WHITE)

            # derive the case notion based on two object types
            case_notion = self.get_combined_case_notion(case_notion_columns)

            # map new case id on the combination of unique columns
            columns = case_notion.columns
            combined_case_notion_log = self.extended_table_log
            for index, row in case_notion.iterrows():
                combined_case_notion_log.loc[((combined_case_notion_log[columns[0]] == row[columns[0]]) & (
                        combined_case_notion_log[columns[1]] == row[columns[1]])), 'case:concept:name'] = row[
                    columns[2]]

            # merge attributes
            log = self.merge_event_attributes(combined_case_notion_log, 'case:concept:name')

            # rename the columns for preparing the xes log
            log['event_id'] = log['event_id'].astype(str)
            columns_to_rename = {'timestamp': 'time:timestamp', 'activity': 'concept:name'}
            log.rename(columns=columns_to_rename, inplace=True)

        else:  # if only one column is considered as a case notion
            print(Fore.YELLOW, 'Info: You are using the object type projection.')
            print(Fore.WHITE)

            # get events for selected case notion
            log = self.merge_event_attributes(self.extended_table_log, case_notion_columns[0])

            # rename the columns for preparing the xes log
            log['event_id'] = log['event_id'].astype(str)
            columns_to_rename = {case_notion_columns[0]: 'case:concept:name',
                                 'timestamp': 'time:timestamp',
                                 'activity': 'concept:name',
                                 'lifecycle': 'lifecycle:transition'}
            log.rename(columns=columns_to_rename, inplace=True)
            log['case:concept:name'] = log['case:concept:name'].astype(str)

        # remove all empty values for the case id from the log
        log = log[log['case:concept:name'] != 'EMPTY']
        log = log.dropna()

        # convert to xes format
        parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "case:concept:name",
                      constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
                      constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"}

        log = log.sort_values(by=['case:concept:name', 'time:timestamp'])
        return conversion_factory.apply(log, parameters=parameters)

    def get_combined_case_notion(self, case_notion_columns):

        # get all unique combinations of the column values
        extracted = self.extended_table_log[case_notion_columns].values.tolist()
        unique = list(set(tuple(combination) for combination in extracted))
        filtered = [combination for combination in unique if 'EMPTY' not in combination]

        # create a table to map the unique combinations to a new case id
        case_notion = pd.DataFrame(filtered).rename(columns={0: case_notion_columns[0], 1: case_notion_columns[1]})
        case_notion['case:concept:name'] = case_notion.index.astype(str)

        return case_notion

    def xes_to_disk(self):
        path = 'xesLogs/xes_' + self.case_notion + '.xes'
        xes_exporter.apply(self.event_log, path)
        print(Fore.GREEN, 'Finished: Extracted XES log file can be found here: ', path)


if __name__ == '__main__':
    log_extractor = XESLogExtractor(sys.argv[1:])
    log_extractor.xes_to_disk()

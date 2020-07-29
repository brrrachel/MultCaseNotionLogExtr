import pandas as pd
from tqdm import tqdm
from pm4py.objects.log.log import EventLog
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.util import constants
from pm4py.objects.log.adapters.pandas import csv_import_adapter


class XESLogTool:

    def __init__(self, case_notion_columns: list):
        self.case_notion = ''.join(case_notion_columns)
        self.event_log: EventLog = self.__create_xes_file__(case_notion_columns)
    
    def __create_xes_file__(self, case_notion_columns, extended_tablelog_path ='tableLogs/extended_tableLog.csv') -> EventLog:

        # load extended table log
        self.extended_tablelog = csv_import_adapter.import_dataframe_from_path(extended_tablelog_path, sep=",")

        # the final log in form of a pandas DataFrame
        log = pd.DataFrame(columns=self.extended_tablelog.columns)
        
        
        

        def is_slice_in_list(list1, list2):
                return all(elem in list2 for elem in list1)

        # check weather all column names exist in the table
        if not is_slice_in_list(case_notion_columns, self.extended_tablelog.columns):
            print('Error: (Some) Columns may not exist.')
            exit(0)

        if len(case_notion_columns) > 1:  # if multiple columns should be considered as one case notion
            exit(0)
            '''
            case_notion = self.get_case_notion(case_notion_columns)

            # map new case id on the combination of unqiue columns
            dataframe = pd.concat([self.tableLog, case_notion], axis=1, join='outer')

            # rename the columns for preparing the xes log
            columns_to_rename = {'timestamp': 'time:timestamp', 'activity': 'concept:name'}
            dataframe.rename(columns=columns_to_rename, inplace=True)
            '''

        else:  # if only one column is considered as a case notion

            # get case ids
            case_ids = self.get_case_ids(case_notion_columns[0])

            # get events for selected case notion
            for case in tqdm(case_ids):
                event_ids = list(set(self.extended_tablelog[(self.extended_tablelog[case_notion_columns[0]] == case)]['event_id'].values.tolist()))
                for event in event_ids:
                    event_attributes = self.get_case_attributes(case_notion_columns[0], event, case)
                    log = log.append(event_attributes, ignore_index=True, sort=True)

            # rename the columns for preparing the xes log
            
            log['store'] = log['store'].astype(str)
            log['event_id'] = log['event_id'].astype(str)
            
            columns_to_rename = {case_notion_columns[0]: 'case:concept:name',
                                 'timestamp': 'time:timestamp',
                                 'activity': 'concept:name',
                                 'lifecycle': 'lifecycle:transition'}
            log.rename(columns=columns_to_rename, inplace=True)
            
            log = log[log['case:concept:name'] != 'EMPTY']
            
            log['case:concept:name'] = log['case:concept:name'].astype(str)

        # convert to xes format
        parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "case:concept:name",
                      constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
                      constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"}

        log = log.sort_values(by=['case:concept:name', 'time:timestamp'])
        return conversion_factory.apply(log, parameters=parameters)

    def get_case_ids(self, column) -> list:
        return list(set(self.extended_tablelog[column].values.tolist()))

    def get_case_attributes(self, case_notion, event_id, case_id) -> dict:
        filtered = self.extended_tablelog[(self.extended_tablelog['event_id'] == event_id) & (self.extended_tablelog[case_notion] == case_id)]
        if len(filtered) == 1:
            event_attributes = filtered.reset_index(drop=True).to_dict('records')[0]
            return event_attributes
        else:
            event_attributes = {}
            for column in filtered.columns:
                if column in ['event_id', 'activity', 'timestamp', case_notion, 'lifecycle']:
                    event_attributes[column] = filtered.iloc[0][column]
                else:
                    # get all involved objects of the event
                    column_value = list(set(filtered[column].values.tolist()))
                    event_attributes[column] = str(column_value) if len(column_value) > 1 else column_value[0]
            return event_attributes

    '''
    def get_case_notion(self, case_notion_columns):
        extracted = self.tableLog[case_notion_columns].values.tolist()
        unique = list(set(tuple(combination) for combination in extracted))
        filtered = [combination for combination in unique if not 'EMPTY' in combination]
        case_notions = pd.DataFrame(filtered).rename(columns={ 0: case_notion_columns[0], 1: case_notion_columns[1]})
        case_notions['case:concept:name'] = case_notions.index.astype(str)
        return case_notions
    '''

    def xes_to_disk(self):
        xes_exporter.apply(self.event_log, 'xesLogs/xes_' + self.case_notion + '.xes')


if __name__ == '__main__':
    log_extractor = XESLogTool(['customer'])
    log_extractor.xes_to_disk()

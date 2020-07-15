import pandas as pd
from pm4py.objects.log.log import EventLog
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.exporter.xes import exporter as xes_exporter
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.petrinet import factory as petri_net_visualization
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.util import constants
from pm4py.objects.log.adapters.pandas import csv_import_adapter


class XESLogTool:

    def __init__(self, csv_file_path: str, case_notion_columns: list):
        self.case_notion = ''.join(case_notion_columns)
        self.event_log: EventLog = self.__create_xes_file__(csv_file_path, case_notion_columns)
    
    def __create_xes_file__(self, csv_file_path, case_notion_columns) -> EventLog:
        # load csv file
        dataframe = csv_import_adapter.import_dataframe_from_path(csv_file_path, sep=",")
        dataframe.rental = dataframe.rental.astype(str)

        def is_slice_in_list(list1, list2):
            return all(elem in list2 for elem in list1)

        # check weather all column names exist in the table
        if not is_slice_in_list(case_notion_columns, dataframe.columns):
            print('Error: (Some) Columns may not exist.')
            exit(0)

        if len(case_notion_columns) > 1:  # if multiple columns should be considered as one case notion
            case_notion = self.get_case_notion(case_notion_columns, dataframe)

            # map new case id on the combination of unqiue columns
            dataframe = pd.concat([dataframe, case_notion], axis=1, join='outer')

            # rename the columns for preparing the xes log
            columns_to_rename = {'timestamp': 'time:timestamp', 'activity': 'concept:name'}
            dataframe.rename(columns=columns_to_rename, inplace=True)

        else: # if only one column is considered as a case notion
            indexNames = dataframe[ dataframe[case_notion_columns[0]] == 'EMPTY' ].index
            dataframe.drop(indexNames, inplace=True)

            # rename the columns for preparing the xes log
            columns_to_rename = {case_notion_columns[0]: 'case:concept:name',
                                 'timestamp': 'time:timestamp',
                                 'activity': 'concept:name',
                                 'lifecycle': 'lifecycle:transition'}
            dataframe.rename(columns=columns_to_rename, inplace=True)

        # convert to xes format
        parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "case:concept:name",
                      constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
                      constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp",
                      constants.PARAMETER_CONSTANT_TRANSITION_KEY: "lifecycle:transition"}
        return conversion_factory.apply(dataframe, parameters=parameters)

    def get_case_ids(self) -> list:
        return [case.attributes['concept:name'] for case in self.event_log]

    def get_case_notion(self, case_notion_columns, df):
        extracted = df[case_notion_columns].values.tolist()
        unique = list(set(tuple(combination) for combination in extracted))
        filtered = [combination for combination in unique if not 'EMPTY' in combination]
        case_notions = pd.DataFrame(filtered).rename(columns={ 0: case_notion_columns[0], 1: case_notion_columns[1]})
        case_notions['case:concept:name'] = case_notions.index.astype(str)
        return case_notions

    def get_events_for_case(self, case_id: int):
        return [event for event in self.event_log[case_id]]

    def get_directly_follows_graph(self):
        dfg = dfg_discovery.apply(self.event_log)
        parameters = {dfg_visualization.Variants.PERFORMANCE.value.Parameters.FORMAT: "png"}
        gviz = dfg_visualization.apply(dfg, log=self.event_log, parameters=parameters)
        dfg_visualization.save(gviz, 'graphs/DFG_' + self.case_notion + '.png')

    def xes_to_disk(self):
        xes_exporter.apply(self.event_log, 'xesLogs/xes_' + self.case_notion + '.xes')


if __name__ == '__main__':
    log_extractor = XESLogTool('tableLog.csv', ['staff', 'inspection'])
    log_extractor.get_directly_follows_graph()
    log_extractor.xes_to_disk()

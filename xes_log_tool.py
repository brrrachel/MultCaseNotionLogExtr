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
    csv: pd.DataFrame

    def __init__(self, csv_file_path: str, case_notion_column: str):
        self.case_notion = case_notion_column
        self.event_log: EventLog = self.__create_xes_file__(csv_file_path, case_notion_column)
    
    def __create_xes_file__(self, csv_file_path, case_notion_column) -> EventLog:
        # load csv file
        dataframe = csv_import_adapter.import_dataframe_from_path(csv_file_path, sep=",")
        if case_notion_column in dataframe.columns:
            # rename the column which will be the case notion
            columns_to_rename = {case_notion_column: 'case:concept:name', 'timestamp': 'time:timestamp', 'activity': 'concept:name'}
            dataframe.rename(columns=columns_to_rename, inplace=True)
        else:
            print('Column does not exist.')
            exit(0)
        # convert to xes format
        parameters = {constants.PARAMETER_CONSTANT_CASEID_KEY: "case:concept:name",
                              constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
                              constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"}
        return conversion_factory.apply(dataframe, parameters=parameters)
    
    def get_case_ids(self) -> list:
        return [case.attributes['concept:name'] for case in self.event_log]
    
    def get_events_for_case(self, case_id: int):
        return [event for event in self.event_log[case_id]]
    
    def create_petri_net(self):
        net, initial_marking, final_marking = alpha_miner.apply(self.event_log)
        gviz = petri_net_visualization.apply(net, initial_marking, final_marking, parameters={"format":"png"})
        petri_net_visualization.save(gviz, 'graphs/petri_' + self.case_notion + '.png')
    
    def get_directly_follows_graph(self):
        dfg = dfg_discovery.apply(self.event_log, variant=dfg_discovery.Variants.PERFORMANCE)
        parameters = {dfg_visualization.Variants.PERFORMANCE.value.Parameters.FORMAT: "png"}
        gviz = dfg_visualization.apply(dfg, log=self.event_log, variant=dfg_visualization.Variants.PERFORMANCE, parameters=parameters)
        dfg_visualization.save(gviz, 'graphs/DFG_' + self.case_notion + '.png')
    
    def xes_to_disk(self):
        xes_exporter.apply(self.event_log, 'xesLogs/xes_' + self.case_notion + '.xes')

if __name__ == '__main__':
    log_extractor = XESLogTool('sortedTableLog.csv', 'rental')
    log_extractor.create_petri_net()
    log_extractor.get_directly_follows_graph()
    log_extractor.xes_to_disk()
    
    
    
    
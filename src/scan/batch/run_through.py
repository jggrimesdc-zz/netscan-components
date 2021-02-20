import os
import pandas as pd
import time

from add_date_col import AddDateColumn
from add_domain_col import AddDomainColumn
from breach_prep import BreachPrep
from config_reader import GetConfig
from date_col_update import DateColumnUpdates
from email_update import EmailUpdate
from ingest_api import IngestFilesAPI
from ingest_api_paginated import IngestFilesAPIPaginated
from ingest_blackarch import IngestBlackarch
from ingest_class import IngestFiles
from ingest_kali import IngestKali
from read_csv_alien import ReadAlienCSV
from read_csv_columns import ReadCSVColumns
from read_csv_comments import ReadCSVComments
from read_csv_simple import ReadCSV
from read_jl import ReadBreachJL
from read_json import ReadJSON
# from read_json_vuln import ReadVulnJSON
from read_json_nested import ReadJSONNested
from read_tool_html import ReadToolHTML
from read_tool_pkgbld import ReadToolPKGBLD
from read_txt_single_col import ReadSingleColTxt
from to_parquet import DataframeToParquet
from to_parquet_breach import DataframeToParquetBreach
from to_parquet_no_success import DataframeToParquetNoSuccess
from tools_inc_load import ToolsIncrementalLoad

config = GetConfig()
for source in config.config_json:
    for label, file in config.config_json[source].items():
        if label == os.getenv('LABEL'):
            print(file)
            df = pd.DataFrame()
            for class_step in file['transformations']:
                class_call = globals()[class_step]

                if 'Ingest' in class_call.__name__:
                    test_run = class_call(source,
                                          label,
                                          file,
                                          config,
                                          df=None)
                    test_run.run_all()
                    print(class_call.__name__ + " complete for " + label + " at " + time.strftime("%H:%M:%S",
                                                                                                  time.localtime()))
                elif 'Read' in class_call.__name__:
                    test_run = class_call(source,
                                          label,
                                          file,
                                          config,
                                          df=None)

                    df_con = test_run.run_all()
                    df = df.append(df_con)
                    print(class_call.__name__ + " complete for " + label + " at " + time.strftime("%H:%M:%S",
                                                                                                  time.localtime()))
                else:
                    test_run = class_call(source,
                                          label,
                                          file,
                                          config,
                                          df=df)
                    df_new = test_run.run_all()

                    # df.update(df_new)
                    if df_new is not None:
                        df = df_new.copy()

                    # df = test_run.run_all()
                    print(class_call.__name__ + " complete for " + label + " at " + time.strftime("%H:%M:%S",
                                                                                                  time.localtime()))
        # else:
        #     print(f"{label}")

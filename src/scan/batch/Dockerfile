FROM python:3.8

WORKDIR /batch_q

COPY requirements.txt /batch_q/

RUN apt-get update -y \
      && apt-get -y install sudo \
      && sudo apt-get -y install libsnappy-dev \
      && sudo apt-get -y install python3-dev \
      && sudo apt-get -y install git

RUN pip3 install -r requirements.txt

COPY run_through.py /batch_q
COPY config_reader.py /batch_q
COPY ingest_class.py /batch_q
COPY ingest_api.py /batch_q
COPY ingest_api_paginated.py /batch_q

COPY read_csv_alien.py /batch_q
COPY read_csv_comments.py /batch_q
COPY read_csv_columns.py /batch_q
COPY read_csv_simple.py /batch_q
COPY read_json.py /batch_q
COPY read_txt_single_col.py /batch_q
COPY read_json_nested.py /batch_q

COPY base_worker.py /batch_q
COPY add_domain_col.py /batch_q
COPY add_date_col.py /batch_q
COPY date_col_update.py /batch_q
COPY to_parquet.py /batch_q
COPY to_parquet_no_success.py /batch_q

COPY breach_prep.py /batch_q
COPY email_update.py /batch_q
COPY read_jl.py /batch_q
COPY to_parquet_breach.py /batch_q

COPY ingest_blackarch.py /batch_q
COPY read_tool_pkgbld.py /batch_q

COPY ingest_kali.py /batch_q
COPY read_tool_html.py /batch_q
COPY tools_inc_load.py /batch_q

CMD [ "python", "run_through.py" ]

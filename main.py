from datetime import date
from pathlib import Path

from api import settings
from api.api1 import api1
from api.packages import excel_pivot

if __name__ == '__main__':
    report_date = date.today()
    api1.run(report_date)

    # api1_csv_dir = Path.joinpath(settings.BASE_DIR, "api1/csv")
    # df = excel_pivot.import_csv(api1_csv_dir)
    # table = excel_pivot.create_pivot(df, index_list=['end_datetime', 'hostname', 'interface'], value_list=['max_rx_kbps', 'sum_rx_octets', 'max_tx_kbps', 'sum_tx_octets'])
    # api1_report_dir = Path.joinpath(settings.BASE_DIR, "api1")
    # excel_pivot.save_report(table, api1_csv_dir/'report.xlsx')

    print('Done!')

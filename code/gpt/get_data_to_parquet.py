import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

API_URL = "http://www.pinet-server.org/pinet/api/uniprotdb/organism/9606/accession/O15393"
def main():
  try:
    response = requests.get(API_URL)
    if response.status_code == 200:
      data = response.json()
      function_text = data.get('function', '')
      df = pd.DataFrame({'function': [function_text]})
      table = pa.Table.from_pandas(df)
      pq.write_table(table, 'protein_summary.parquet')
    else:
      print(f'Failed to retrieve data: {response.status_code}')
  except Exception as error:
    print(error)


if __name__ == "__main__":
  main()

# !pip install soda-core soda-core-contracts python-dotenv pyyaml soda-core-pandas-dask numpy==1.26.4

import json
import dask.dataframe as dd
from soda.scan import Scan

def run_contract_scan(file_path: str, datacontract_path: str):

    with open(filepath, "r") as infile:
        checks = infile.read()
    
    log.info(f"Checks: {chacks}")

    

    scan = Scan()
    scan.set_scan_definition_name("test")
    scan.set_data_source_name("dask")

    ddf = dd.read_csv('data/emoji_usage_dataset.csv')

    scan.add_dask_dataframe(dataset_name="emoji", dask_df=ddf)

    # Checks para usar: https://docs.soda.io/soda-cl/soda-cl-overview.html
    checks = """
    checks for emoji:
        - row_count > 0
        - invalid_count("User Age") = 0:
            valid min: 26
            valid max: 52
        - avg("User Age") > 37
        - duplicate_count(Emoji) = 0
    # Checks for schema changes
        - schema:
            name: Find forbidden, missing, or wrong type
            warn:
                when required column missing: [Emoji, "User Gender"]
                when forbidden column present: [credit_card]
                when wrong column type:
                    Platform: varchar
            fail:
                when forbidden column present: [pii*]
                when wrong column index:
                    "User Age": 1
    """

    scan.add_sodacl_yaml_str(checks)
    scan.set_verbose(True)
    scan.execute()
    resultados_json = scan.get_scan_results()

    json_path = "output/resultados.json"
    with open(json_path, "w") as outfile:
        outfile.write(json.dumps(resultados_json, indent = 4))
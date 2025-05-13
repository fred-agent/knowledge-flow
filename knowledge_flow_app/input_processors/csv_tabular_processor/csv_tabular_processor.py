# knowledge_flow_app/processors/processor_example_tabular/example_tabular_processor.py

from pathlib import Path
from typing import List, Dict
import csv

import pandas

from knowledge_flow_app.input_processors.base_input_processor import BaseTabularProcessor

class CsvTabularProcessor(BaseTabularProcessor):
    """
    An example tabular processor for CSV files.
    Extracts header and rows from a simple CSV file.
    """

    def check_file_validity(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == ".csv" and file_path.is_file()

    def extract_file_metadata(self, file_path: Path) -> dict:
        df = pandas.read_csv(file_path, nrows=5)
        return {
            "format": "CSV",
            "row_count": len(pandas.read_csv(file_path)),  # optional: use nrows param if needed
            "num_columns": len(df.columns),
            "sample_columns": df.columns.tolist(),
        }

    def convert_file_to_table(self, file_path: Path) -> pandas.DataFrame:
        return pandas.read_csv(file_path)

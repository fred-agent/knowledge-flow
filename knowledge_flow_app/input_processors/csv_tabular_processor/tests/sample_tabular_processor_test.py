# test_example_tabular_processor.py
import tempfile
import pandas as pd
from pathlib import Path

from knowledge_flow_app.input_processors.csv_tabular_processor.csv_tabular_processor import CsvTabularProcessor


def test_valid_csv():
    processor = CsvTabularProcessor()
    content = "name,age\nAlice,30\nBob,25"
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv') as f:
        f.write(content)
        temp_path = Path(f.name)

    assert processor.check_file_validity(temp_path)
    df = processor.convert_file_to_table(temp_path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)

    metadata = processor.extract_file_metadata(temp_path)
    assert metadata['num_columns'] == 2
    assert metadata['sample_columns'] == ['name', 'age']

    temp_path.unlink()

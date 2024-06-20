from pathlib import Path

class Config:
    root_path: Path = Path(__file__).parent
    data_path: Path = root_path / 'data'
    dataset_file: Path = data_path / 'data.csv'

settings = Config()

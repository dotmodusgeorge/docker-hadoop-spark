import argparse
import pathlib
import os
import random
import shutil

from faker import Faker
from faker import providers

import pandas
from tqdm import tqdm

fake = Faker()
fake.add_provider(providers.bank)
fake.add_provider(providers.person)


FILES_DIR = 'Files'

def generate_id_pool(id_range: int):
    return list(range(0, id_range))

class MockData:
    def __init__(self):
        self.id_pool_1 = generate_id_pool(1000)
        self.id_pool_2 = generate_id_pool(500)
        self.id_pool_3 = generate_id_pool(250)

    def generate_mock_data(self, filename: str):
        record_count = random.randint(120, 640)
        start = 0
        records = []
        while start < record_count:
            id1 = self.id_pool_1[random.randint(0, len(self.id_pool_1) - 1)]
            id2 = self.id_pool_2[random.randint(0, len(self.id_pool_2) - 1)]
            id3 = self.id_pool_3[random.randint(0, len(self.id_pool_3) - 1)]
            records.append(self.generate_mock_row(id1, id2, id3))
            start = start + 1
        df = pandas.DataFrame(data=records)
        df.to_csv(filename, index=False, header=True)


    def generate_mock_row(self, id1: str, id2: str, id3: str):
        row = {}
        row['id1'] = id1
        row['id2'] = id2
        row['id3'] = id3
        row['name'] = fake.name().replace(',', '_')
        row['prefix'] = fake.prefix().replace(',', '_')
        row['suffix'] = fake.suffix().replace(',', '_')
        row['job'] = fake.job().replace(',', '_')
        row['country'] = fake.bank_country().replace(',', '_')
        return row


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--count", default=50)
    args = parser.parse_args()

    current_dir = pathlib.Path(__file__).parent
    current_file = pathlib.Path(__file__)
    output_dir = os.path.join(current_dir, FILES_DIR, args.name)

    if not os.path.exists(os.path.join(current_dir, FILES_DIR)):
        os.mkdir(os.path.join(current_dir, FILES_DIR))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)
    else:
        os.mkdir(output_dir)

    mock = MockData()

    with tqdm(total=int(args.count)) as pbar:
        i = 0
        while i < int(args.count):
            filename = os.path.join(output_dir, F"fact_test_file_{str(i)}.csv")
            mock.generate_mock_data(filename)
            pbar.update(1)
            i = i+1

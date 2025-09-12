import csv
import os
from datetime import datetime
from collections import defaultdict

from pep_parse.settings import RESULTS_DIR, BASE_DIR


class PepParsePipeline:
    def __init__(self):
        self.results_dir = BASE_DIR / RESULTS_DIR
        self.results_dir.mkdir(exist_ok=True)

    def open_spider(self, spider):
        self.status_counter = defaultdict(int)

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        filename = os.path.join(
            self.results_dir,
            'status_summary_{}.csv'
            .format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        )

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel', quoting=csv.QUOTE_NONE)

            results = []
            for code, count in sorted(self.status_counter.items()):
                results.append([code, count])

            rows = [
                ['Статус', 'Количество'],
                *results,
                ['Total', sum(self.status_counter.values())],
            ]

            writer.writerows(rows)

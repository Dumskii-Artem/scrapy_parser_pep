import csv
import os
from datetime import datetime
from collections import defaultdict

from pep_parse.settings import RESULTS_DIR


class PepParsePipeline:

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        os.makedirs(RESULTS_DIR, exist_ok=True)
        return pipeline

    def open_spider(self, spider):
        self.status_counter = defaultdict(int)

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        filename = os.path.join(
            RESULTS_DIR,
            'status_summary_{}.csv'
            .format(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        )
        with (open(filename, mode='w', encoding='utf-8', newline='') as f):
            writer = csv.writer(f)
            rows = [
                ['Статус', 'Количество']
            ] + sorted(self.status_counter.items()) + [
                ['Total', sum(self.status_counter.values())]
            ]
            writer.writerows(rows)

import csv
import os
from datetime import datetime
from collections import defaultdict


class PepParsePipeline:
    def __init__(self):
        self.status_counter = defaultdict(int)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.status_counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        feed_path = list(spider.settings.get('FEEDS').keys())[0]
        results_dir = os.path.dirname(feed_path)
        os.makedirs(results_dir, exist_ok=True)
        filename = os.path.join(results_dir, f'status_summary_{now}.csv')

        total = sum(self.status_counter.values())

        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            for status, count in sorted(self.status_counter.items()):
                writer.writerow([status, count])
            writer.writerow(['Total', total])

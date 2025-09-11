import csv
import os
from datetime import datetime
from collections import defaultdict


class PepParsePipeline:
    def open_spider(self, spider):
        # здесь для тестов такие сложности
        self.status_counter = defaultdict(int)
        feed_path = list(spider.settings.get('FEEDS').keys())[0]
        self.results_dir = os.path.dirname(feed_path)

        os.makedirs(self.results_dir, exist_ok=True)

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
            writer = csv.writer(f)
            rows = [['Статус', 'Количество']] + \
                   sorted(self.status_counter.items()) + \
                   [['Total', sum(self.status_counter.values())]]
            writer.writerows(rows)

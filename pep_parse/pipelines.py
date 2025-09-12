import csv
import os
from datetime import datetime
from collections import defaultdict
from pathlib import Path

from pep_parse.settings import RESULTS_DIR


class PepParsePipeline:
    def _resolve_results_dir(self, spider) -> Path:
        feeds = spider.settings.get("FEEDS") or {}
        try:
            first_key = next(iter(feeds))
            return Path(str(first_key)).parent
        except Exception:
            return Path(spider.settings.get("RESULTS_DIR", RESULTS_DIR))

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        pipeline.results_dir = pipeline._resolve_results_dir(crawler.spider)
        os.makedirs(pipeline.results_dir, exist_ok=True)
        return pipeline

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
        with (open(filename, mode='w', encoding='utf-8', newline='') as f):
            writer = csv.writer(f)
            rows = [
                ['Статус', 'Количество']
            ] + sorted(self.status_counter.items()) + [
                ['Total', sum(self.status_counter.values())]
            ]
            writer.writerows(rows)

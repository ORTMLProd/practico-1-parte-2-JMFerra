import logging
from collections import defaultdict
import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.spiders import Spider
from scrapy.utils.misc import md5sum


class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider: Spider) -> dict:
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["id"])
            return item


class JSONPipeline:
    def __init__(self):
        self.file = open('carone_data.json', 'w')
        self.file.write("[\n")
        self.first_item = True

    def close_spider(self, spider):
        self.file.write("\n]")
        self.file.close()

    def process_item(self, item, spider):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(",\n")

        line = json.dumps(dict(item))
        self.file.write(line)
        return item


class ItemLimit:
    def __init__(self, max_items_per_label: int, label_field: str):
        self.label_counts = defaultdict(int)
        self.max_items_per_label = max_items_per_label
        self.label_field = label_field

    def process_item(self, item, spider) -> dict:
        adapter = ItemAdapter(item)
        label = adapter[self.label_field]
        if self.label_counts[label] >= self.max_items_per_label:
            raise DropItem(f"Reached max number of items for label {label}")
        else:
            self.label_counts[label] += 1
            return item

    @classmethod
    def from_crawler(cls, crawler):
        try:
            max_items_per_label = crawler.settings["max_items_per_label"]
            label_field = crawler.settings["label_field"]
        except KeyError as exc:
            logging.error(
                "max_items_per_label or label_field settings not found in the crawler"
                "settings. You need to set them for the ItemLimit pipeline to work.\n"
                f"{exc}"
            )
        return cls(max_items_per_label, label_field)


class CustomImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return f'full/{image_guid}'

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Image Download Failed")
        item['image_paths'] = image_paths
        return item

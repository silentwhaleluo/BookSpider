# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors


class BookspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonExporterPipeline(object):
    def __init__(self):
        # use the exporter from scrapy export json files
        self.file = open('bookexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        mysqlParms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **mysqlParms)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_data, item)
        query.addErrback(self.handle_error, item, spider)  # process error

    def handle_error(self, failure, item, spider):
        print(failure)

    def take_first(self, list):
        if list:
            return list[0]
        else:
            return None

    def insert_data(self, curosr, item):
        sql_qury = '''insert into bookspider(url,url_md5,process_date,img_url,title,description,star_rating,upc,
        product_type,currency,price_exceltax,price_incltax,tax,availability,n_reviews) 
        VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)
        '''
        curosr.execute(sql_qury,
                       (item.get('url', None), item.get('url_md5', None), item.get('process_date', None),
                       self.take_first(['img_url']),
                       item.get('title', None), item.get('description', None), item.get('star_rating', None),
                       item.get('upc', None),
                       item.get('product_type', None), item.get('currency', None), item.get('price_exceltax', None),
                       item.get('price_incltax', None), item.get('tax', None), item.get('availability', None),
                       item.get('n_reviews', None))
                       )

    class BookImagePipeline(ImagesPipeline):
        def item_completed(self, results, item, info):
            if 'img_url' in item:
                for b, value in results:
                    image_path = value['path']
                item['img_path'] = image_path
            return item

# if __name__ == '__main__':
#     mysqlParms = dict(
#         host=settings['MYSQL_HOST'],
#         dbname=settings['MYSQL_DBNAME'],
#         user=settings['MYSQL_USER'],
#         passwd=settings['MYSQL_PASSWORD'],
#         charset='utf8',
#         cursorclass=MySQLdb.cursors.DictCursor,
#         use_unicode=True,
#     )
#     print(mysqlParms)

__author__ = 'Jing'

from scrapy.cmdline import execute
import sys
import os
import MySQLdb
from scrapy.utils.project import get_project_settings


# make the dictionary for images
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def create_files():
    # create file to save images
    img_file_path = os.path.dirname(os.path.abspath(__file__)) + '/BookSpider/images'
    if not os.path.exists(img_file_path):
        os.makedirs(img_file_path)
        print('images path: %s' % img_file_path)

    # create for database and tables for to export results
    settings = get_project_settings()
    host = settings['MYSQL_HOST']
    dbname = settings['MYSQL_DBNAME']
    user = settings['MYSQL_USER']
    passwd = settings['MYSQL_PASSWORD']
    print(host,dbname,user,passwd)
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd)
    cursor = conn.cursor()
    result = cursor.execute(
        '''
        CREATE DATABASE IF NOT EXISTS %s;
        USE %s;
        DROP TABLE IF EXISTS bookspider;
        CREATE TABLE IF NOT EXISTS bookspider(
        url VARCHAR(300),
        url_md5 CHAR(32) PRIMARY KEY,
        process_date DATE,
        img_url VARCHAR(100),
        title VARCHAR(255),
        description LONGTEXT,
        star_rating TINYINT(1) UNSIGNED,
        upc CHAR(16),
        product_type VARCHAR(50),
        currency CHAR(1),
        price_exceltax FLOAT(5,2) UNSIGNED,
        price_incltax FLOAT(5,2) UNSIGNED,
        tax FLOAT(5,2) UNSIGNED,
        availability SMALLINT UNSIGNED,
        n_reviews SMALLINT(4) UNSIGNED) DEFAULT CHARSET=utf8;
        ''' % (dbname, dbname))
    # print(result)
    print('database %s and table bookspider is created'%dbname)
    cursor.close()
    conn.close()


print('starting scrape book info')
create_files()
# print(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'book_spider', '-s', 'LOG_FILE=BookSpider.log'])


execute(['scrapy', 'crawl', 'book_spider'])

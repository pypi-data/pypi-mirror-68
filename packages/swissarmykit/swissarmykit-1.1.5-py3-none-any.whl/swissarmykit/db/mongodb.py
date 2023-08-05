
try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py
from mongoengine.base import UPDATE_OPERATORS
from mongoengine import *
import datetime
import json
import os
import sys
import csv
from pprint import pprint
from typing import List, Union

from swissarmykit.utils.timer import Timer
from swissarmykit.utils.loggerutils import LoggerUtils
from swissarmykit.req.FileThread import FileTask
from swissarmykit.utils.fileutils import FileUtils
from swissarmykit.utils.stringutils import StringUtils
from swissarmykit.utils.counter import Counter
from swissarmykit.utils.command import Command
from swissarmykit.office.excelutils import ExcelUtils
from urllib.parse import parse_qs, urlparse

_counter = Counter.instance()

class BaseDocument(DynamicDocument):
    '''
        url = StringField(sparse=True, required=True, unique=True)
        name = StringField()
        has_html_1 = BooleanField()
        data = DictField()
        extra = DictField()
        images = StringField()
        version = IntField()
        updated_at = DateTimeField(default=datetime.datetime.now)

        SQL Terms/Concepts	    MongoDB Terms/Concepts
        database	            database
        table	                collection
        row	                    document or BSON document
        column	                field
        index	                index
        table joins	            $lookup, embedded documents
        primary key             primary key

        Field define: http://docs.mongoengine.org/guide/defining-documents.html
    '''
    meta = {
        'abstract': True,
    }

    _db_alias = None

    url = StringField(sparse=True, required=True, unique=True)
    name = StringField()
    has_html_1 = BooleanField()
    data = DictField()
    value = DynamicField()
    extra = DictField()
    images = StringField()
    version = IntField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    timer = None
    is_tmp = False

    @classmethod
    def get_db(cls):
        return get_db()

    @classmethod
    def get_db_name(cls):
        return appConfig.DATABASE_NAME

    @classmethod
    def get_meta(cls):
        return cls._meta

    @classmethod
    def count(cls, filters=None): # type: (dict) -> int
        if filters:
            cls.objects.filters(**filters).count()
        return cls.objects.count()

    @classmethod
    def delete_html(cls, id=None, lst=None, level=1):
        has_html_ = {'unset__has_html_%d' % level: 1}
        if id:
            cls.objects(id=id).update(**has_html_)
        if lst:
            cls.objects.filter(**{'id__in':lst}).update(**has_html_)
        raise Exception('Cls required id, and lst')

    def remove_html(self, level=1):
        self.update(**{'unset__has_html_%d' % level: 1})

    @classmethod
    def delete_table(cls):
        cls.drop_collection()

    @classmethod
    def truncate_table(cls):
        cls.drop_collection()

    @classmethod
    def exists_id(cls, id):
        return cls.objects.with_id(object_id=id)

    @classmethod
    def exists(cls, col: str, val):
        return cls.objects(__raw__={col: val})

    @classmethod
    def get_all_rows(cls):
        return [o for o in cls.objects]

    @classmethod
    def get_all_docs(cls):
        return [o for o in cls.objects]

    @classmethod
    def exists_html(cls, url, level=1):
        has_html_ = 'has_html_%d' % level
        return getattr(cls.get_by_url(url), has_html_)

    @classmethod
    def dump_mysql_of_this_table(cls, path=None):
        lst = [o.to_json() for o in cls.objects]
        FileUtils.to_html_file(path, json.dumps(lst))

    @classmethod
    def get_first_row(cls):  # type: () -> BaseDocument
        return cls.objects.first()

    @classmethod
    def get_items(cls, **kwargs):  # type: (any) -> BaseDocument
        if 'limit' not in kwargs: kwargs['limit'] = - 1
        return [item for item in cls.get_one(**kwargs)]

    @classmethod
    def get_record(cls, **kwargs):  # type: (dict) -> BaseDocument
        return cls.get_one(limit=1, **kwargs)

    @classmethod
    def get_records(cls, **kwargs):  # type: (dict) -> Union[List[BaseDocument], BaseDocument]
        return cls.get_one(limit=-1, **kwargs)

    @classmethod
    def print_database_info(cls):
        print('Database: %s. Table: %s\nMeta: %s' % (cls.get_db_name(), cls.get_table_name(), str(cls.get_meta())))

    @classmethod
    def get_all_schemas(cls):
        return cls.get_db().adminCommand('listDatabases')

    @classmethod
    def show_tables(cls):
        pprint(cls.get_all_collection_name())

    @classmethod
    def get_all_tables(cls):
        return cls.get_all_collection_name()

    @classmethod
    def get_table_name(cls):
        return cls._get_collection_name()

    @classmethod
    def get_collection_name(cls):
        return cls._get_collection_name()

    @classmethod
    def get_all_collection_name(cls):
        return cls.get_db().list_collection_names()

    @classmethod
    def insert_record(cls, data=None):
        return cls(**data).save()

    @classmethod
    def get_fields(cls):
        field_dict = cls.get_first_row()._fields
        lst = []
        for field_name, field in field_dict.items():
            lst.append(field_name)
            # print(field_name, field.required, field.__class__)
        return lst

    @classmethod
    def export_data_to_csv_2(cls, lst=None, headers_order=None, col_name='data', limit=-1, offset=0,
                           headers=None, callback_format_data=None,
                           remove_invalid_char=False, auto_order_header=False, sort_header=None,
                           file_name=None):

        file = appConfig.EXCEL_PATH + '/' + (file_name if file_name else cls.get_collection_name()) + '.csv'

        with open(file, 'w', newline='', encoding="utf-8") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)

            if not headers:
                print('INFO: Will automatic get headers')
                headers = cls.get_headers()

            wr.writerow(headers)

            if not lst:
                lst = cls.get_one(limit=limit, offset=offset, col_name=col_name, is_null_data=False) if col_name == 'data' else cls.get_one(limit=limit, offset=offset, col_name=col_name)

            for item in lst:
                try:
                    item.check()

                    data = item.get_data()
                    if callback_format_data:
                        data = callback_format_data(data)

                    _l = []

                    for h in headers:
                        _l.append(data.get(h, ''))
                    wr.writerow(_l)
                except Exception as e:
                    print('Error: Retry ', e, ' data:', _l, ' line: ', item.get_id_offset())
                    try:
                        wr.writerow([StringUtils.get_valid_utf_8(__l) for __l in _l])
                    except Exception as e:
                        print('error:', e, ' SKIP')

    @classmethod
    def export_data_to_csv(cls, lst=None, headers=None, file_name=None):
        file = appConfig.EXCEL_PATH + '/' + (file_name if file_name else cls.get_collection_name()) + '.csv'
        print('INFO: Total: ', len(lst))
        if isinstance(lst[0], dict):
            lst = [list(item.values()) for item in lst]

        if headers:
            lst.insert(0, headers)

        timer = Timer.instance()
        timer.reset(len(lst))
        with open(file, 'w', newline='', encoding="utf-8") as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i, l in enumerate(lst):
                try:
                    timer.check(idx=i)
                    wr.writerow(l)
                except Exception as e:
                    print('Error: Retry ', e, ' data:', l, ' line: ', i + 1)
                    try:
                        wr.writerow([StringUtils.get_valid_utf_8(_l) for _l in l])
                    except Exception as e:
                        print('error:', e, ' SKIP')
        print('INFO: Output to CSV ', file)

    @classmethod
    def convert_excel_to_csv(cls):
        pass

    @classmethod
    def export_data_to_excel(cls, lst=None, headers_order=None, col_name='data', limit=-1, offset=0, format='',
                             headers=None, callback_format_data=None,
                             remove_invalid_char=False, debug=False, auto_order_header=False, sort_header=None,
                             file_name='', write_one_by_one=False):
        '''

        :param lst:
        :param headers_order: Header order base on few order
        :param col_name:
        :param limit:
        :param offset:
        :param format:
        :param headers: Header limit exectly
        :param callback_format_data:
        :param remove_invalid_char:
        :param debug:
        :param auto_order_header:
        :param sort_header:
        :param file_name:
        :param write_one_by_one:
        :return:
        '''
        data_lst = []
        if lst is not None:
            data_lst = lst[offset:limit] if limit > 0 else lst[offset:]
        else:
            __lst = cls.get_one(limit=limit, offset=offset, col_name=col_name, is_null_data=False) if col_name == 'data' else cls.get_one(limit=limit, offset=offset, col_name=col_name)
            for item in __lst:
                try:
                    data = getattr(item, col_name)
                    if remove_invalid_char:
                        data = {k: StringUtils.get_valid_text_for_excel(v) for k, v in data.items()}

                    if callback_format_data:
                        data = callback_format_data(data)
                        if not data:
                            continue
                    data_lst.append(data)
                except Exception as e:
                    print('ERROR: ', e, item)

        # Auto get header_order
        if auto_order_header or headers_order:
            headers = {}
            for data in data_lst:
                for key in data.keys():
                    headers[key] = 1
            new_order = list(headers.keys())

            if sort_header:
                if sort_header in ['DESC', 'desc']:
                    new_order.sort(reverse=True)
                else:
                    new_order.sort()

            if headers_order:
                headers = {}
                headers_order = headers_order + new_order
                for key in headers_order: headers[key] = 1
                headers_order = list(headers.keys())
            else:
                headers_order = new_order

        if debug:
            print(data_lst)

        if not data_lst:
            print('ERROR: Empty list to export to Excel')
            return False

        if not file_name:
            file_name = appConfig.EXCEL_PATH + '/' + cls.get_collection_name() + '.xlsx'

        ExcelUtils.json_to_openpyxl(data_lst, headers_order=headers_order, headers=headers, file_name=file_name,
                                    write_one_by_one=write_one_by_one)

    @classmethod
    def export_header_key(cls, col_name='data'):
        headers = {}
        for item in cls.objects:
            data = getattr(item, col_name)

            if data:
                for h in data.keys():
                    headers[h] = 0
        re = list(headers.keys())
        print(re)
        return re

    def get_values(self):
        lst = []
        fields = self.get_fields()
        data = self.__dict__.get('_data')
        for f in fields:
            lst.append(data.get(f) if data.get(f) else '')
        return lst

    @classmethod
    def output_html(cls, id=None, path=None):
        item = cls.objects(id=id)
        path = path if path else appConfig.USER_DESKTOP + '/_test_html.html'
        FileUtils.to_html_file(path, item.get_html())
        print('INFO: output to html of %d:%s' % (id, path))

    @classmethod
    def get_html_by_id(cls, id=1, output=False):
        item = cls.get_html_by_id(id)
        html = item.get_html()
        if output:
            html_path = '%s/%s_id_%d.html' % (appConfig.get_desktop_path(), cls.get_collection_name(), id)
            FileUtils.to_html_file(html_path, html)
            print('INFO: output to html: %s' % html_path)

        return html

    @classmethod
    def get_by_url(cls, url):  # type: (str) -> BaseDocument
        try:
            return cls.objects.get(url=url)
        except Exception as e:
            # print('ERROR: ', e)
            return None

    @classmethod
    def get_html_by_url(cls, url):  # type: (str) -> str
        item = cls.get_by_url(url)
        if item:
            return item.get_html()
        return ''

    @classmethod
    def get_counter(cls): # type: () -> Counter
        return _counter

    @classmethod
    def get_urls(cls, have_html=None):
        return [o.url for o in cls.get_one(-1, col_name='url', have_html=have_html)]

    @classmethod
    def get_headers(cls, remove=(), remove_contains=(), col_name='data'):
        headers = {}


        timer = Timer.instance()
        timer.reset(cls.count())

        for o in cls.objects:
            timer.check()

            data = getattr(o, col_name)
            if not data:
                continue

            for h in data:
                if h not in headers:
                    headers[h] = 1

        new_headers = {}
        for h in headers:
            if h in remove:
                continue
            skip = False
            for c in remove_contains:
                if c in h:
                    skip = True
            if skip:
                continue

            new_headers[h] = 1
        return list(new_headers.keys())

    @classmethod
    def get_ids(cls):
        return [str(o.id) for o in cls.objects.only(*['id'])]

    @classmethod
    def exists_url(cls, val, is_cache=True):
        if is_cache:
            if not hasattr(cls, '__cache_url'):
                cls.__cache_url = cls.get_urls()
            return val in cls.__cache_url

        return cls.exists('url', val)

    @classmethod
    def find_by_url(cls, url):
        return cls.get_by_url(url)

    @classmethod
    def save_url(cls, url, name=None, html=None, data=None, value=None, extra=None, attr=None, level=1, update_modified_date=None,
                 force_insert=False):  # type: (str, str, str, dict, any, dict, dict, int, bool, bool) -> BaseDocument

        # if not cls.is_tmp and '?' in url:
        #     print('WARN: should strip ? for unique url')

        if not url:
            return 0

        _data = {'url': url}
        if name:
            _data['name'] = name
        if data:
            _data['data'] = data
        if value:
            _data['value'] = value

        if extra:
            _data['extra'] = extra
        if update_modified_date:
            _data['updated_at'] = datetime.datetime.now()

        if attr:
            _data.update(attr)


        try:
            if force_insert:
                obj = cls(**_data).save()
            else:
                obj = cls.objects(url=url).upsert_one(write_concern=None, **_data)
        except Exception as e:
            cls.valid_data(_data)
            raise e

        if html:
            obj.save_html(html, level)

        return obj

    @classmethod
    def get_last(cls):
        return cls.objects.order_by('-id').first()

    @classmethod
    def get_one_item(cls, **kwargs):
        if 'limit' in kwargs: del kwargs['limit']

        return cls.get_one(limit=1, **kwargs).first()

    @classmethod
    def get_one(cls, limit=1, offset=0, col_name=None, desc=None, where_id=None, where_url=None, where_url_contains=None, filters=None, order_by=None, have_html=None, level=1,
                is_null_data=None, no_cursor_timeout=False, timeout=False, batch_size=0):  # type: (int, int, str, bool, list, list, str, dict, any, bool, int, bool, bool, bool, int) -> Union[List[BaseDocument], BaseDocument]
        '''
         http://docs.mongoengine.org/guide/querying.html
            result exhausation
            batchSize:
            timeout: alias with no_cursor_timeout
        '''
        _counter.offset = offset

        filter = filters if filters else {}

        if where_id:
            if isinstance(where_id, list):
                filter['id__in'] = where_id
            else:
                filter['id'] = where_id

        if where_url_contains:
            filter['url__icontains'] = where_url_contains

        if where_url:
            if isinstance(where_url, list):
                filter['url__in'] = where_url
            else:
                filter['url'] = where_url

        if have_html is not None:
            if have_html:
                filter['has_html_%s' % level] = True
            else:
                filter['has_html_%s' % level] = None

        if is_null_data is not None:
            if is_null_data:
                filter['data'] = None
            else:
                filter['data__ne'] = None


        qs = cls.objects.filter(**filter)

        if col_name:
            if isinstance(col_name, str):
                qs = qs.only(*[col_name])
            else:
                qs = qs.only(*col_name)

        if desc is not None:
            if desc:
                qs = qs.order_by('-id')
            else:
                qs = qs.order_by('+id')

        if order_by:
            if isinstance(order_by, list):
                qs = qs.order_by(*order_by)
            else:
                qs = qs.order_by(**order_by)

        if offset:
            qs = qs.skip(offset) #  Skip is expensive . https://stackoverflow.com/questions/13935733/mongoose-limit-offset-and-count-query

        if limit > 0:
            qs = qs.limit(limit)

        if no_cursor_timeout or batch_size or not timeout:
            qs = qs.timeout(False) # not work yet

        if batch_size:
            qs = qs.batch_size(batch_size)

        # print(qs.explain())

        _t = qs.count() - offset
        cls.timer = Timer.instance()
        cls.timer.reset(_t)

        if not _t: print('WARNING: Records in db ', cls.count(), ', Count(*): 0, Current offset: ', offset)
        return qs

    def check(self):
        ''' Check timer '''
        _counter.count_offset()
        if self.timer:
            self.timer.check(self, idx=_counter.offset)
        return _counter.offset

    def _get_offset(self):
        return _counter.offset

    def save_html(self, html, level=1, update_modified_date=None):  # type: (str, int, bool) -> BaseDocument
        if not html: return 0

        if FileTask(id=self.id, table=self.get_collection_name(), html=html, html_path=self.get_html_path()).save(level=level):
            update = {'has_html_%d' % level: True}
            if update_modified_date:
                update['updated_at'] = datetime.datetime.now()

            return self.update(**update)
        return False

    @classmethod
    def get_html_path(cls):
        if cls._db_alias:
            return appConfig.get_other_html_path(cls._db_alias)
        return None

    def get_html(self, level=1, unset_html=False): # type: (int, bool) -> str
        self.check()

        try:
            if getattr(self, 'has_html_%d' % level):
                return FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path()).load(level=level)
        except Exception as e:
            print('ERROR: ', e)
            if unset_html:
                print(' d ', end='', flush=True)
                self.remove_html(level=level)
                raise e

        print('WARNING: Not found html, id', self.id)
        return ''

    def have_html(self, level=1, unset_html=False):
        try:
            if getattr(self, 'has_html_%d' % level):
                if FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path()).exists(level=level):
                    return True
        except Exception as e:
            print('ERROR: ', e)

        if unset_html:
            print('.', end='', flush=True)
            self.remove_html(level=level)

        return False

    def get_url_query(self):
        return parse_qs(urlparse(self.url).query)

    def get_html_size(self, level=1):
        if getattr(self, 'has_html_%d' % level):
            return FileTask(id=self.id, table=self.get_collection_name(), html_path=self.get_html_path()).size(level=level)

        print('WARNING: Not found html, id', self.id)
        return 0

    def save_extra(self, data):
        return self.update(**{'extra': data})

    def save_name(self, name):
        return self.update(**{'name': name})

    def get_extra(self):
        return self.extra

    def get_id_offset(self):
        return _counter.offset

    @classmethod
    def get_offset(cls, url):
        urls = cls.get_urls()
        return urls.index(url)

    @classmethod
    def valid_data(cls, data):
        if set(data.keys()) & set(UPDATE_OPERATORS):
            raise Exception('ERROR: From MyApp: keys must not same as ' + str(data.keys()) + ' - ' + str(UPDATE_OPERATORS))
        return True

    def save_data(self, data, value=None, attr=None, update_modified_date=None):  # type: (dict, dict, bool) -> BaseDocument
        update = {'data': data} if data else {}

        if update_modified_date:
            update['updated_at'] = datetime.datetime.now()
        if value:
            update['value'] = value

        if attr:
            update.update(attr)

        try:
            if update: return self.update(**update)
            else: print('ERROR: Update, but no data to update')
        except Exception as e:
            self.valid_data(update)
            raise e
        return None

    def remove_data(self):
        self.update(**{'unset__data': 1})

    def save_attr(self, attr, value=None, update_modified_date=None):
        self.save_data(None, attr=attr, value=value, update_modified_date=update_modified_date)

    def save_value(self, value):
        self.save_data({}, value=value)

    def get_data(self):
        return self.data

    @classmethod
    def find_one_by_id(cls, id): # type: (int) -> BaseDocument
        return cls.objects.get(id=id)

    @classmethod
    def get_all(cls, col=None): # type: (str) -> Union[List[BaseDocument], BaseDocument]
        return cls.get_one(-1, col_name=col)

    @classmethod
    def output_tmp(cls, id=1):
        return cls.output_html_by_id(id, appConfig.DIST_PATH + '/tmp.html')

    @classmethod
    def output_html_by_id(cls, id=1, html_path=None):
        item = cls.get_one(where_id=id)
        html = item.get_html()

        if not html_path:
            html_path = '%s/%s_id_%d.html' % (appConfig.get_desktop_path(), cls.get_table_name(), id)
        FileUtils.to_html_file(html_path, html)
        return html

    def set_data_null(self):
        self.delete_html(self.id)

    @classmethod
    def update_html_to_1(cls):
        return cls.objects.update(unset__has_html_1=1)

    @classmethod
    def delete_all_html(cls):
        task = FileTask(0, cls.get_collection_name(), html_path=cls.get_html_path())
        task.delete_all()
        cls.update_html_to_1()
        print('INFO: Delete all folder %s' % task.get_path())

    @classmethod
    def get_tmp_class(cls, class_name='', level=1, other_db=False): # type: (str, int, bool) -> BaseDocument
        class_name = 'zz_tmp_' + class_name + '_' + str(level)
        clazz =  cls.get_class(class_name, other_db=other_db)
        clazz.is_tmp = True
        return clazz

    @classmethod
    def get_class(cls, class_name='', other_db=False, version=1): # type: (str, bool, int) -> BaseDocument
        if other_db:
            from swissarmykit.db.other_mongodb import OtherBaseDocument
            # noinspection PyTypeChecker
            class_: BaseDocument = type(class_name, (OtherBaseDocument,), {})
        else:
            # noinspection PyTypeChecker
            class_: BaseDocument = type(class_name, (BaseDocument,), {})
        return class_

    @classmethod
    def done_query(cls):
        log = LoggerUtils.instance()
        print()
        log.info('BaseDocument: ', cls.get_collection_name(), '. Last offset: ', _counter.offset - 1)

    @classmethod
    def zip_data_to_desktop(cls):
        name = cls.get_collection_name()
        FileUtils.mkdir(appConfig.USER_DESKTOP + '/' + name)

        # html_path = FileTask(0, cls.get_collection_name()).get_path()
        # zip_name = '%s/%s/html_%s' % (appConfig.USER_DESKTOP, name, name)
        # FileUtils.zip_dir(zip_dir=html_path, zip_name=zip_name)

        program = '"C:/Program Files/MongoDB/Server/4.2/bin/mongodump.exe"'
        Command.exec('%s --db %s --collection %s --gzip --archive > %s/%s/%s.gz' % (program, cls.get_db_name(), name, appConfig.USER_DESKTOP, name, name))

    @classmethod
    def sync_from_other(cls):
        pass

    @classmethod
    def sync_to_other(cls):
        pass


    @classmethod
    def print_all_row(cls):
        for row in cls.objects: print(row.to_json())

    def get_json(self, fields=None): # type: (list) -> dict
        ''' fields=[]  '''
        if fields:
            return self.to_mongo(fields=fields)
        return self.to_mongo()

    def get_created_at(self):
        return self.id.generation_time()

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        if hasattr(self, 'url'):
            return '(%s %s)' % (str(self.id), getattr(self, 'url'))
        return str(self.id)

if __name__ == '__main__':

    wiki = BaseDocument.get_class('WikiPage')
    # wiki.new_field = StringField()
    #
    # # seed Data
    # wiki.save_url('test2', attr={'name': '2', 'has_html_1': False}, update_modified_date=True)
    # wiki.save_url('test3', attr={'name': '3', 'has_html_1': True})
    # wiki.save_url('test4', attr={'name': '4'})
    # wiki.save_url('test5', attr={'name': '5', 'has_html_1': True}, update_modified_date=True)
    #
    # print(wiki.count())

    wiki.zip_data_to_desktop()

    # for item in wiki.get_one(-1):
    #     print(item.get_created_at())




    # page = wiki()
    # page.data = {'test': 4, 'ds': 2}
    # page.name = '3333'
    # page.url = 'willnguyen.work'
    # page.save()

    # wiki.delete_html(lst=['5dcbfb827742180574512298', '5dcc2a48882d4c7180ca1137'])
    # item = wiki.get_by_url('willnguyen.work5')
    # print(wiki.get_ids())

    # for item in wiki.get_one(-1):
    #     print('record', item)

    # obj = wiki.save_url('willnguyen.work7')
    # print(obj.get_html())

    # print(WikiPage.insert_record({'url': 'fdfd', 'name': 'dd', 'data': {"33":3}}))
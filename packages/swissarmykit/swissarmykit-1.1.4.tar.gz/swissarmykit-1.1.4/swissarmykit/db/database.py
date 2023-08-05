# coding=utf-8

import json
import csv
from pprint import pprint
from peewee import *

from playhouse.shortcuts import model_to_dict
from swissarmykit.db.schema import SchemaObj
from swissarmykit.office.excelutils import ExcelUtils
from swissarmykit.utils.stringutils import StringUtils
from swissarmykit.utils.fileutils import FileUtils

try: from definitions_prod import *
except Exception as e: pass # Surpass error. Note: Create definitions_prod.py

class RecordModel(Model):

    @classmethod
    def get_db(cls, database=appConfig.DATABASE_NAME):
        ''' Ref: https://stackoverflow.com/questions/15559468/why-is-peewee-including-the-id-column-into-the-mysql-select-query
            Every table must have id column'''

        if not appConfig:
            raise Exception('Must import definitions.py which contains: appConfig: appConfig = appConfig.instance()')

        if appConfig.is_use_mysql():
            config = appConfig.config.get('mysql')
            return MySQLDatabase(host=config.get('host'), port=config.get('port'), user=config.get('user'),
                                 passwd=config.get('pass'), database=database)
        else:
            return SqliteDatabase(appConfig.DATABASE_PATH + '/' + database)

    @classmethod
    def _return_boolean_sql(cls, sql):
        cursor = cls.execute_sql(sql=sql)
        re = cursor.fetchone()
        return re and re[0]

    @classmethod
    def count(cls):
        return cls._return_boolean_sql('SELECT COUNT(*) FROM %s;' % cls.get_table_name())

    @classmethod
    def delete_html(cls, id=None, lst=None):
        sql = 'DELETE FROM html_file WHERE id IN (%s)' % (','.join(lst) if lst else str(id))
        return cls.execute_sql(sql=sql)

    @classmethod
    def truncate_table(cls):
        if appConfig.is_use_mysql():
            sql = 'TRUNCATE TABLE %s;' % cls.get_table_name()
            print('INFO: Truncate table %s' % cls.get_table_name())
            return cls.execute_sql(sql=sql)
        else:
            cls.recreate_table()

    @classmethod
    def exists_id(cls, id):
        cursor = cls.execute_sql('select * from %s where id=%d' % (cls.get_table_name(),id))
        re = cursor.fetchone()
        return re != None

    @classmethod
    def exists(cls, col:str, val):
        value = val
        if isinstance(val, str):
            value = '"%s"' % val.replace('%', '%%') #  Because not enough arguments for format string, query % args in peewee

        return cls._return_boolean_sql('select exists(select * from %s where %s=%s limit 1);' % (cls.get_table_name(), col, value))

    @classmethod
    def exists_html(cls, val=''):
        value = val
        if isinstance(val, str):
            value = '"%s"' % val.replace('%', '%%') #  Because not enough arguments for format string, query % args in peewee

        return cls._return_boolean_sql('select html_id from %s where url=%s limit 1;' % (cls.get_table_name(), value))

    @classmethod
    def get_or_create_custom(cls, where_dict):
        query = cls.select()
        for field, value in where_dict.items():
            query = query.where(getattr(cls, field) == value)
        return query

    @classmethod
    def update_or_create(cls, data=None, ids_name=None, return_obj=False): # type: (dict, str, bool) -> RecordModel

        def get_user_obj(data, ids_name):
            where = {}
            if ids_name:
                for i in ids_name.split(','):
                    id = i.strip()
                    where[id] = data.get(id)

                user, created = cls.get_or_create(**where)
            else:
                user, created = cls.get_or_create(id=data.get('id'))

            return user, created

        if data:
            user, created = get_user_obj(data, ids_name)

            for key, value in data.items():
                setattr(user, key, value)
            status = user.save()
            if return_obj:
                return user
            else:
                return status
        return False

    @classmethod
    def dump_mysql_of_this_table(cls):
        ''' Dumps main table '''
        table = cls.get_table_name()
        file0 = appConfig.HTML_PATH + os.sep + table
        file1 = cls.dump_on_query_by_id()

        files = [file1, file0]

        file_name = appConfig.get_desktop_path() + '/' + table + '_sql.zip'
        FileUtils.zipfiles(files, file_name=file_name)

    @classmethod
    def dump_mysql_to_sqlite(cls):
        '''
        :return: Use tool to Export to csv or json instead. Not work now!
        '''
        import subprocess

        table = cls.get_table_name()
        file1 = cls.dump_on_query_by_id()
        program = appConfig.BIN_PATH + os.sep + 'mysql2sqlite'

        command = '%s %s > %s/%s_lite.sql' % (program, file1, appConfig.USER_DESKTOP, table)
        command = command.replace('\\', '/').replace('C:', '/mnt/c')
        subprocess.call(command, shell=True)
        print('INFO: Execute ', command.split(' '))


    @classmethod
    def dump_on_query_by_id(cls, ids: list = None, path=None, file_name=None, table=None):
        ''' Ref: https://stackoverflow.com/questions/935556/mysql-dump-by-query
            mysqldump -u root -proot --where="id in (1,2)" sale test_auto > auto_test.sql
        '''

        if not path:
            path = appConfig.get_desktop_path()

        table = table if table else cls.get_table_name()
        mydb = cls.db_name

        if not ids:
            # if table in ['html_file', 'extra_column']:
            #     return ''  # Prevent extract all big table.
            query = ''
        else:
        #     id_lst = []
        #     for id in ids:
        #         id_lst.append(str(id))

            query = '--where="id > %d and id < %d"' % (ids[0], ids[1])
        output = '%s/%s.sql' % (path, file_name if file_name else table)
        command = 'mysqldump -u root -proot %s %s %s > %s' % (query, mydb, table, output)

        os.system(command)
        print('INFO: Execute ', command)
        return output

    @classmethod
    def get_first_rows(cls): # type: () -> RecordModel
        return cls.select().limit(1).first()

    @classmethod
    def insert_on_duplication(cls, data=None):
        ''' Example:
        d.insert_on_duplication(data={'id': 1, 'id_other': 5, 'name': 'aa'})
        INSERT INTO dbconnect_table (id,id_other,name) VALUES (1,5,"aa") ON DUPLICATE KEY UPDATE id=1,id_other=5,name="aa";
        '''
        sql = '''INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s;'''

        table = cls.get_table_name()
        keys = [key for key in data.keys()]
        values = ['"%s"' % value if isinstance(value, str) else str(value) for value in data.values()]
        s_1 = table
        s_2 = ','.join(keys)
        s_3 = ','.join(values)

        dup = [] # ... ON DUPLICATE KEY UPDATE id=1,id_other=5,name="aa";
        for i, key in enumerate(keys):
            dup.append('{}={}'.format(key, values[i]))
        s_4 = ','.join(dup)
        sql = sql % (s_1, s_2, s_3, s_4)

        # print('INFO', cls.db_name, table, sql) # Debug...
        return cls.execute_sql(sql=sql)

    @classmethod
    def create_table_if_not_exists(cls, unique_lst=None):
        if cls.table_exists():
            return False
        sql = cls.get_schema(unique_lst=unique_lst, create_if_not_exist=True)
        re = cls.execute_sql(sql)
        if not appConfig.is_use_mysql() and 'url' in sql:
            table = cls.get_table_name()
            cls.execute_sql('CREATE UNIQUE INDEX url_%s on %s (url);' % (table, table))

        print('Create successful. %s' % sql)
        return re

    @classmethod
    def create_fields_if_not_exists(cls):

        for name, db_type in cls._meta.fields.items():
            pass
            # todo:
        # sql = cls.get_schema(create_if_not_exist=True)
        # re = cls.execute_sql(sql)
        # print('Create successful. %s' % sql)
        # return re

    @classmethod
    def recreate_table(cls, unique_lst=None):
        sql = cls.get_schema(unique_lst=unique_lst)
        re = cls.execute_sql(sql)
        print('Re-create successful. %s' % sql)
        return re

    @classmethod
    def print_database_info(cls):
        print('Database: %s. Table: %s\n%s' % (cls.db_name, cls.get_table_name, cls._meta))

    @classmethod
    def print_schema(cls, unique_lst=None):
        print('\n\n%s\n\n' % (cls.get_schema(unique_lst=unique_lst)))
        exit(0)

    @classmethod
    def get_all_schemas(cls):
        cursor = cls.get_db().execute_sql("show databases;")
        schemas = cursor.fetchall()
        schemas = [x[0] for x in schemas]
        return schemas

    @classmethod
    def show_tables(cls, database=''):
        tables = cls.get_all_tables(database=database)
        pprint(tables)
        return tables

    @classmethod
    def get_all_tables(cls, database=''):
        database = database if database else cls.db_name
        cursor = cls.get_db(database=database).execute_sql("show tables;")
        tables = cursor.fetchall()
        tables = [x[0] for x in tables]
        return tables

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def get_name(cls):
        return cls.get_table_name()

    @classmethod
    def get_all_fields(cls, database='', table=''):
        database = database if database else cls.db_name
        table = table if table else cls.get_table_name()
        cursor = cls.get_db(database=database).execute_sql('''
            select * from information_schema.columns
            where table_schema = '%s' && table_name = '%s'
            order by table_name,ordinal_position
        ''' % (database, table))
        schemas = cursor.fetchall()
        return [SchemaObj(x) for x in schemas]

    @classmethod
    def get_class_def(cls, table='', base_model='BaseModel'):
        fields = cls.get_all_fields(table=table)
        lines = ''
        for field in fields:
            lines += field.get_def_text()

        class_def = '''from peewee import *\n
class %s(%s):\n%s    
        ''' % (table, base_model, lines)

        return class_def

    @classmethod
    def get_schema(cls, unique_lst=None, create_if_not_exist=False):
        table = cls.get_table_name()
        is_use_mysql = appConfig.is_use_mysql()

        if create_if_not_exist:
            schema = 'CREATE TABLE IF NOT EXISTS `%s` (\n' %  table
        else:
            # cls.drop_table()
            schema = 'CREATE TABLE `%s` (\n' %  table

        for name, db_type in cls._meta.fields.items():
            _type = db_type.field_type.lower()
            schema += '\t' + QueryBuilder.get_dll(name, _type, unique_lst, is_use_mysql) + '\n'

        if is_use_mysql:
            schema += '\tPRIMARY KEY (`id`)'
            if 'url' in cls._meta.fields.keys():
                schema += ',\n\tUNIQUE KEY `url` (`url`) USING BTREE'

            if unique_lst:
                for u in unique_lst:
                    schema += ',\n\tUNIQUE KEY `%s` (`%s`) USING BTREE' % (u, u)

            schema += ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;'
        else:
            schema = schema.rstrip(',\n') + ');'

        return schema

    # TODO: fix later
    @classmethod
    def get_id(cls, where=None):
        return RecordModel.select('id').where(where).get().id


    @classmethod
    def insert_record(cls, data=None):
        return cls.create(**data)

    @classmethod
    def get_fields(cls):
        lst = []
        for f in cls._meta.sorted_field_names:
            lst.append(f)
        return lst

    @classmethod
    def export_data_to_csv(cls, lst=None, headers=None, file_name=None):
        file = appConfig.EXCEL_PATH + '/' + (file_name if file_name else cls.get_table_name()) + '.csv'
        print('INFO: Total: ', len(lst))
        if headers:
            lst.insert(0, headers)

        with open(file, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            for i, l in enumerate(lst):
                try:
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
    def export_data_to_excel(cls, lst=None, headers_order=None, col_name='data', limit=-1, offset=0, format='', headers=None,
                             remove_invalid_char=False, debug=False, auto_order_header=False, sort_header=None, file_name='', write_one_by_one=False):
        data_lst = []
        if lst != None:
            data_lst = lst[offset:limit] if limit > 0 else lst[offset:]
        else:
            for item in cls.get_one(limit=limit, offset=offset, col_name=col_name, is_null_data=False):
                try:
                    data = StringUtils.get_valid_text_for_excel(getattr(item, col_name)) if remove_invalid_char else  getattr(item, col_name)
                    data_lst.append(json.loads(data))
                except Exception as e:
                    print('ERROR: ', item)

        # Auto get header_order
        if auto_order_header:
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
                for key in headers_order:
                    headers[key] = 1
                headers_order = list(headers.keys())
            else:
                headers_order = new_order

        if debug:
            print(data_lst)

        if not data_lst:
            print('ERROR: Empty list to export to Excel')
            return False

        if not file_name:
            file_name = appConfig.EXCEL_PATH + '/' + cls.get_table_name() + '.xlsx'

        ExcelUtils.json_to_openpyxl(data_lst, headers_order=headers_order, headers=headers, file_name=file_name, write_one_by_one=write_one_by_one)

    @classmethod
    def export_header_key(cls, col_name='data'):
        headers = {}
        for item in cls.select():
            if col_name == 'data':
                data = item.get_data()
            elif col_name == 'extra':
                data = item.get_extra_col()
            else:
                raise Exception('col_name undefined')

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
        item = cls.select('id').where(cls.id == id)
        path = path if path else appConfig.USER_DESKTOP + '/_test_html.html'
        FileUtils.to_html_file(path, item.html)
        print('INFO: output to html of %d:%s' % (id, path))

    @classmethod
    def execute_sql(cls, sql, params=None, database=''):
        ''' https://stackoverflow.com/questions/18500956/python-peewee-execute-sql-example '''
        db = cls.get_db(database if database else cls.db_name)
        return db.execute_sql(sql, params=params)

    @classmethod
    def get_by_url(cls, url): # type: (str) -> RecordModel
        ''' Note: this method for scraping, but used many place'''
        if not url:
            return 0

        return cls.select().where(cls.url == url).first()

    @classmethod
    def get_html_by_url(cls, url): # type: (str) -> str
        item = cls.get_by_url(url)
        if item:
            return item.get_html()
        return ''

    @classmethod
    def get_urls(cls):
        return [item.url for item in cls.select(cls.url)]

    @classmethod
    def get_headers(cls, remove=(), remove_contains=(), col_name='data'):
        headers = {}
        for item in cls.get_one(-1, col_name=col_name):
            data = item.get_data()
            if not data:
                continue

            for h in data:
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
        return [item.id for item in cls.select(cls.id)]

    @classmethod
    def exists_url(cls, val, is_cache=True):
        if is_cache:
            if not hasattr(cls, '__cache_url'):
                lst = cls.get_urls()
                setattr(cls, '__cache_url', lst)
            else:
                lst = getattr(cls, '__cache_url')
            return val in lst

        return cls.exists('url', val)

    @classmethod
    def find_by_url(cls, val):
        return cls.select().where(cls.url == val).get()

    @classmethod
    def save_id(cls, id, name=None, url=None, others=None, html=None, force_insert=False): # type: (int, str, str, dict) -> RecordModel
        ''' Note: this method for scraping, but used many place'''

        if not id:
            return 0

        data = {'id': id, 'url': url if url else str(id)} # Must have url to distinguish
        if name:
            data['name'] = name

        if others:
            data.update(others)

        if force_insert:
            obj =  cls.create(**data)
        else:
            obj =  cls.update_or_create(data=data, ids_name='id', return_obj=True)

        if html:
            obj.save_html(html)
    @classmethod
    def get_all_id(cls): # type: () -> [()]
        sql = 'select id from %s' % (cls.get_table_name())
        cursor = cls.execute_sql(sql)
        return [row[0] for row in cursor.fetchall()]

    @classmethod
    def get_id_list_not_exist(cls, fr, to): # type: (int, int) -> list
        table = cls.get_table_name()
        sql = 'select id from %s where id between %s and %s' % (table, fr, to)
        print('Find id not exist on list sql: ', sql)
        cursor = cls.execute_sql(sql)
        re = [row[0] for row in cursor.fetchall()]
        return [i for i in range(fr, to) if i not in re]

    @classmethod
    def save_url(cls, url, name=None, html=None, data=None, extra=None, attr=None, force_insert=False): # type: (str, str, str, dict, dict, dict, bool) -> RecordModel
        ''' Note: this method for scraping, but used many place'''
        if not url:
            return 0

        _data = {'url': url}
        if name:
            _data['name'] = name
        if data:
            _data['data'] = json.dumps(data)
        if extra:
            _data['extra'] = json.dumps(extra)
        if attr:
            _data.update(attr)

        if force_insert:
            obj = cls.create(**_data)
        else:
            obj = cls.update_or_create(data=_data, ids_name='url', return_obj=True)
        if html:
            obj.save_html(html)

        return obj

    @classmethod
    def get_records_by_query_builder(cls, q):   # type: (QueryBuilder) -> dict
        sql = ''
        try:
            order_by =  ''
            if q.get_sort():
                order_by = 'ORDER BY ' + ', '.join(q.get_sort())
            sql = 'SELECT * FROM %s %s LIMIT %d, %d' % (cls.get_table_name(), order_by,  q.get_offset(), q.get_limit())

            cursor = cls.execute_sql(sql)
            data = [row for row in cursor.fetchall()]
            return {
                'meta': {'total': cls.count(), 'fields': cls.get_fields(), 'count': len(data), 'page': q.page, 'limit': q.get_limit()},
                'data': data
            }
        except Exception as e:
            print('ERROR', e, sql)

    @classmethod
    def print_all_row(cls):
        cursor = cls.execute_sql('select * from %s;' % cls.get_table_name())
        for row in cursor.fetchall():
            print(row)

    def __str__(self):
        ''' to json: https://stackoverflow.com/questions/21975920/peewee-model-to-json '''
        return str(model_to_dict(self, backrefs=True))

    def __repr__(self):
        return '(%d %s)' % (self.id, self.url)

class QueryBuilder:
    MAX_PER_PAGE = 500

    def __init__(self):
        self.per_page = QueryBuilder.MAX_PER_PAGE
        self.page = 0
        self.sort = []

    def set_sort(self, column_name='', asc='ASC'):
        if column_name:
            self.sort.append(column_name + ' ' + asc)

    def set_page(self, page: int = 0):
        self.page = page

    def set_per_page(self, per_page: int = 0):
        self.per_page = per_page if per_page else QueryBuilder.MAX_PER_PAGE

    def get_limit(self):
        return self.per_page if self.per_page < QueryBuilder.MAX_PER_PAGE + 1 else QueryBuilder.MAX_PER_PAGE

    def get_offset(self):
        return self.page * self.get_limit()

    def get_sort(self):
        return self.sort

    @staticmethod
    def get_dll(name, type, unique_lst, is_use_mysql=True):
        if is_use_mysql:
            # MySQL
            if name == 'id':
                if type == 'int':
                    return "`id` int(10) unsigned NOT NULL AUTO_INCREMENT,"
                elif type == 'bigint':
                    return "`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,"
                else:
                    raise Exception("id field must auto increase, and integer type.")

            elif type == 'text':
                if name == 'html':
                    return "`%s` long%s," % (name, type)
                return "`%s` %s," % (name, type)

            elif type == 'int':
                return "`%s` int(11) DEFAULT '0'," % name

            elif type == 'bigint':
                return "`%s` bigint(20) DEFAULT '0'," % name

            elif type == 'smallint':
                return "`%s` tinyint(4) DEFAULT '0'," % name

            elif type == 'varchar':
                return "`%s` varchar(1000) DEFAULT NULL," % name
            return ''
        else:
            # SQLite
            unique = 'UNIQUE' if unique_lst and name in unique_lst else ''

            if name == 'id':
                if type in ['int', 'bigint']:
                    return "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                else:
                    raise Exception("id field must auto increase, and integer type.")

            elif type in ['text', 'varchar']:
                if name == 'url':
                    return "`%s` TEXT NOT NULL UNIQUE," % name
                return "`%s` TEXT %s," % (name, unique)

            elif type  in ['int', 'bigint', 'smallint']:
                if name == 'html_id':
                    return "`%s` INTEGER DEFAULT 0," % name
                return "`%s` INTEGER," % name

            return ''


if __name__ == '__main__':
    r = RecordModel()
    from definitions import * # Must have definitions file

    class Test(RecordModel):
        id = IntegerField()  # Will be primary key.
        url = TextField()
        name = TextField()
        html_id = IntegerField()

    t = Test()
    print(t.get_schema())

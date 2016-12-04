from __future__ import with_statement
from contextlib import closing

import os
import sqlite3
import sys

class FeedsDB(object):

    # The SQLite3 database file and schema. No path checking here because I assume the
    # files will live in same directory as the scraper and this module. In principle
    # SQLite3 could be replaced by any other RDBMS with a Python binding, with
    # minimal changes here.
    DB_FILE = 'feeds.db'
    DB_SCHEMA = 'schema.sql'

    @classmethod
    def setup(cls):
            if not os.path.exists(cls.DB_FILE):
                print('\n\tDB does not exist, creating DB {} ... '.format(cls.DB_FILE))
                with sqlite3.connect(cls.DB_FILE, timeout=5000) as db:
                    with open(cls.DB_SCHEMA, 'rt') as f:
                       schema = f.read()
                    print('\tcreating DB schema')
                    db.executescript(schema)

    def _insert_row(self, table, columns, values):
        # SQLite3 supports multiple threads and processes connecting to and reading
        # from the database via a shared lock, but only permits one thread or process
        # to write to the database at any given time via a so-called reserved lock.
        #
        # https://www.sqlite.org/atomiccommit.html
        #
        # As the scraper runs this method is called in the context of multiple processes
        # trying to write to the database, but each much wait its turn for the reserved
        # lock to be released, which is where the connection timeout is relevant. Not
        # specifying a timeout value for the connection means that a process may have too
        # long for SQLite3 to release the lock in which case it throws an OperationalError.
        # I've used the default timeout period of 5 seconds.
        with sqlite3.connect(self.DB_FILE, timeout=5000) as db:
            with closing(db.cursor()) as cursor:
                try:                    
                    statement = """insert into {} ({}) values ({})""".format(
                        table, ','.join(columns), '{}'.format(','.join(['?'] * len(values)))
                    )
                    cursor.execute(
                        statement,
                        tuple(values)
                    )
                except sqlite3.DatabaseError as e:
                    print('\tIN DB: ERROR: {}'.format(str(e)))
                else:
                    db.commit()
                    return cursor.lastrowid
       
    def save(self, model_inst):
        # Note: I assume that the model class names are capitalized versions of
        # the corresponding table names and the model field names are identical to the
        # corresponding table column names after stripping the '_' prefix. This
        # assumption makes it easier to write this method generically and for the
        # scraper calling method to save model instances to the db.
        table = model_inst.__class__.__name__.lower()
        print('\tDB: saving object ({}, {}) to database table {}'.format(model_inst, model_inst.uuid, table))
        columns = [key.strip('_') for key in model_inst.__dict__]
        values = [model_inst.__dict__[key] if model_inst.__dict__[key] else '' for key in model_inst.__dict__]
        if table == 'tag':
            print('\tDB: inserting values {} for object ({}, {})'.format(values, model_inst, model_inst.uuid))
        self._insert_row(table, columns, values)

#  Drakkar-Software OctoBot-Backtesting
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
from sqlite3 import OperationalError, DatabaseError

import aiosqlite

from octobot_backtesting.data import DataBaseNotExists
from octobot_backtesting.enums import DataBaseOrderBy
from octobot_commons.logging.logging_util import get_logger


class DataBase:
    TIMESTAMP_COLUMN = "timestamp"
    DEFAULT_ORDER_BY = TIMESTAMP_COLUMN
    DEFAULT_SORT = DataBaseOrderBy.DESC.value
    DEFAULT_WHERE_OPERATION = "="
    DEFAULT_SIZE = -1
    CACHE_SIZE = 50

    def __init__(self, file_name):
        self.file_name = file_name
        self.logger = get_logger(self.__class__.__name__)

        self.tables = []
        self.cache = {}

        self.connection = None
        self.cursor = None

    async def initialize(self):
        try:
            self.connection = await aiosqlite.connect(self.file_name)
            self.cursor = await self.connection.cursor()
            await self.__init_tables_list()
        except (OperationalError, DatabaseError) as e:
            raise DataBaseNotExists(e)

    async def create_index(self, table, columns):
        await self.__execute_index_creation(table, '_'.join(columns), ', '.join(columns))

    async def __execute_index_creation(self, table, name, columns):
        await self.cursor.execute(f"CREATE INDEX index_{table.value}_{name} ON {table.value} ({columns})")

    async def insert(self, table, timestamp, **kwargs):
        if table.value not in self.tables:
            await self.__create_table(table, **kwargs)

        # Insert a row of data
        inserting_values = [f"'{value}'" for value in kwargs.values()]
        await self.__execute_insert(table, self.__insert_values(timestamp, ', '.join(inserting_values)))

    async def insert_all(self, table, timestamp, **kwargs):
        # TODO refactor with : cursor.executemany("INSERT INTO my_table VALUES (?,?)", values)
        if table.value not in self.tables:
            await self.__create_table(table, **kwargs)

        insert_values = []

        for index, values in enumerate(timestamp):
            # Insert a row of data
            inserting_values = \
                [f"'{value if not isinstance(value, list) else value[index]}'" for value in kwargs.values()]
            insert_values.append(self.__insert_values(values, ', '.join(inserting_values)))

        await self.__execute_insert(table, ", ".join(insert_values))

    def __insert_values(self, timestamp, inserting_values) -> str:
        return f"({timestamp}, {inserting_values})"

    async def __execute_insert(self, table, insert_items) -> None:
        await self.cursor.execute(f"INSERT INTO {table.value} VALUES {insert_items}")

        # Save (commit) the changes
        await self.connection.commit()

    async def select(self, table, size=DEFAULT_SIZE, order_by=DEFAULT_ORDER_BY, sort=DEFAULT_SORT, **kwargs):
        return await self.__execute_select(table=table,
                                           where_clauses=self.__where_clauses_from_kwargs(**kwargs),
                                           additional_clauses=self.__select_order_by(order_by, sort),
                                           size=size)

    async def select_max(self, table, max_columns, selected_items=None, group_by=None, **kwargs):
        return await self.__execute_select(table=table,
                                           select_items=f"{self.__max(max_columns)}"
                                                        f"{', ' if selected_items else ''}"
                                                        f"{self.__selected_columns(selected_items)}",
                                           where_clauses=self.__where_clauses_from_kwargs(**kwargs),
                                           group_by=self.__select_group_by(group_by) if group_by else "")

    async def select_min(self, table, min_columns, selected_items=None, group_by=None, **kwargs):
        return await self.__execute_select(table=table,
                                           select_items=f"{self.__min(min_columns)}"
                                                        f"{', ' if selected_items else ''}"
                                                        f"{self.__selected_columns(selected_items)}",
                                           where_clauses=self.__where_clauses_from_kwargs(**kwargs),
                                           group_by=self.__select_group_by(group_by) if group_by else "")

    async def select_from_timestamp(self, table, timestamps: list, operations: list,
                                    size=DEFAULT_SIZE, order_by=DEFAULT_ORDER_BY, sort=DEFAULT_SORT, use_cache=False,
                                    **kwargs):
        timestamps_where_clauses = self.__where_clauses_from_operations(keys=[self.TIMESTAMP_COLUMN] * len(timestamps),
                                                                        values=timestamps,
                                                                        operations=operations,
                                                                        should_quote_value=False)
        timestamps_where_clauses = f"AND {timestamps_where_clauses}" if timestamps_where_clauses else ''
        return await self.__execute_select(table=table,
                                           where_clauses=f"{self.__where_clauses_from_kwargs(**kwargs)} "
                                                         f"{timestamps_where_clauses}",
                                           additional_clauses=self.__select_order_by(order_by, sort),
                                           size=size)

    def __where_clauses_from_kwargs(self, should_quote_value=True, **kwargs) -> str:
        return self.__where_clauses_from_operations(list(kwargs.keys()), list(kwargs.values()), [],
                                                    should_quote_value=should_quote_value)

    def __where_clauses_from_operation(self, key, value, operation=DEFAULT_WHERE_OPERATION, should_quote_value=True):
        return f"{key} {operation if operation is not None else self.DEFAULT_WHERE_OPERATION} " \
               f"{self.__quote_value(value) if should_quote_value else value}"

    def __where_clauses_from_operations(self, keys, values, operations, should_quote_value=True):
        return " AND ".join([self.__where_clauses_from_operation(keys[i],
                                                                 values[i],
                                                                 operations[i] if len(operations) > i else None,
                                                                 should_quote_value=should_quote_value)
                             for i in range(len(keys))
                             if values[i] is not None])

    def __select_order_by(self, order_by, sort):
        return f"ORDER BY " \
               f"{order_by if order_by is not None else self.DEFAULT_ORDER_BY} " \
               f"{sort if sort is not None else self.DEFAULT_SORT}"

    def __select_group_by(self, group_by):
        return f"GROUP BY {group_by}"

    def __quote_value(self, value):
        return f"'{value}'"

    def __max(self, columns):
        return f"MAX({self.__selected_columns(columns)})"

    def __min(self, columns):
        return f"MIN({self.__selected_columns(columns)})"

    def __selected_columns(self, columns=None):
        return ','.join(columns) if columns else ""

    async def __execute_select(self, table, select_items="*", where_clauses="", additional_clauses="", group_by="",
                               size=DEFAULT_SIZE):
        try:
            await self.cursor.execute(f"SELECT {select_items} FROM {table.value} "
                                      f"{'WHERE' if where_clauses else ''} {where_clauses} "
                                      f"{additional_clauses} {group_by}")
            return await self.cursor.fetchall() if size == self.DEFAULT_SIZE else await self.cursor.fetchmany(size)
        except OperationalError as e:
            if not await self.check_table_exists(table):
                raise DataBaseNotExists(e)
            self.logger.error(f"An error occurred when executing select : {e}")
        return []

    async def check_table_exists(self, table) -> bool:
        await self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table.value}'")
        return await self.cursor.fetchall() != []

    async def check_table_not_empty(self, table) -> bool:
        await self.cursor.execute(f"SELECT count(*) FROM '{table.value}'")
        row_count = await self.cursor.fetchone()
        return row_count[0] != 0

    async def __create_table(self, table, with_index_on_timestamp=True, **kwargs) -> None:
        try:
            columns: list = list(kwargs.keys())
            await self.cursor.execute(
                f"CREATE TABLE {table.value} ({self.TIMESTAMP_COLUMN} datetime, {' text, '.join([col for col in columns])})")

            if with_index_on_timestamp:
                await self.create_index(table, [self.TIMESTAMP_COLUMN])

                for i in range(1, round(len(columns) / 2) + 1):
                    await self.create_index(table, [self.TIMESTAMP_COLUMN] + [columns[u] for u in range(0, i)])

        except OperationalError:
            self.logger.error(f"{table} already exists")
        finally:
            self.tables.append(table.value)

    async def __init_tables_list(self):
        await self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
        self.tables = await self.cursor.fetchall()

    async def stop(self):
        if self.connection is not None:
            await self.connection.close()

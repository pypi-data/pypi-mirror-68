#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import tests.config as cfg

from taz.table import Table
from taz.storage_account import StorageAccount


class TableTests(unittest.TestCase):
    def setUp(self):
        self.storage_account = self.storage_account = StorageAccount(
            connection_string=cfg.tables["storage_connection_string"]
        )
        self.table_name = cfg.tables["table_name"]
        self.table = Table(self.table_name, storage_account=self.storage_account)
        self.entity1 = {
            "PartitionKey": "part1",
            "RowKey": "row1",
            "field1": "val1",
        }
        self.entity2 = {
            "PartitionKey": "part1",
            "RowKey": "row2",
            "field1": "val2",
        }
        self.entity3 = {
            "PartitionKey": "part2",
            "RowKey": "row1",
            "field1": "val3",
        }
        self.entity4 = {
            "PartitionKey": "part1",
            "RowKey": "row2",
            "field2": "val4",
        }

    def test_010_list(self):
        for table in self.storage_account.list_tables():
            print(table.name)

    def test_030_create(self):
        self.assertTrue(self.table.create().exists())

    def test_040_exists(self):
        self.assertTrue(self.table.exists())

    def test_050_insert(self):
        self.table.insert_entity(self.entity1)
        self.table.insert_entity(self.entity2)

    def test_060_upsert(self):
        self.entity1["field1"] = "val1_mod"
        self.table.upsert_entity(self.entity1)
        self.table.upsert_entity(self.entity3)

    def test_070_merge(self):
        self.table.merge_entity(self.entity4)

    def test_080_get_entity(self):
        self.assertEqual(self.table.get_entity("part1", "row2")["field1"], "val2")
        self.assertEqual(self.table.get_entity("part1", "row2")["field2"], "val4")
        self.assertEqual(self.table.get_entity("part1", "row1")["field1"], "val1_mod")
        self.assertEqual(self.table.get_entity("part2", "row1")["field1"], "val3")

    def test_090_delete_entity(self):
        (
            self.table.delete_entity("part1", "row1")
            .delete_entity("part1", "row2")
            .delete_entity("part2", "row1")
        )

    def test_100_delete(self):
        self.assertFalse(self.table.delete().exists())


if __name__ == "__main__":
    sys.argv.append("-v")
    unittest.main()

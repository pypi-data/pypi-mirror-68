#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: Azure Tables (Cosmos DB light)
"""

from azure.cosmosdb.table.models import Entity

from taz.storage_account import StorageAccount


class Table:
    def __init__(self, table_name: str, storage_account: StorageAccount):
        """Table class

        :param table_name: name of table
        :type table_name: str
        :param storage_account: [description]
        :type storage_account: StorageAccount
        """
        self.name = table_name
        self.storage_account = storage_account

    def create(self):
        self.storage_account.table_service_client.create_table(self.name)
        return self

    def exists(self):
        return self.storage_account.table_service_client.exists(self.name)

    def delete(self):
        self.storage_account.table_service_client.delete_table(self.name)
        return self

    def insert_entity(self, entity: dict):
        """insert entity

        :param entity: entity to insert (must content a PartitionKey and a RowKey)
        :type entity: dict
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.insert_entity(self.name, entity)
        return self

    def upsert_entity(self, entity: dict):
        """insert or replace entity

        :param entity: entity to upsert (must content a PartitionKey and a RowKey)
        :type entity: dict
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.insert_or_replace_entity(
            self.name, entity
        )
        return self

    def merge_entity(self, entity: dict):
        """insert or replace entity

        :param entity: entity to upsert (must content a PartitionKey and a RowKey)
        :type entity: dict
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.merge_entity(self.name, entity)
        return self

    def delete_entity(self, partition_key: str, row_key: str):
        """delete entity by partition and row keys

        :param partition_key: partition key
        :type partition_key: str
        :param row_key: row key
        :type row_key: str
        :return: return self object
        :rtype: taz.table.Table
        """
        self.storage_account.table_service_client.delete_entity(
            self.name, partition_key=partition_key, row_key=row_key
        )
        return self

    def get_entity(self, partition_key: str, row_key: str):
        """get entity by partition and row keys

        :param partition_key: partition key
        :type partition_key: str
        :param row_key: row key
        :type row_key: str
        :return: selected entity
        :rtype: azure.storage.table.models.Entity (can be used as a dict)
        """
        return self.storage_account.table_service_client.get_entity(
            self.name, partition_key=partition_key, row_key=row_key
        )

    def __str__(self):
        return self.name

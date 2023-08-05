#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Taz library: Storage Account
"""
import re
from azure.storage.blob import BlobServiceClient
from azure.cosmosdb.table.tableservice import TableService


class StorageAccount:
    def __init__(self, name=None, connection_string=None, key=None):
        """Define Storage Account Object

        connection_string or key + name are required

        :param name: storage account name
        :type name: str, optionnal
        :param connection_string: storage account connection string
        :type connection_string: str, optionnal
        :param key: key, defaults to None
        :type key: str, optional
        """
        self.name = name
        self.key = key
        self.connection_string = connection_string

        if self.name is None:
            self.name = re.search(";AccountName=(.*?);", self.connection_string)

        if self.connection_string is None:
            self.connection_string = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={};EndpointSuffix=core.windows.net".format(
                self.name, self.key
            )

        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )

        self.table_service_client = TableService(
            connection_string=self.connection_string
        )

    def list_tables(self):
        return self.table_service_client.list_tables()

    def list_containers(self, prefix=None):
        """ list storage account containers

        Returns:
            - azure.storage.blob.models.Container List: list of container, Container class attributes:
                - name
                - metadata
                - properties
        """
        return self.blob_service_client.list_containers(name_starts_with=prefix)

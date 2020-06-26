"""
Asset properties object.
Drive each asset properties and configurations

Configuration setup. WIP
Asset variations of such type:
    - material (texture)
    - geometry
    - light
    - fx

    CONTAIN: name | value

Asset configuration:
    CONTAIN: config_name | variation | value
"""

# TODO: design asset configuration

import sqlite3
import entities


class AssetData:
    def __init__(self, SQL_FILE_PATH, asset_id):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH
        self.asset_id = asset_id

        # Data attributes
        self.asset = None
        self.asset_type_dic = None  # entities.Asset.asset_types dict

        self.init_asset()

    def init_asset(self):

        # Get Asset from the database
        self.asset = self.get_asset(self.asset_id)

        # Detect asset type
        for asset_type in entities.Asset.asset_types:
            if entities.Asset.asset_types[asset_type]['id'] == self.asset.type:
                self.asset_type_dic = entities.Asset.asset_types[asset_type]

    def get_asset(self, asset_id):
        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE id=:id",
                       {'id': asset_id})

        asset_tuple = cursor.fetchone()

        connection.close()

        if asset_tuple:
            return entities.Converter.convert_to_asset([asset_tuple])[0]

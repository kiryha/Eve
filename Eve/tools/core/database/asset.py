"""
Asset properties object.
Drive each asset properties and configurations
"""

class AssetData:
    def __init__(self, SQL_FILE_PATH, asset_id):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH
        self.asset_id = asset_id

        # Data attributes
        self.asset = None
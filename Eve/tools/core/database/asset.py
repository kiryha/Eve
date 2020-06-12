"""
Asset properties object.
Drive each asset properties and configurations

"""

# TODO: design asset configuration

class AssetData:
    def __init__(self, SQL_FILE_PATH, asset_id):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH
        self.asset_id = asset_id

        # Data attributes
        self.asset = None

        self.init_asset()

    # Asset data operations
    def init_asset(self):

        self.asset = self.get_asset(self.asset_id)
        # self.get_configs()
        # self.get_variants()

    def get_asset(self, asset_id):

        pass
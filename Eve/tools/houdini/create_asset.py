import sys
import os

import hou

from core import database
from core import file_path
from core import settings

# Get data
eve_root = os.environ['EVE_ROOT']
asset_id = int(sys.argv[-1])
eve_data = database.EveData(settings.SQL_FILE_PATH.format(eve_root))
asset = eve_data.get_asset(asset_id)

# Create EveFilePath
file_type = database.EveFile.file_types['asset_hip']
file_path_asset = file_path.EveFilePath()

# Get asset_type dictionary
asset_type_dic = None
for asset_type in database.Asset.asset_types:
    if database.Asset.asset_types[asset_type]['id'] == asset.type:
        asset_type_dic = database.Asset.asset_types[asset_type]

# Create file path string
file_path_asset.build_path_asset_hip(file_type, asset_type_dic, asset.name, '001')
scene_path = file_path_asset.version_control()

# Save file
if scene_path:
    hou.hipFile.save(scene_path)

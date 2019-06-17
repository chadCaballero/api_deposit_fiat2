from apps.config import LOGGER_CONFIG
from utils.libs import check_resource

# print(os.path.isdir('~/logs_dev/'))
# print(os.path.isdir(FILE_PATH))
check_resource(folder=LOGGER_CONFIG['log_folder'])

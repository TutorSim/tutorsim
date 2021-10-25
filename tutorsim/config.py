import contexts
# Stores credential information
TELEGRAM_API_KEY='YOUR-TELEGRAM-BOT-KEY'

# Google Drive API, credentials
GOOGLE_SERVICE_KEY='YOUR-GOOGLE-SERVICE-KEY.json'

# Google Drive API, credentials
GOOGLE_SPREAD_SHEET='YOUR-GOOGLE-SPREADSHEET-NAME'

import os
if os.path.isfile("/root/instance/telegram_config.py"):
	from instance.telegram_config import *

if os.path.isfile("/root/instance/course_config.py"):
	from instance.course_config import *

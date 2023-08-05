
class ConfigDefault:

    @staticmethod
    def generate_config(file):
        data =  '''{
  "default": {
    "mysql": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "pass": "root"
    },
    "mongodb": {
      "host": "127.0.0.1:27017",
      "port": 27017,
      "user": "",
      "pass": ""
    },
    "redis": {
      "host": "127.0.0.1",
      "port": 6379,
      "db": 5
    },
    "database": "sale",
    "use_sqlite": false,
    "use_mongo_db": true,
    "images_path": "G:/data/download_images",
    "html_path": "G:/data/html",
    "database_path": "G:/data/database",
    "user_path": "C:/Users/Will",
    "chrome_driver": "C:/Users/Will/Desktop/code/ai_/app/bin/Windows/chromedriver.exe"
  },
  "dev": {
    "env": "dev",
    "google_sheet_credentials": "C:/Users/Will/Desktop/code/ai_/dist/config/credentials/credentials.json",
    "google_sheet_tokens": "C:/Users/Will/Desktop/code/ai_/dist/config/credentials/token.pickle"
  },
  "prod": {
    "env": "prod"
  },
  "mac": {
    "env": "mac",
    "google_sheet_credentials": "/Users/will/Desktop/code/ai_/dist/config/credentials/credentials.json",
    "google_sheet_tokens": "/Users/will/Desktop/code/ai_/dist/config/credentials/token.pickle"
  }
}'''
        text_file = open(file, 'w')
        n = text_file.write(data)
        text_file.close()
        print('INFO: Generate file: ', file)
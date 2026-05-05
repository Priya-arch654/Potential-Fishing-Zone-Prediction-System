# MongoDB Database Export

This directory contains the exported collections from the `pfz_database` MongoDB database.

To restore this data to your local MongoDB instance, run the following Python command from the root of the project to import the JSON files back into MongoDB:

```bash
python -c "import pymongo, json; from bson import json_util; client = pymongo.MongoClient('mongodb://localhost:27017/'); db = client['pfz_database']; import os, glob; [db[os.path.basename(f).replace('.json', '')].insert_many(json_util.loads(open(f).read())) for f in glob.glob('database_export/*.json') if json_util.loads(open(f).read())]"
```

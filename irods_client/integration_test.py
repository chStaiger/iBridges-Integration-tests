import sys
import os
print("Integration tests start ...")
summary = {}
summary['python_version'] = sys.version

try:
    from utils.json_config import JsonConfig
    from irodsConnector.manager import IrodsConnector
    summary['import_backend'] = "success"
except Exception as e:
    print(repr(e))
    summary['import_backend'] = "fail"

print("Loading configs ...")
ibridgesEnv = JsonConfig("/root/.ibridges/ibridges_config.json")
print("iBridges config:")
print(ibridgesEnv.config)
print()
irodsEnv = JsonConfig("/root/.irods/irods_environment.json")
print("iRODS config:")
print(irodsEnv.config)

print("Passing configs to irodsConnector ...")
ic = IrodsConnector()
ic.ibridges_configuration = ibridgesEnv
print(ic.ibridges_configuration.config)
ic.irods_env_file = irodsEnv.filepath
ic.irods_environment = irodsEnv
print(ic.irods_environment.config)


print("Connect with cached password:")
try:
    ic.connect()
    print("Valid iRODS session: ", ic.session.has_valid_irods_session())
    summary['iRODS_server_version'] = ic.session.server_version
    summary['authentication_cached_passwd'] = "success"
except Exception as e:
    summary['authentication_cached_passwd'] = repr(e)

print("Get home collection")
try:
    coll = ic.data_op.get_collection(ic.irods_environment.config.get('irods_home', '/'+ic.zone+'/home/'+ic.username))
    print(coll.path)
    summary['get_home_coll'] = "success"
except Exception as e:
    summary['get_home_coll'] = repr(e)

print("Get resources")
try:
    summary["resources"] = [resc for resc in ic.resources]
except Exception as e:
    summary["resources"] = repr(e)

print("Upload testdata folder")
try:
    coll = ic.data_op.get_collection(ic.irods_environment.config.get('irods_home', '/'+ic.zone+'/home/'+ic.username))
    ic.data_op.upload_data("/tmp/testdata", coll, ic.default_resc, size=0, force=True)
    uploadColl = ic.data_op.get_collection(coll.path+'/testdata')
    print("Uploaded data objects: ", str(uploadColl.data_objects))
    summary['upload_testdata_folder'] = "success"
except Exception as e:
    summary['upload_testdata_folder'] = repr(e)

print("Add metadata to collection")
try:
    ic.meta.add([uploadColl], 'key', 'value')
    print(uploadColl.metadata)
    summary['metadata_collection'] = uploadColl.metadata
except Exception as e:
    summary['metadata_collection'] = repr(e)

print("Download collection")
try:
    ic.data_op.download_data(uploadColl, "/tmp", 0, force=True)
    files = os.listdir("/tmp/"+uploadColl.name)
    os.system("rm -rf /tmp/"+uploadColl.name)
    summary['download_collecion'] = files
except Exception as e:
    summary['download_collecion'] = repr(e)

print("Remove metadata")
try:
    ic.meta.delete([uploadColl], 'key', 'value')
    print(uploadColl.metadata)
    summary['delete_metadata'] = 'success'
except Exception as e:
    summary['delete_metadata'] = repr(e)

print("Delete collection")
try:
    ic.data_op.delete_data(uploadColl)
    subcolls = [c.name for c in coll.subcollections]
    if "testdata" in subcolls:
        summary['delete_collection'] = 'failed'
    else:
        summary['delete_collection'] = 'success'
except Exception as e:
    summary['delete_collection'] = repr(e)
    

print("Close iBridges session")
try:
    del ic
    summary['session_cleanup'] = "success"
except Exception as e:
    summary['session_cleanup'] = repr(e)
    

print("Integration tests end")
print()
print("Summary")
for key, value in summary.items():
    print(key, ':', value)

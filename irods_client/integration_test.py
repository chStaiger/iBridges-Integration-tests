print("Integration tests start ...")
summary = {}

try:
    from utils.json_config import JsonConfig
    from irodsConnector.manager import IrodsConnector
    summary['Import_backend'] = "success"
except Exception as e:
    print(repr(e))
    summary['Import_backend'] = "fail"

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

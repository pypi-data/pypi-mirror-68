import os
import nose
import shutil
import yaml
import unittest
from sherlock.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="sherlock"
)
arguments, settings, log, dbConn = su.setup()

# # load settings
# stream = file(
#     "/Users/Dave/.config/sherlock/sherlock.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/example_settings3.yaml", 'r')
settings = yaml.load(stream)
stream.close()


import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

# xt-setup-unit-testing-files-and-folders

try:
    from fundamentals.mysql import writequery
    sqlQuery = """drop table IF EXISTS tcs_cat_ned_stream;""" % locals()
    writequery(
        log=log,
        sqlQuery=sqlQuery,
        dbConn=dbConn
    )
except:
    pass


class test_ned(unittest.TestCase):

    def test_ned_metadata_function(self):
        coordinateList = []
        from sherlock.imports import ned
        catalogue = ned(
            log=log,
            settings=settings,
            coordinateList=coordinateList,
            radiusArcsec=300
        )
        catalogue._download_ned_source_metadata()

    # def test_ned_function(self):
    #     coordinateList = ["23.2323 -43.23434"]
    #     from sherlock.imports import ned
    #     catalogue = ned(
    #         log=log,
    #         settings=settings,
    #         coordinateList=coordinateList,
    #         radiusArcsec=300
    #     )
    #     catalogue.ingest()

    def test_ned_function_exception(self):

        from sherlock.imports import ned
        try:
            this = ned(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function

#!/usr/local/bin/python
# encoding: utf-8
"""
*Clean up the database tables used by sherlock - maintainance tools*

:Author:
    David Young

:Date Created:
    November 18, 2016
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle
from fundamentals import tools, times
from docopt import docopt
from fundamentals.mysql import readquery, writequery


class database_cleaner():
    """*Clean and maintain the database helper tables used by sherlock*

    The helper tables list row counts for tables and views and provide the column maps that help sherlock know which catalogue columns relate to which parameters (e.g. RA, DEC etc)

    **Key Arguments:**
        - ``dbConn`` -- mysql database connection
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary

     **Usage:**

        .. todo::

            - add an entry in the tutorial to clean database tables

        .. code-block:: python 

            from sherlock.database_cleaner import database_cleaner
            db = database_cleaner(
                log=log,
                settings=settings
            )
            db.clean()

    .. todo ::

        - update key arguments values and definitions with defaults
        - update return values and definitions
        - update usage examples and text
        - update docstring text
        - check sublime snippet exists
        - clip any useful text to docs mindmap
        - regenerate the docs and check redendering of this docstring
    """
    # Initialisation

    def __init__(
            self,
            log,
            settings=False,

    ):
        self.log = log
        log.debug("instansiating a new 'database_cleaner' object")
        self.settings = settings
        # xt-self-arg-tmpx

        # INITIAL ACTIONS# Initial Actions
        # SETUP ALL DATABASE CONNECTIONS
        from sherlock import database
        db = database(
            log=self.log,
            settings=self.settings
        )
        dbConns, dbVersions = db.connect()
        self.transientsDbConn = dbConns["transients"]
        self.cataloguesDbConn = dbConns["catalogues"]
        self.pmDbConn = dbConns["marshall"]

        return None

    def clean(self):
        """*clean up and run some maintance tasks on the crossmatch catalogue helper tables*

        .. todo ::

            - update key arguments values and definitions with defaults
            - update return values and definitions
            - update usage examples and text
            - update docstring text
            - check sublime snippet exists
            - clip any useful text to docs mindmap
            - regenerate the docs and check redendering of this docstring
        """
        self.log.debug('starting the ``get`` method')

        self._update_tcs_helper_catalogue_tables_info_with_new_tables()
        self._updated_row_counts_in_tcs_helper_catalogue_tables_info()
        self._clean_up_columns()
        self._update_tcs_helper_catalogue_views_info_with_new_views()
        self._clean_up_columns()
        self._updated_row_counts_in_tcs_helper_catalogue_tables_info()

        print "`tcs_helper_catalogue_tables_info` & `tcs_helper_catalogue_views_info` database tables updated"

        self.log.debug('completed the ``get`` method')
        return None

    def _updated_row_counts_in_tcs_helper_catalogue_tables_info(
            self):
        """ updated row counts in tcs catalogue tables

        .. todo ::

            - update key arguments values and definitions with defaults
            - update return values and definitions
            - update usage examples and text
            - update docstring text
            - check sublime snippet exists
            - clip any useful text to docs mindmap
            - regenerate the docs and check redendering of this docstring
        """
        self.log.debug(
            'starting the ``_updated_row_counts_in_tcs_helper_catalogue_tables_info`` method')

        sqlQuery = u"""
            select * from tcs_helper_catalogue_tables_info where table_name like "%%stream" or (number_of_rows is null and legacy_table = 0)
        """ % locals()
        rows = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )

        for row in rows:
            tbName = row["table_name"]

            sqlQuery = u"""
                update tcs_helper_catalogue_tables_info set number_of_rows = (select count(*) as count from %(tbName)s) where table_name = "%(tbName)s"
            """ % locals()
            writequery(
                log=self.log,
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
            )

        sqlQuery = u"""
            select * from tcs_helper_catalogue_views_info where (number_of_rows is null and legacy_view = 0)
        """ % locals()
        rows = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )

        for row in rows:
            tbName = row["view_name"]
            print tbName

            sqlQuery = u"""
                update tcs_helper_catalogue_views_info set number_of_rows = (select count(*) as count from %(tbName)s) where view_name = "%(tbName)s"
            """ % locals()
            writequery(
                log=self.log,
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
            )

        self.log.debug(
            'completed the ``_updated_row_counts_in_tcs_helper_catalogue_tables_info`` method')
        return None

    def _update_tcs_helper_catalogue_tables_info_with_new_tables(
            self):
        """update tcs helper catalogue tables info with new tables

        .. todo ::

            - update key arguments values and definitions with defaults
            - update return values and definitions
            - update usage examples and text
            - update docstring text
            - check sublime snippet exists
            - clip any useful text to docs mindmap
            - regenerate the docs and check redendering of this docstring
        """
        self.log.debug(
            'starting the ``_update_tcs_helper_catalogue_tables_info_with_new_tables`` method')

        sqlQuery = u"""
            SELECT max(id) as thisId FROM tcs_helper_catalogue_tables_info;
        """ % locals()
        thisId = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )
        try:
            highestId = thisId[0]["thisId"] + 1
        except:
            highestId = 1

        sqlQuery = u"""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA like '%%catalogues%%' and TABLE_NAME like "tcs_cat%%";
        """ % locals()
        tablesInDatabase = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )

        sqlQuery = u"""
            SELECT table_name, old_table_name FROM tcs_helper_catalogue_tables_info;
        """ % locals()
        tableList = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )
        tbList = []
        oldList = []
        for tb in tableList:
            oldList.append(tb["old_table_name"])

        for tb in tableList:
            if tb["old_table_name"] not in tbList:
                tbList.append(tb["old_table_name"])
            if tb["table_name"] not in tbList:
                tbList.append(tb["table_name"])

        for tb in tablesInDatabase:
            if tb["TABLE_NAME"] not in tbList:
                thisTableName = tb["TABLE_NAME"]
                print "`%(thisTableName)s` added to `tcs_helper_catalogue_tables_info` database table" % locals()
                sqlQuery = u"""
                    INSERT INTO tcs_helper_catalogue_tables_info (
                            id,
                            table_name
                        )
                        VALUES (
                            %(highestId)s,
                            "%(thisTableName)s"
                    )""" % locals()
                writequery(
                    log=self.log,
                    sqlQuery=sqlQuery,
                    dbConn=self.cataloguesDbConn,
                )
                highestId += 1

        self.log.debug(
            'completed the ``_update_tcs_helper_catalogue_tables_info_with_new_tables`` method')
        return None

    def _clean_up_columns(
            self):
        """clean up columns

        .. todo ::

            - update key arguments values and definitions with defaults
            - update return values and definitions
            - update usage examples and text
            - update docstring text
            - check sublime snippet exists
            - clip any useful text to docs mindmap
            - regenerate the docs and check redendering of this docstring
        """
        self.log.debug('starting the ``_clean_up_columns`` method')

        sqlQueries = [
            "update tcs_helper_catalogue_tables_info set old_table_name = table_name where old_table_name is null;",
            "update tcs_helper_catalogue_tables_info set version_number = 'stream' where table_name like '%%stream' and version_number is null;",
            """update tcs_helper_catalogue_tables_info set in_ned = 0 where table_name like '%%stream' and in_ned is null;""",
            """update tcs_helper_catalogue_tables_info set vizier_link = 0 where table_name like '%%stream' and vizier_link is null;""",
            "update tcs_helper_catalogue_views_info set old_view_name = view_name where old_view_name is null;",
        ]

        for sqlQuery in sqlQueries:
            writequery(
                log=self.log,
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
            )

        # VIEW OBJECT TYPES
        sqlQuery = u"""
            SELECT view_name FROM tcs_helper_catalogue_views_info where legacy_view = 0 and object_type is null;
        """ % locals()
        rows = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )

        for row in rows:
            view_name = row["view_name"]
            object_type = view_name.replace("tcs_view_", "").split("_")[0]

            sqlQuery = u"""
                update tcs_helper_catalogue_views_info set object_type = "%(object_type)s" where view_name = "%(view_name)s"
            """ % locals()
            writequery(
                log=self.log,
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
            )

        # MASTER TABLE ID FOR VIEWS
        sqlQuery = u"""
            SELECT view_name FROM tcs_helper_catalogue_views_info where legacy_view = 0 and table_id is null;
        """ % locals()
        rows = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )

        for row in rows:
            view_name = row["view_name"]
            table_name = view_name.replace("tcs_view_", "").split("_")[1:]
            table_name = ("_").join(table_name)
            table_name = "tcs_cat_%(table_name)s" % locals()

            sqlQuery = u"""
                update tcs_helper_catalogue_views_info set table_id = (select id from tcs_helper_catalogue_tables_info where table_name = "%(table_name)s") where view_name = "%(view_name)s"
            """ % locals()
            writequery(
                log=self.log,
                sqlQuery=sqlQuery,
                dbConn=self.cataloguesDbConn,
            )

        self.log.debug('completed the ``_clean_up_columns`` method')
        return None

    def _update_tcs_helper_catalogue_views_info_with_new_views(
            self):
        """ update tcs helper catalogue tables info with new tables

        .. todo ::

            - update key arguments values and definitions with defaults
            - update return values and definitions
            - update usage examples and text
            - update docstring text
            - check sublime snippet exists
            - clip any useful text to docs mindmap
            - regenerate the docs and check redendering of this docstring
        """
        self.log.debug(
            'starting the ``_update_tcs_helper_catalogue_views_info_with_new_views`` method')

        sqlQuery = u"""
            SELECT max(id) as thisId FROM tcs_helper_catalogue_views_info;
        """ % locals()
        thisId = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )
        try:
            highestId = thisId[0]["thisId"] + 1
        except:
            highestId = 1

        sqlQuery = u"""
            SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='VIEW' AND TABLE_SCHEMA like '%%catalogues%%' and TABLE_NAME like "tcs_view%%" and TABLE_NAME not like "%%helper%%";
        """ % locals()
        tablesInDatabase = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )

        sqlQuery = u"""
            SELECT view_name FROM tcs_helper_catalogue_views_info;
        """ % locals()
        tableList = readquery(
            log=self.log,
            sqlQuery=sqlQuery,
            dbConn=self.cataloguesDbConn,
            quiet=False
        )
        tbList = []
        for tb in tableList:
            tbList.append(tb["view_name"])

        for tb in tablesInDatabase:
            if tb["TABLE_NAME"] not in tbList:
                thisViewName = tb["TABLE_NAME"]
                print "`%(thisViewName)s` added to `tcs_helper_catalogue_views_info` database table" % locals()
                sqlQuery = u"""
                    INSERT INTO tcs_helper_catalogue_views_info (
                            id,
                            view_name
                        )
                        VALUES (
                            %(highestId)s,
                            "%(thisViewName)s"
                    )""" % locals()
                writequery(
                    log=self.log,
                    sqlQuery=sqlQuery,
                    dbConn=self.cataloguesDbConn,
                )
                highestId += 1

        self.log.debug(
            'completed the ``_update_tcs_helper_catalogue_views_info_with_new_views`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

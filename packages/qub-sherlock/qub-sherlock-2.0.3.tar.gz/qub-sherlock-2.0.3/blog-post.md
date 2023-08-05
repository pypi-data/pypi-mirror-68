sherlock
========

[![Documentation Status](https://readthedocs.org/projects/qub-sherlock/badge/)](http://qub-sherlock.readthedocs.io/en/latest/?badge)

[![Coverage Status](https://cdn.jsdelivr.net/gh/thespacedoctor/sherlock@master/coverage.svg)](https://cdn.jsdelivr.net/gh/thespacedoctor/sherlock@master/htmlcov/index.html)

*A python package with command-line tools for contextually classifying variable/transient astronomical sources. Sherlock mines a library of historical and on-going astronomical survey data in an attempt to identify sources transient/variable events, and predict their classifications based on the associated crossmatched data*.

Command-Line Usage
==================

``` bash
# SHERLOCK #
: INFERING TRANSIENT-SOURCE CLASSIFICATIONS FROM SPATIALLY CROSS-MATCHED CATALOGUED SOURCES :
=============================================================================================

Documentation for sherlock can be found here: http://qub-sherlock.readthedocs.org/en/stable

.. todo ::

    - docuument cl_utils module
    - tidy usage text

Usage:
    sherlock init
    sherlock info [-s <pathToSettingsFile>]
    sherlock [-NA] dbmatch [--update] [-s <pathToSettingsFile>]
    sherlock [-bN] match -- <ra> <dec> [<pathToSettingsFile>] 
    sherlock clean [-s <pathToSettingsFile>]
    sherlock wiki [-s <pathToSettingsFile>]
    sherlock import ned <ra> <dec> <radiusArcsec> [-s <pathToSettingsFile>]
    sherlock import cat <cat_name> <pathToDataFile> <cat_version> [-s <pathToSettingsFile>]
    sherlock import stream <stream_name> [-s <pathToSettingsFile>]

Options:
    init                    setup the sherlock settings file for the first time
    match                   XXXX
    dbmatch                 database match
    clean                   XXXX
    wiki                    XXXX
    import                  XXXX
    ned                     use the online NED database as the source catalogue
    cat                     import a static catalogue into the sherlock-catalogues database
    stream                  download/stream new data from a give source catalogue into the sherlock sherlock-catalogues database
    info                    print an overview of the current catalogues, views and streams in the sherlock database ready for crossmatching

    ra                      the right-ascension coordinate with which to perform a conesearch (sexegesimal or decimal degrees)
    dec                     the declination coordinate with which to perform a conesearch (sexegesimal or decimal degrees)
    radiusArcsec            radius in arcsec of the footprint to download from the online NED database
    cat_name                name of the catalogue being imported (veron|ned_d)                          
    stream_name             name of the stream to import into the sherlock-catalogues database (ifs)

    -N, --skipNedUpdate     do not update the NED database before classification
    -A, --skipMagUpdate     do not update the peak magnitudes and human readable text annotations of objects (can eat up some time)
    -h, --help              show this help message
    -s, --settings          the settings file
    -b, --verbose           print more details to stdout
    -l, --transientlistId   the id of the transient list to classify
    -u, --update            update the transient database with new classifications and crossmatches
    -v, --version           print the version of sherlock
```

Installation
============

Although you can get Sherlock from a simple `pip` install, it\'s best to install it within a Conda environment under Anaconda. If you\'re not familiar with Anaconda, you\'ll find a [good tutorial here](http://astronotes.co.uk/blog/2017/10/04/An-Astronomer's-Guide-to-dotstar-Conda.html) to get you up and running.

Once you have Anaconda installed, go ahead and create a new Conda environment to host Sherlock:

``` bash
conda create -n sherlock python=2.7 pip numpy
```

Now activate the environment and install sherlock:

``` bash
source activate sherlock
pip install qub-sherlock
```

At any point in the future you can upgrade to the latest version of sherlock with the command:

``` bash
pip install qub-sherlock --upgrade
```

If instead you want to clone the [github repo](https://github.com/thespacedoctor/sherlock) and install from a local version of the code:

``` bash
git clone git@github.com:thespacedoctor/sherlock.git
cd sherlock
source activate sherlock
python setup.py install
```

Documentation
=============

Documentation for sherlock is hosted by [Read the Docs](http://qub-sherlock.readthedocs.org/en/stable/) (last [stable version](http://qub-sherlock.readthedocs.org/en/stable/) and [latest version](http://qub-sherlock.readthedocs.org/en/latest/)).

Sherlock Tutorial
=================

Before you begin using sherlock you will need to populate some custom parameters within the sherlock settings file.

To setup the default settings file at `~/.config/sherlock/sherlock.yaml` run the command:

``` bash
sherlock init
```

This should create and open a new config file; follow the instructions in the file to populate the missing parameters values (usually given an `XXX` placeholder).

<div class="todo" markdown="1">

-   add tutorial

</div>

Initialisation and Setup
------------------------

### Populating Sherlock\'s Settings File

The settings file now contains every option required to change the way the code runs, including database settings and the actual search algorithm.

#### Database Settings

``` yaml
database settings:
    static catalogues:
        db: crossmatch_catalogues
        host: 127.0.0.1
        user: pessto
        password: p355t0

    transients:
        user: pessto
        password: p355t0
        db: ps13pipublic
        host: 127.0.0.1
        transient table: tcs_transient_objects
        transient query: "select id as 'id', followup_id as 'alt_id', ra_psf 'ra', dec_psf 'dec', local_designation 'name', object_classification as 'object_classification'
            from tcs_transient_objects
            where detection_list_id = 2
            and object_classification is null
            order by followup_id"
        transient id column: id
        transient classification column: object_classification

    pessto marshall:
        user: pessto
        password: p355t0
        db: pessto_marshall
        host: 127.0.0.1
```

The <span class="title-ref">static catalogues</span> settings are the settings for connecting to the static catalogues database. Do not edit these settings unless you know what you\'re doing. If you have your RSA key on starbase, the code will setup a ssh-tunnel for you so that you can connect to this database remotely.

The <span class="title-ref">transients</span> settings are for the database you have your transients stored in. <span class="title-ref">transient table</span> is the name of the table containing your transients, <span class="title-ref">transient query</span> is the SQL query that need executed to get the following info for the transients needing classified:

-   <span class="title-ref">id</span> - the primary ID for the transient in the database
-   <span class="title-ref">alt\_id</span> - human readable name (optional)
-   <span class="title-ref">ra</span> - the ra of the object
-   <span class="title-ref">dec</span> - the dec of the object
-   <span class="title-ref">name</span> - a further alt id (optional)

The <span class="title-ref">transient id column</span> is the primary ID column in the transient database and <span class="title-ref">transient classification column</span> is the column you wish to add the classification to.

#### The Search Algorithm

The order searches appear in the <span class="title-ref">search algorithm</span> section is the order they shall be run in the actual code:

``` yaml
search algorithm:
    sdss qso:
        angular radius arcsec: 2.0
        transient classification: AGN
        database table: tcs_cat_v_sdss_dr9_spect_qsos
    milliquas:
        angular radius arcsec: 3.0
        transient classification: AGN
        database table: tcs_cat_milliquas
    veron:
        angular radius arcsec: 2.0
        transient classification: AGN
        database table: tcs_veron_cat
    ned qso:
        angular radius arcsec: 2.0
        transient classification: AGN
        database table: tcs_cat_v_ned_qsos
    ned nt:
        angular radius arcsec: 3.0
        physical radius kpc: 0.5
        transient classification: NT
        database table: tcs_cat_v_ned_galaxies
    sdss spec nt:
        angular radius arcsec: 3.0
        physical radius kpc: 0.5
        transient classification: NT
        database table: tcs_cat_v_sdss_dr9_spect_galaxies
    sdss phot nt: 
        angular radius arcsec: 0.5
        transient classification: NT
        database table: tcs_cat_v_sdss_dr9_galaxies_notspec
    ...
```

The first time you run <span class="title-ref">sherlock</span> you will be told to add your settings to the empty settings file that\'s been created in <span class="title-ref">\~/.config/sherlock/sherlock.yaml</span>.

For details about all of the catalogue in the catalogues database, run:

``` bash
sherlock info 
```

Classifying Transients
----------------------

### A Single Transient Classification

### Classifying Transients in a Transient Database

### The Classification Workflow

![](https://camo.githubusercontent.com/dd84c3c74b99d24d1343a9ab29ca289ee2f16c9f/68747470733a2f2f692e696d6775722e636f6d2f546147693970622e706e67)

#### Synonyms vs Associations

Sherlock distinguishes between what it views as transient objects
synonymous with a catalogued source (the same as or very closely linked
to), *synonyms*, and those it deems as merely associated with the
catalogued source, *associations*.

Examples of transient-synonym matches are CVs, AGN and variable stars
(VS) that match within 1-2 arcsec of their catalogue counterpart.
Stretching the definition of *synonym* a little, Sherlock will also
match transients close to the centre of galaxies as synonyms[^1].
Transient-associations include those transients that are located near,
but not on top of, a catalogued source. Example of these associations
are \'transients\' matching close to bright-stars and are classified as
bright-star artefacts (BS) resulting from poor image subtractions near
bright stars ($~>14-16^{th}$ mag) or transients matched near to a galaxy
which may be classified as supernovae (SN). By definition synonyms are a
more secure match than associations.

Each search algorithm module should contain a *synonym* and an
*association* key-value sets. For example here is a Guide-Star Catalogue
search module:

``` yaml
gsc bright stars:
 angular radius arcsec: 100.0
 synonym: VS
 association: BS
 database table: tcs_view_star_guide_star_catalogue_v2_3
 bright mag column: B
 bright limit: 16. 
```

If a transient is matched on top of a source in the GSC it\'s identified as a synonym and classified as a variable star, but if it is match near to the source but not co-located if may been identified as an association and classified as a potential bright-star artefact (BS).

There\'s also a top-level `synonym radius arcsec` parameter in the
Sherlock settings file that defines the maximum transient-catalogue
source separation that secures a synonym identification.

``` yaml
synonym radius arcsec: 0.5
```

Sherlock performs a two-staged catalogue match, first looking for
synonym matches and then for associations. For an individual transient
if a synonym match is found within the first search stage the second
search stage for associations is skipped as it becomes irrelevant. For
example consider the image below (transients marked in red):

figure:: <https://farm3.staticflickr.com/2772/33007793206_6dd3e34a21_o.jpg%20title=%22Sherlock%20synonyms%20and%20associations%22%20width=600px>

The first stage search should match transients A, C and E as synonyms
(NT, VS, VS), these transients are then removed from a further
association search. The second stage search then flags B as associated
with the large galaxy at the centre of the image and transient D as
either associated with the bright-star in the bottom right corner of the
image or with the galaxy in the centre.

#### NED Stream Updater

The settings in the settings file relating to the NED stream are:

``` yaml
ned stream search radius arcec: 300
first pass ned search radius arcec: 240
ned stream refresh rate in days: 90
```

To update the NED stream, for each transient coordinates the code does a conesearch on the <span class="title-ref">tcs\_helper\_ned\_query\_history</span> table to see if a search has already been performed within the designated <span class="title-ref">ned stream refresh rate in days</span>. If a match isn\'t found then NED is queried and the <span class="title-ref">tcs\_helper\_ned\_query\_history</span> is updated for the transient coordinates.

#### Search Algoritm

The algorithm is written and modified within the <span class="title-ref">sherlock.yaml</span> settings file. This means you can modify the algorithm without affecting anyone else\'s search (as long as you are working off the different transient databases).

``` yaml
search algorithm:
    sdss qso:
        angular radius arcsec: 2.0
        transient classification: AGN
        database table: tcs_view_qso_sdss_spect_galaxies_qsos_dr12
        stop algorithm on match: False
        match nearest source only: False
    milliquas:
        angular radius arcsec: 3.0
        transient classification: AGN
        database table: tcs_view_agn_milliquas_v4_5
        stop algorithm on match: False
        match nearest source only: False
    veron:
        angular radius arcsec: 2.0
        transient classification: AGN
        database table: tcs_view_agn_veron_v13
        stop algorithm on match: False
        match nearest source only: False
    ned qso:
        angular radius arcsec: 2.0
        transient classification: AGN
        ...
```

Note, to remove a module temporarily, simply comment it out in the settings file (yaml treats lines beginning with <span class="title-ref">\#</span> as comments).

Behind the scenes there are 2 types of searches performed on the catalogues.

1.  Angular Separation Search
2.  Physical Separation Search

#### Angular Separation Search

An example of an angular separation search looks like this in the settings file:

``` yaml
milliquas:
    angular radius arcsec: 2.0
    transient classification: AGN
    database table: tcs_view_agn_milliquas_v4_5
    stop algorithm on match: False
    match nearest source only: False
```

The code performs a cone-search on <span class="title-ref">database table</span> using the <span class="title-ref">angular radius arcsec</span>. If matches are found the associated transient is given a <span class="title-ref">transient classification</span> and the results are added to the <span class="title-ref">tcs\_cross\_matches</span> table of the transients database. If <span class="title-ref">stop algorithm on match</span> is true the code breaks out of the search algorithm and starts afresh with the next transient to be classified, otherwise the algorithm contines and all matches are recorded in the <span class="title-ref">tcs\_cross\_matches</span> table. If <span class="title-ref">match nearest source only</span> is true only the closest match from each catalogue query is be recorded in the <span class="title-ref">tcs\_cross\_matches</span> table.

#### Physical Separation Search

If the <span class="title-ref">physical radius kpc</span> key is found in the conesearch module then a physical separation search is performed. First of all an angular cone-search is performed at the coordinates using a suitably large search radius. After this a further search is done on the physical distance parameters returned (distance, physical separation distance, semi-major axis length \...) for each match.

A physical match is found if:

-   The transient falls within 1.5 x semi-major axis of a galaxy
-   The transient is within the <span class="title-ref">physical radius kpc</span> of a galaxy

As before, all matches are recorded in the <span class="title-ref">tcs\_cross\_matches</span> table.

#### Classification Rankings

If transients are found:

-   within 2.0 arc of source, **OR**
-   within 20 kpc of host galaxy **AND** assigned a SN classification, **OR**
-   within 1.2 times the semi-major axis of the host **AND** assigned a SN classification

they are all given the same top level ranking for classification. After this catalogue weights come into effect to determine the orders of classifications. The catalogue weights are found in the \[<span class="title-ref">tcs\_helper\_catalogue\_tables\_info</span>\](Crossmatch Catalogue Tables) table of the catalogues database and give an indication of the accuracy of the classifications of sources in the catalogue. For example the <span class="title-ref">tcs\_cat\_sdss\_spect\_galaxies\_qsos\_dr12</span> is given a greater weight than <span class="title-ref">tcs\_cat\_sdss\_photo\_stars\_galaxies\_dr12</span> as classifications of the objects based on spectral observations is more accurate than photometry alone.

Once the classifications for each individual transient are ranked, a final, ordered classification listing is given to the transient within its original database table. For example <span class="title-ref">SN/VARIABLE STAR</span> means the the transient is most likely a SN but may also be a variable star.

A transient is matched against a source in the sherlock-catalogues because it is either synonymous with a point-like catalogue source (e.g. a variable star or an AGN) or it is hosted by the catalogue source (e.g. supernova, nuclear transient).

A synonymous crossmatch is always a simple angular crossmatch with a search radius that reflects the astrometric accuracy of the RMS combined astrometric errors of the transient source location and that of the catalogue being matched against.

Sherlock\'s Catalogue Database
------------------------------

### Database Table Naming Scheme

There\'s a \[strict table naming syntax for the crossmatch-catalogues\](Crossmatch-Catalogues Database Scheme) database to help deal with catalogue versioning (as updated versions of out sherlock-catalogues are released) and to help ease the burden of modifying crossmatch algorithms employed.

\[See here for an up-to-date list of the crossmatch-catalogues\](Crossmatch Catalogue Tables) and the \[views\](Crossmatch Catalogue Views) found on those tables.

#### Table Classes

There are 4 classes of tables in the <span class="title-ref">crossmatch\_catalogues</span> database:

Table Type \| Prefix \| Notes \| Example \|  
:\-\-\-\-\-\-\-\-\-\-\-- \| :\-\-\-\-\-\-\-\-\-\-- \| :\-\-\-\-\-\-\-\-\-\-- \| :\-\-\-\-\-\-\-\-\-\-- \|  
Catalogue \| <span class="title-ref">tcs\_cat</span> \| The table is named with the scheme <span class="title-ref">tcs\_cat\_</span> \<catalogue name\> \<version\> \| <span class="title-ref">tcs\_cat\_ned\_d\_v10\_2\_0</span> \|  
View \| <span class="title-ref">tcs\_view</span> \| The view is named with the scheme <span class="title-ref">tcs\_view\_</span> \<object type contained\> \<source table name\> \| <span class="title-ref">tcs\_view\_galaxies\_ned\_d</span> \|  
Helper \| <span class="title-ref">tcs\_helper</span> \| Mostly used to store relational information, notes on database tables and book-keeper info \| <span class="title-ref">tcs\_helper\_catalogue\_tables\_info</span> \|  
Legacy \| <span class="title-ref">legacy\_tcs\_</span> \| Legacy tables used in previous incarnations of the transient classifier \| <span class="title-ref">legacy\_tcs\_cat\_md01\_chiappetti2005</span> \|

#### Versioning

Each catalogue is versioned by appending a version indicator to the end of the table name. There are 3 indicator types:

1.  <span class="title-ref">\_final</span> to show that the catalogue is now at it\'s final version and shall remain unchanged.
2.  <span class="title-ref">\_stream</span> to show that the catalogue is constantly being updated
3.  <span class="title-ref">\_vX\_X</span> to show a version number for the catalogue, e.g. for v10.2 this would be <span class="title-ref">\_v10\_2</span>. We can also have data-release versions (e.g. <span class="title-ref">\_dr12</span>).

### Maintainance and Updates of Catalogues Database

<div class="todo" markdown="1">

-   write about marshall stream updates
-   write about helper table updates
-   write that some tasks need automated

</div>

There are various cron-scripts that run on PESSTO-VM03 to automate some tasks. These tasks include

-   updating of data-streams into the crossmatch-catalogues database and
-   the updates of certain helper tables in the crossmatch-catalogues database.

Currently there are scripts running every:

-   5 mins
-   30 mins
-   1 hr
-   3 hrs
-   12 hrs
-   24 hrs

### Updating Catalogues and Adding New Catalogues to the Database

<div class="todo" markdown="1">

-   list current catalogue importers and how to use them
-   add tutorial about creating a new importer
-   add steps for adding a catalogue to the database and the search algorithm
-   add details about updating the column map
-   write code into conf.py to generate tables for docs and link them from here (views, tables and streams)

</div>

Using the <span class="title-ref">sherlock-import</span> command it\'s possible to **import and update various catalogues and data-streams** including Milliquas, Veron AGN and the NED-D catalogues. \[See here for details\](Catalogue Importers).

``` bash
sherlock-importers cat <cat_name> <pathToDataFile> <cat_version> [-s <pathToSettingsFile>]
sherlock-importers stream <stream_name> [-s <pathToSettingsFile>]
```

The command to **import new versions of catalogues** and **data streams** into the <span class="title-ref">crossmatch\_catalogues</span> database is:

``` python
Usage:
    sherlock-importers cat <cat_name> <pathToDataFile> <cat_version> [-s <pathToSettingsFile>]
    sherlock-importers stream <stream_name> [-s <pathToSettingsFile>]
```

For example:

``` bash
> sherlock-importers cat milliquas ~/Desktop/milliquas.txt 4.5
1153111 / 1153111 milliquas data added to memory
1153111 / 1153111 rows inserted into tcs_cat_milliquas_v4_5
5694 / 5694 htmIds added to tcs_cat_milliquas_v4_5
```

The command currently supports imports for the following **catalogues**:

-   Milliquas
-   Veron AGN
-   NED-D

Using the command:

``` bash
sherlock-importers stream pessto
```

will import all of the various **data-streams** added to the PESSTO marshall (ASASSN, CRTS, LSQ, PSST \...).

THE COLUMN MAP LIFTED FROM <span class="title-ref">tcs\_helper\_catalogue\_tables\_info</span> TABLE IN CATALOGUE DATABASE (COLUMN NAMES ENDDING WITH \'ColName\')

[^1]: could be classified as a nuclear transient or supernova depending on
    search algorithm parameters

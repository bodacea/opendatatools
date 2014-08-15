Oliver platforms hold links to potentially useful datastores; they can also hold data, where needed for resilience or because it's analysts' working data.  The data storage mechanisms haven't been worked out yet - this table is for managing the links to datastores.

## Table features

* uid
* name
* original source information
  * generating agency
  * data format (csv, mysql dump, json, access, excel, xml etc)
  * date of acquisition from data provider
* contributor info
  * contributor uid
* access priviledges
  * data affiliation (we may want to manage some data access by affiliation)
  * who is allowed to view
  * who is allowed to edit
  * who is allowed to change/ revoke access priviledges
* data quality (has data been cleaned etc)
* data standards used
* link to metadata (if it exists)
* api address (if it exists)

## Cool things about datastores

* The dataset links should include links to scraper pages, so users can access and use data that's been output in difficult to access formats (pdf etc).

## Possible extensions

* Datasets need to be tagged, to allow users to search for data relevant to their task. It's possible to build ontologies of these tags (and linking information).  If these tags become dominant in the tables, it's worth considering a nosql database (like couchdb) instead of a structured one.

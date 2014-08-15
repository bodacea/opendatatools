Every Oliver platform has links to other Oliver platforms and sites (even if it's only the master site in New York that the maintenance guy downloads updates from). This table supports that site directory (the "yellow pages" of sites, if you will).  We may or may not need to split out the aorta platforms list from the remote sites list - we'll see. 

## Table features

* uid
* name
* description - free-text description of this site.
* affiliation (we may want to manage some data access by affiliation)
* primary purpose (some sites will be specialised for data or processing; other sites will be general).
* low-bandwidth (Some sites will be in places where Internet access is intermittent and bandwidth limited. We want to reduce the amount of junk that gets sent to these).
* Lat/long (this may be difficult to determine, but would give an indication of where a functioning site might be found during a crisis. 'Cloud' should also be an option here).
* verified (because we need to be aware of and counter for site spoofing).
* url (because we need to know where the platform is)

## Cool things about sites

* Users can find sites like their own. 
* There isn't just one type of site - sites can specialise in things like data warehousing or processing.  
* All sites will be designed so that if the local Internet fails (e.g. during a disaster), the sites will still be able to function.

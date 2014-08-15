Most of these notes are products of painful learning experiences. Please add your own to them!

To start, you'll need:

* A copy of the rails/Oliver code from this repository
* [[Mongodb|http://www.mongodb.org/]]
* Ruby
* Rails

When you start up a local version, don't forget to type "mongod" before "rails s", or you'll get a database error. 

Mongo can be a bit of a pain on a mac. If you see this error "exception in initAndListen std::exception: dbpath (/data/db/) does not exist, terminating" when you type "mongod" in your terminal window, it's probably because you don't have a directory called /data/db. Try this:

* mkdir /data
* mkdir /data/db
* sudo chown 'id -u' /data/db

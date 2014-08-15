Oliver is built in Ruby on Rails, to manage a toolkit that has a lot of python modules in it. This may seem like a strange choice ("why not just run stuff directly from the framework?), but the needs on the framework are different to the needs on the toolkit. Also, many of the existing tools aren't in Python, and there are some excellent ways to call Python from Ruby without losing too much hair. 

The Oliver database is Mongo, chosen because we're integrating datastore and tool information that's come from multiple sources and isn't likely to contain the same metainformation.  It also allows us to mess around with the tables without all the pain involved in rebuilding sql databases. 

The Oliver prototype has several good things in it, which are shamelessly nicked. Amongst these are:

* Using Mongo
* [[Devise|https://github.com/plataformatec/devise]] - for user security

Other useful stuff:

* Github - obviously
* [[Pencil|http://pencil.evolus.vn/en-US/Downloads/Application.aspx]] - a freeware tool for wireframing
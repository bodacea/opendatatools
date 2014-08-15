Oliver is being designed to work in a specific set of environments.  

##Domain Objects

A domain object is something outside a system that the system interacts with. Domain objects could include system users and other systems. For Oliver, these are:

* Users – people with the right to access information held on this specific platform

  * Analyst
  * Developer
  * Platform manager
  * Network manager
  * Data owner
  * Tool owner

* Data sources – information about specific topics or areas

  * Remote datastores – data held at sites outside the platform system. Some datastores will be private, and will be accessible only to queries made from the UN parts of the system.
  * Local datastores - data held either within or connected to the platform
  * Remote datastreams
  * Local datastreams

* Tools – applications for accessing manipulating and making sense of data

  * Remote tools
  * Local tools

* Systems

  * other Oliver platforms
  * processor farms – large-scale computing sites (e.g. EU Grid)

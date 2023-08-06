======
 News
======


1.1.7 - Sixth Law of Nature
===========================

* Fix error in ``--export-storage``
* Include documentation in source archive


1.1.6 - Sixth Law of Nature
===========================

* Improve logging for ``--export-storage``


1.1.5 - Sixth Law of Nature
===========================

* Improve logging for ``--export-storage``


1.1.4 - Fifth Law of Nature
===========================

* Use ``shutil.move`` for ``--export-storage``


1.1.3 - Fourth Law of Nature
============================

* Add a ``--export-storage=FOLDER`` command-line argument (by Unrud, see #606)


1.1.2 - Third Law of Nature
===========================

* **Security fix**: Add a random timer to avoid timing oracles and simple
  bruteforce attacks when using the htpasswd authentication method
* Various minor fixes


1.1.1 - Second Law of Nature
============================

* Fix the owner_write rights rule


1.1 - Law of Nature
===================

One feature in this release is **not backward compatible**:

* Use the first matching section for rights (inspired from daald)

Now, the first section matching the path and current user in your custom rights
file is used. In the previous versions, the most permissive rights of all the
matching sections were applied. This new behaviour gives a simple way to make
specific rules at the top of the file independant from the generic ones.

Many **improvements in this release are related to security**, you should
upgrade Radicale as soon as possible:

* Improve the regex used for well-known URIs (by Unrud)
* Prevent regex injection in rights management (by Unrud)
* Prevent crafted HTTP request from calling arbitrary functions (by Unrud)
* Improve URI sanitation and conversion to filesystem path (by Unrud)
* Decouple the daemon from its parent environment (by Unrud)

Some bugs have been fixed and little enhancements have been added:

* Assign new items to corret key (by Unrud)
* Avoid race condition in PID file creation (by Unrud)
* Improve the docker version (by cdpb)
* Encode message and commiter for git commits
* Test with Python 3.5


1.0.1 - Sunflower Again
=======================

* Update the version because of a **stupid** "feature"™ of PyPI


1.0 - Sunflower
===============

* Enhanced performances (by Mathieu Dupuy)
* Add MD5-APR1 and BCRYPT for htpasswd-based authentication (by Jan-Philip Gehrcke)
* Use PAM service (by Stephen Paul Weber)
* Don't discard PROPPATCH on empty collections (by Markus Unterwaditzer)
* Write the path of the collection in the git message (by Matthew Monaco)
* Tests launched on Travis


0.10 - Lovely Endless Grass
===========================

* Support well-known URLs (by Mathieu Dupuy)
* Fix collection discovery (by Markus Unterwaditzer)
* Reload logger config on SIGHUP (by Élie Bouttier)
* Remove props files when deleting a collection (by Vincent Untz)
* Support salted SHA1 passwords (by Marc Kleine-Budde)
* Don't spam the logs about non-SSL IMAP connections to localhost (by Giel van Schijndel)


0.9 - Rivers
============

* Custom handlers for auth, storage and rights (by Sergey Fursov)
* 1-file-per-event storage (by Jean-Marc Martins)
* Git support for filesystem storages (by Jean-Marc Martins)
* DB storage working with PostgreSQL, MariaDB and SQLite (by Jean-Marc Martins)
* Clean rights manager based on regular expressions (by Sweil)
* Support of contacts for Apple's clients
* Support colors (by Jochen Sprickerhof)
* Decode URLs in XML (by Jean-Marc Martins)
* Fix PAM authentication (by Stepan Henek)
* Use consistent etags (by 9m66p93w)
* Use consistent sorting order (by Daniel Danner)
* Return 401 on unauthorized DELETE requests (by Eduard Braun)
* Move pid file creation in child process (by Mathieu Dupuy)
* Allow requests without base_prefix (by jheidemann)


0.8 - Rainbow
=============

* New authentication and rights management modules (by Matthias Jordan)
* Experimental database storage
* Command-line option for custom configuration file (by Mark Adams)
* Root URL not at the root of a domain (by Clint Adams, Fabrice Bellet, Vincent Untz)
* Improved support for iCal, CalDAVSync, CardDAVSync, CalDavZAP and CardDavMATE
* Empty PROPFIND requests handled (by Christoph Polcin)
* Colon allowed in passwords
* Configurable realm message


0.7.1 - Waterfalls
==================

* Many address books fixes
* New IMAP ACL (by Daniel Aleksandersen)
* PAM ACL fixed (by Daniel Aleksandersen)
* Courier ACL fixed (by Benjamin Frank)
* Always set display name to collections (by Oskari Timperi)
* Various DELETE responses fixed


0.7 - Eternal Sunshine
======================

* Repeating events
* Collection deletion
* Courier and PAM authentication methods
* CardDAV support
* Custom LDAP filters supported


0.6.4 - Tulips
==============

* Fix the installation with Python 3.1


0.6.3 - Red Roses
=================

* MOVE requests fixed
* Faster REPORT answers
* Executable script moved into the package


0.6.2 - Seeds
=============

* iPhone and iPad support fixed
* Backslashes replaced by slashes in PROPFIND answers on Windows
* PyPI archive set as default download URL


0.6.1 - Growing Up
==================

* Example files included in the tarball
* htpasswd support fixed
* Redirection loop bug fixed
* Testing message on GET requests


0.6 - Sapling
=============

* WSGI support
* IPv6 support
* Smart, verbose and configurable logs
* Apple iCal 4 and iPhone support (by Łukasz Langa)
* KDE KOrganizer support
* LDAP auth backend (by Corentin Le Bail)
* Public and private calendars (by René Neumann)
* PID file
* MOVE requests management
* Journal entries support
* Drop Python 2.5 support


0.5 - Historical Artifacts
==========================

* Calendar depth
* MacOS and Windows support
* HEAD requests management
* htpasswd user from calendar path


0.4 - Hot Days Back
===================

* Personal calendars
* Last-Modified HTTP header
* ``no-ssl`` and ``foreground`` options
* Default configuration file


0.3 - Dancing Flowers
=====================

* Evolution support
* Version management


0.2 - Snowflakes
================

* Sunbird pre-1.0 support
* SSL connection
* Htpasswd authentication
* Daemon mode
* User configuration
* Twisted dependency removed
* Python 3 support
* Real URLs for PUT and DELETE
* Concurrent modification reported to users
* Many bugs fixed (by Roger Wenham)


0.1 - Crazy Vegetables
======================

* First release
* Lightning/Sunbird 0.9 compatibility
* Easy installer

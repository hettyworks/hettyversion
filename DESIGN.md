# hettyversion


## Core Features

* A headyversion.com clone with support for arbitrary song lists and multiple bands
* A head-to-head song ranking game (e.g. http://www.allourideas.org/)

## Tech Stack

* Python (what version?)
* Flask

## Schema Design

```
user table is like: ID, username, hashpw, role
song is: ID, name, desc
version is: ID, datestamp_added, datestamp_source, songid, link, added_by
band is: ID, name
head2head: ID, datestamp, versionID1, versionID2, winner, userID
```

## Pages

login, logout, register, resetpw, home page, single song page w/list of versions, single version page, h2h between versions page, master list of songs (edited)
add version, edit version, add song, edit song
add single band page, add band, edit band

## Questions

* How do we handle different versions of songs? can people just add new versions at will?

## Future

* Verification of versions
* Verification of new bands
* Verification of new songs

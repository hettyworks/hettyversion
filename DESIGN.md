# hettyversion


## Core Features

* A headyversion.com clone with support for arbitrary song lists and multiple bands
* A head-to-head version ranking game (e.g. http://www.allourideas.org/)
* Generate ELO & ranking of any given version

## Tech Stack

* Python 3
* Flask
* Docker

## Schema Design

* users: ID, username, hashpw, role
* songs: ID, name, desc, bandid
* versions: ID, title, datestamp, songid, link (optional)
* bands: ID, name, desc
* headtohead: ID, userid, version1id, version2id, winnerid

## Pages

* login, logout, register, resetpw
* home page, list of bands, list of all songs, single band page w/list of their songs, single song page w/list of versions, single version page, h2h between versions page
* add version, edit version, delete version (admin)
* add song (admin), edit song (admin), delete song (admin)
* add band (admin), edit band (admin), delete band (admin)

## Questions

## Future

* Verify/moderate versions

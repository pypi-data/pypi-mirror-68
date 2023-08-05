#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search geonames for given places

you need to set the environment variable GEO_USER like this:

  $ export GEO_USER=[my-geonames-account-username]

or pass the variable username to the search function!
"""

import os
import requests

GEONAMES = "http://api.geonames.org/searchJSON"
GEOPARAMS = {
  "username": "",
  "style": "short",
  "maxRows": 3,
  "countryBias": "DE",
  "q": ""
}


def search(place, username=None):
    """search geoname entity for given place (requires geoname username)"""
    if username is None:
        try:
            username = os.environ["GEO_USER"]
        except KeyError:
            print("")
            print("to do the geonames search either pass")
            print("your geonames username like this:")
            print("search(\""+place+"\", username=USERNAME)\n")
            print("... or set environment variable GEO_USER")
            print("to your geonames username!")
            print("")
            return None
    GEOPARAMS["q"] = place
    GEOPARAMS["username"] = username
    result = requests.get(GEONAMES, params=GEOPARAMS).json()["geonames"][0]
    geoname = result["toponymName"]
    geonameId = "http://www.geonames.org/{0}".format(result["geonameId"])
    return geoname, geonameId

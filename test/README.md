# WoWthon Tests #
## Overview ##
A set of test scripts and unit tests to ensure correct functionality.

## test_all_realm_to_slug_names.py ##
Running this produces a unit test for every realm in every region to ensure
that the static `wowthon.WoWAPI.realm_name_to_slug` method works correctly
and is idempotent.
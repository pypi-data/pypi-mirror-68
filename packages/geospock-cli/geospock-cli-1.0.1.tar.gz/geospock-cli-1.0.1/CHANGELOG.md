# GeoSpock CLI

## Release 1.0.1

#### Bug fixes
 - V3-323 Reporting any error now exits with an exit code other than 0. 
 - V3-321 Modify the cleaning of query responses to accept arbitrary type as input


## Release 1.0.0 
 
#### Features
 - V3-291 `null` values removed from CLI responses when stripNulls specified in CLI template.

#### Bug Fixes
 - V3-237 Will now only save valid credentials, otherwise CLI exits with error message.


## Release 0.1.4

#### Features
 - GS-10984 Can now load schema files from s3
  
#### Bug fixes
 - V3-172 Add non-zero exit code when exception during display_result
 
 
## Release 0.1.3

#### Features
 - GS-10983 Add profile-list command to list initialised profiles
 - GS-10998 Automatically open a web browser with the correct link when running get-credentials

#### Bug fixes
 - GS-10988 Added check that list item is dict when recursively removing nulls
 
 
## Release 0.1.2

#### Bug fixes
- GS-10972 Exit code 1 when args missing from command


## Release 0.1.1

#### Features
 - Improved messaging when we provide an invalid command.


## Release 0.1.0

#### Notes
 - Initial release.
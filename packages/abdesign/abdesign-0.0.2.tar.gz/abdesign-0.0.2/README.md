# ABDesign

## API

The ABDesign API provides functions and data structures for dealing with Immunoglobulin sequences. It contains computational methods to 'humanize' an antibody by CDR-grafting.

> **Note:** A local installation of ANARCI is needed for this tool. You can downlod ANARCI [here.](http://opig.stats.ox.ac.uk/webapps/newsabdab/sabpred/anarci/#download "ANARCI Download")

### IgObject
Core data structure. All params are set on initialization, either by using create_annotation(), or manually.

* seq *required*
* chain_type
* iso_type
* species
* annotation
* regions
* humaness_score
* hits *(upcoming)*

* export_to_json()

### Humanization
To 'humanize' a queried sequence, a human template sequence must be provided in form of an IgObject, too. It is also possible to indicate the wanted annotation types for the hybrid IgObject. By default, all annotation systems provided by this package are applied.

* replace_cdr(ig_query:IgObject, ig_target:IgObject, annotation_types)
# Proposal: Reputation Indicator Hash

## Problem

There is a requirement to build functionallity to query reputation sources by IP, Domain, and Time in the SOW. Building
a table with

## Proposed Solution

Presently, there's no common identifier for the specified Reputation data sources (URLHaus has URL/Domain, FeodoTracker
has IP, SSLBlacklist has SSL hash or IP). IP and Domain are related fields, and a typical data consumer could easily
expect records with a Domain to also have an IP or vice versa.

## Benefits

- **Query simplicity**: Data consumers simply need to provide any available information for a site to receive a
  response, be it an IP, Domain, or SSL certificate.
- **Extensibility**: Ingesting additional data sources with new types of identifiers would require no additional
  consideration for consumers- they can provide whatever identifying information they have and find any matching
  threats.

## Costs

- **Complications with enrichment**: Providing a single indicator column may deter queries on multiple identifiers,
  should records in the reputation dataset be enriched with missing IP, Domain, or SSL Certificate signatures in the
  future- Consider a URLHaus record enriched with an IP address (an identifier for other datasets that is, at the time
  of writing, absent in this source). Querying such a record by a hash of its IP Address would fail, as the indicator
  for URLHaus data would be a hash of the domain. 

### <a id="documentation-body"></a>

![Hackolade image](/QScan%20documentation/image1.png?raw=true)

Cassandra Physical Model
------------------------

#### Schema for:

Model name: QScan

Author:

Version:

Printed On: Fri Oct 30 2020 08:26:33 GMT-0400 (Eastern Daylight Time)

Created with: [Hackolade](https://hackolade.com/) - Visual data modeling for NoSQL and multimodel databases

### <a id="contents"></a>

* [1. Model](#model)
* [2. Keyspaces](#containers)
    * [2.1 qscan](#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2. Tables](#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.1 by_company_name](#cd233050-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.2 by_company_protocol](#cd23f3a2-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.3 by_domain_name](#cd241ab0-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.4 by_ip_port](#cd2441c3-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.5 by_ipaddress](#cd2441cc-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.6 by_port](#cd2468d3-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.7 by_protocol](#cd248fe3-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.8 by_service_name](#cd24b6f2-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.9 company_scores](#cd24b6fb-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.10 domain_company](#cd250513-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.11 domain_scores](#cd25051c-1aaa-11eb-a5a8-91debe8ed8a4)

      [2.1.2.12 scanid_domain](#cd257a43-1aaa-11eb-a5a8-91debe8ed8a4)

### <a id="model"></a>

##### 1\. Model

##### 1.1 Model **QScan**

##### 1.1.1 **QScan** Entity Relationship Diagram

![Hackolade image](/QScan%20documentation/image2.png?raw=true)

##### 1.1.2 **QScan** Properties

##### 1.1.2.1 **Details** tab

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td><span>Model name</span></td><td>QScan</td></tr><tr><td><span>Technical name</span></td><td></td></tr><tr><td><span>Description</span></td><td><div class="docs-markdown"></div></td></tr><tr><td><span>Author</span></td><td></td></tr><tr><td><span>Version</span></td><td></td></tr><tr><td><span>DB vendor</span></td><td>Cassandra</td></tr><tr><td><span>DB version</span></td><td>3.x</td></tr><tr><td><span>Host</span></td><td></td></tr><tr><td><span>Port</span></td><td></td></tr><tr><td><span>Comments</span></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 1.1.3 **QScan** User-Defined Types

### <a id="containers"></a>

##### 2\. Keyspaces

### <a id="cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1 Keyspace **qscan**

![Hackolade image](/QScan%20documentation/image3.png?raw=true)

##### 2.1.1 **qscan** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Keyspace name</td><td>qscan</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Replication Strategy</td><td>SimpleStrategy</td></tr><tr><td>Replication Factor</td><td>1</td></tr><tr><td>Durable Writes</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr><tr><td>Add to CQL Script</td><td>true</td></tr></tbody></table>

##### 2.1.2 **qscan** Tables

### <a id="cd233050-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1 Table **by\_company\_name**

##### 2.1.2.1.1 **by\_company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image4.png?raw=true)

##### 2.1.2.1.2 **by\_company\_name** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>company_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.1.3 **by\_company\_name** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd235761-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235768-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235760-1aaa-11eb-a5a8-91debe8ed8a4>axfr</a></td><td class="no-break-word">bool</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235762-1aaa-11eb-a5a8-91debe8ed8a4>dmarc</a></td><td class="no-break-word">bool</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235763-1aaa-11eb-a5a8-91debe8ed8a4>ip_addresses</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235769-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235764-1aaa-11eb-a5a8-91debe8ed8a4>ports</a></td><td class="no-break-word">list&lt;num&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23576a-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235765-1aaa-11eb-a5a8-91debe8ed8a4>protocols</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23576b-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235766-1aaa-11eb-a5a8-91debe8ed8a4>services</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23576c-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd235767-1aaa-11eb-a5a8-91debe8ed8a4>spf</a></td><td class="no-break-word">bool</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235760-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.1 Column **axfr**

##### 2.1.2.1.3.1.1 **axfr** Tree Diagram

![Hackolade image](/QScan%20documentation/image5.png?raw=true)

##### 2.1.2.1.3.1.2 **axfr** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>axfr</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>bool</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Default</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235761-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.2 Column **company\_name**

##### 2.1.2.1.3.2.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image6.png?raw=true)

##### 2.1.2.1.3.2.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235762-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.3 Column **dmarc**

##### 2.1.2.1.3.3.1 **dmarc** Tree Diagram

![Hackolade image](/QScan%20documentation/image7.png?raw=true)

##### 2.1.2.1.3.3.2 **dmarc** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>dmarc</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>bool</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Default</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235763-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.4 Column **ip\_addresses**

##### 2.1.2.1.3.4.1 **ip\_addresses** Tree Diagram

![Hackolade image](/QScan%20documentation/image8.png?raw=true)

##### 2.1.2.1.3.4.2 **ip\_addresses** Hierarchy

Parent Column: **by\_company\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd235769-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.1.3.4.3 **ip\_addresses** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ip_addresses</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235769-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.5 Column **\[0\]**

##### 2.1.2.1.3.5.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image9.png?raw=true)

##### 2.1.2.1.3.5.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235764-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.6 Column **ports**

##### 2.1.2.1.3.6.1 **ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image10.png?raw=true)

##### 2.1.2.1.3.6.2 **ports** Hierarchy

Parent Column: **by\_company\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd23576a-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">numeric</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.1.3.6.3 **ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;num&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23576a-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.7 Column **\[0\]**

##### 2.1.2.1.3.7.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image11.png?raw=true)

##### 2.1.2.1.3.7.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235765-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.8 Column **protocols**

##### 2.1.2.1.3.8.1 **protocols** Tree Diagram

![Hackolade image](/QScan%20documentation/image12.png?raw=true)

##### 2.1.2.1.3.8.2 **protocols** Hierarchy

Parent Column: **by\_company\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd23576b-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.1.3.8.3 **protocols** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>protocols</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23576b-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.9 Column **\[0\]**

##### 2.1.2.1.3.9.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image13.png?raw=true)

##### 2.1.2.1.3.9.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235766-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.10 Column **services**

##### 2.1.2.1.3.10.1 **services** Tree Diagram

![Hackolade image](/QScan%20documentation/image14.png?raw=true)

##### 2.1.2.1.3.10.2 **services** Hierarchy

Parent Column: **by\_company\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd23576c-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.1.3.10.3 **services** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>services</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23576c-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.11 Column **\[0\]**

##### 2.1.2.1.3.11.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image15.png?raw=true)

##### 2.1.2.1.3.11.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235767-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.12 Column **spf**

##### 2.1.2.1.3.12.1 **spf** Tree Diagram

![Hackolade image](/QScan%20documentation/image16.png?raw=true)

##### 2.1.2.1.3.12.2 **spf** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>spf</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>bool</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Default</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd235768-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.1.3.13 Column **timestamp**

##### 2.1.2.1.3.13.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image17.png?raw=true)

##### 2.1.2.1.3.13.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.1.4 **by\_company\_name** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_company_name",
    "properties": {
        "axfr": {
            "type": "boolean"
        },
        "company_name": {
            "type": "string"
        },
        "dmarc": {
            "type": "boolean"
        },
        "ip_addresses": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "ports": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "number"
            }
        },
        "protocols": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "services": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "spf": {
            "type": "boolean"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "company_name",
        "timestamp"
    ]
}
```

##### 2.1.2.1.5 **by\_company\_name** JSON data

```
{
    "axfr": true,
    "company_name": "Lorem",
    "dmarc": true,
    "ip_addresses": [
        "Lorem"
    ],
    "ports": [
        4
    ],
    "protocols": [
        "Lorem"
    ],
    "services": [
        "Lorem"
    ],
    "spf": true,
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.1.6 **by\_company\_name** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_company_name" (
  "axfr" boolean,
  "company_name" text,
  "dmarc" boolean,
  "ip_addresses" list<text>,
  "ports" list<int>,
  "protocols" list<text>,
  "services" list<text>,
  "spf" boolean,
  "timestamp" timestamp,
  PRIMARY KEY ("company_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd23f3a2-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2 Table **by\_company\_protocol**

##### 2.1.2.2.1 **by\_company\_protocol** Tree Diagram

![Hackolade image](/QScan%20documentation/image18.png?raw=true)

##### 2.1.2.2.2 **by\_company\_protocol** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_company_protocol</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>company_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td></td><td>protocol</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.2.3 **by\_company\_protocol** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd23f3a3-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23f3a7-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23f3a6-1aaa-11eb-a5a8-91debe8ed8a4>protocol</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23f3a4-1aaa-11eb-a5a8-91debe8ed8a4>domains</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23f3a5-1aaa-11eb-a5a8-91debe8ed8a4>ports</a></td><td class="no-break-word">list&lt;num&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd23f3a8-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23f3a3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2.3.1 Column **company\_name**

##### 2.1.2.2.3.1.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image19.png?raw=true)

##### 2.1.2.2.3.1.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23f3a4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2.3.2 Column **domains**

##### 2.1.2.2.3.2.1 **domains** Tree Diagram

![Hackolade image](/QScan%20documentation/image20.png?raw=true)

##### 2.1.2.2.3.2.2 **domains** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domains</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23f3a5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2.3.3 Column **ports**

##### 2.1.2.2.3.3.1 **ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image21.png?raw=true)

##### 2.1.2.2.3.3.2 **ports** Hierarchy

Parent Column: **by\_company\_protocol**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd23f3a8-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">numeric</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.2.3.3.3 **ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;num&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23f3a8-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2.3.4 Column **\[0\]**

##### 2.1.2.2.3.4.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image22.png?raw=true)

##### 2.1.2.2.3.4.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23f3a6-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2.3.5 Column **protocol**

##### 2.1.2.2.3.5.1 **protocol** Tree Diagram

![Hackolade image](/QScan%20documentation/image23.png?raw=true)

##### 2.1.2.2.3.5.2 **protocol** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>protocol</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd23f3a7-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.2.3.6 Column **timestamp**

##### 2.1.2.2.3.6.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image24.png?raw=true)

##### 2.1.2.2.3.6.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.2.4 **by\_company\_protocol** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_company_protocol",
    "properties": {
        "company_name": {
            "type": "string"
        },
        "domains": {
            "type": "string"
        },
        "ports": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "number"
            }
        },
        "protocol": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "company_name",
        "protocol",
        "timestamp"
    ]
}
```

##### 2.1.2.2.5 **by\_company\_protocol** JSON data

```
{
    "company_name": "Lorem",
    "domains": "Lorem",
    "ports": [
        -91
    ],
    "protocol": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.2.6 **by\_company\_protocol** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_company_protocol" (
  "company_name" text,
  "domains" text,
  "ports" list<int>,
  "protocol" text,
  "timestamp" timestamp,
  PRIMARY KEY ("company_name", "timestamp", "protocol")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC, "protocol" ASC);
```

### <a id="cd241ab0-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3 Table **by\_domain\_name**

##### 2.1.2.3.1 **by\_domain\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image25.png?raw=true)

##### 2.1.2.3.2 **by\_domain\_name** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_domain_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>domain_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.3.3 **by\_domain\_name** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd241ab3-1aaa-11eb-a5a8-91debe8ed8a4>domain_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab7-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab1-1aaa-11eb-a5a8-91debe8ed8a4>axfr</a></td><td class="no-break-word">bool</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab2-1aaa-11eb-a5a8-91debe8ed8a4>dmarc</a></td><td class="no-break-word">bool</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab4-1aaa-11eb-a5a8-91debe8ed8a4>ip_addresses</a></td><td class="no-break-word">tuple</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab8-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab5-1aaa-11eb-a5a8-91debe8ed8a4>ports</a></td><td class="no-break-word">list&lt;num&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab9-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd241ab6-1aaa-11eb-a5a8-91debe8ed8a4>spf</a></td><td class="no-break-word">bool</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab1-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.1 Column **axfr**

##### 2.1.2.3.3.1.1 **axfr** Tree Diagram

![Hackolade image](/QScan%20documentation/image26.png?raw=true)

##### 2.1.2.3.3.1.2 **axfr** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>axfr</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>bool</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Default</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab2-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.2 Column **dmarc**

##### 2.1.2.3.3.2.1 **dmarc** Tree Diagram

![Hackolade image](/QScan%20documentation/image27.png?raw=true)

##### 2.1.2.3.3.2.2 **dmarc** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>dmarc</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>bool</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Default</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.3 Column **domain\_name**

##### 2.1.2.3.3.3.1 **domain\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image28.png?raw=true)

##### 2.1.2.3.3.3.2 **domain\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domain_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.4 Column **ip\_addresses**

##### 2.1.2.3.3.4.1 **ip\_addresses** Tree Diagram

![Hackolade image](/QScan%20documentation/image29.png?raw=true)

##### 2.1.2.3.3.4.2 **ip\_addresses** Hierarchy

Parent Column: **by\_domain\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd241ab8-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.3.3.4.3 **ip\_addresses** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ip_addresses</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>tuple</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab8-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.5 Column **\[0\]**

##### 2.1.2.3.3.5.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image30.png?raw=true)

##### 2.1.2.3.3.5.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.6 Column **ports**

##### 2.1.2.3.3.6.1 **ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image31.png?raw=true)

##### 2.1.2.3.3.6.2 **ports** Hierarchy

Parent Column: **by\_domain\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd241ab9-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">numeric</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.3.3.6.3 **ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;num&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab9-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.7 Column **\[0\]**

##### 2.1.2.3.3.7.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image32.png?raw=true)

##### 2.1.2.3.3.7.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab6-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.8 Column **spf**

##### 2.1.2.3.3.8.1 **spf** Tree Diagram

![Hackolade image](/QScan%20documentation/image33.png?raw=true)

##### 2.1.2.3.3.8.2 **spf** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>spf</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>bool</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Default</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd241ab7-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.3.3.9 Column **timestamp**

##### 2.1.2.3.3.9.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image34.png?raw=true)

##### 2.1.2.3.3.9.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.3.4 **by\_domain\_name** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_domain_name",
    "properties": {
        "axfr": {
            "type": "boolean"
        },
        "dmarc": {
            "type": "boolean"
        },
        "domain_name": {
            "type": "string"
        },
        "ip_addresses": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "ports": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "number"
            }
        },
        "spf": {
            "type": "boolean"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "domain_name",
        "timestamp"
    ]
}
```

##### 2.1.2.3.5 **by\_domain\_name** JSON data

```
{
    "axfr": true,
    "dmarc": true,
    "domain_name": "Lorem",
    "ip_addresses": [
        "Lorem"
    ],
    "ports": [
        -17
    ],
    "spf": true,
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.3.6 **by\_domain\_name** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_domain_name" (
  "axfr" boolean,
  "dmarc" boolean,
  "domain_name" text,
  "ip_addresses" tuple<text>,
  "ports" list<int>,
  "spf" boolean,
  "timestamp" timestamp,
  PRIMARY KEY ("domain_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd2441c3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.4 Table **by\_ip\_port**

##### 2.1.2.4.1 **by\_ip\_port** Tree Diagram

![Hackolade image](/QScan%20documentation/image35.png?raw=true)

##### 2.1.2.4.2 **by\_ip\_port** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_ip_port</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>ip</td></tr><tr><td></td><td>port</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.4.3 **by\_ip\_port** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd2441c5-1aaa-11eb-a5a8-91debe8ed8a4>ip</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441c6-1aaa-11eb-a5a8-91debe8ed8a4>port</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441c8-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441c4-1aaa-11eb-a5a8-91debe8ed8a4>headers</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441c7-1aaa-11eb-a5a8-91debe8ed8a4>service</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441c4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.4.3.1 Column **headers**

##### 2.1.2.4.3.1.1 **headers** Tree Diagram

![Hackolade image](/QScan%20documentation/image36.png?raw=true)

##### 2.1.2.4.3.1.2 **headers** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>headers</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441c5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.4.3.2 Column **ip**

##### 2.1.2.4.3.2.1 **ip** Tree Diagram

![Hackolade image](/QScan%20documentation/image37.png?raw=true)

##### 2.1.2.4.3.2.2 **ip** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ip</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441c6-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.4.3.3 Column **port**

##### 2.1.2.4.3.3.1 **port** Tree Diagram

![Hackolade image](/QScan%20documentation/image38.png?raw=true)

##### 2.1.2.4.3.3.2 **port** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>port</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441c7-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.4.3.4 Column **service**

##### 2.1.2.4.3.4.1 **service** Tree Diagram

![Hackolade image](/QScan%20documentation/image39.png?raw=true)

##### 2.1.2.4.3.4.2 **service** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>service</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441c8-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.4.3.5 Column **timestamp**

##### 2.1.2.4.3.5.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image40.png?raw=true)

##### 2.1.2.4.3.5.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.4.4 **by\_ip\_port** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_ip_port",
    "properties": {
        "headers": {
            "type": "string"
        },
        "ip": {
            "type": "string"
        },
        "port": {
            "type": "string"
        },
        "service": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "ip",
        "port",
        "timestamp"
    ]
}
```

##### 2.1.2.4.5 **by\_ip\_port** JSON data

```
{
    "headers": "Lorem",
    "ip": "Lorem",
    "port": "Lorem",
    "service": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.4.6 **by\_ip\_port** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_ip_port" (
  "headers" text,
  "ip" text,
  "port" text,
  "service" text,
  "timestamp" timestamp,
  PRIMARY KEY (("ip", "port"), "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd2441cc-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5 Table **by\_ipaddress**

##### 2.1.2.5.1 **by\_ipaddress** Tree Diagram

![Hackolade image](/QScan%20documentation/image41.png?raw=true)

##### 2.1.2.5.2 **by\_ipaddress** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_ipaddress</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>ip_address</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.5.3 **by\_ipaddress** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd2441d0-1aaa-11eb-a5a8-91debe8ed8a4>ip_address</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441d3-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441cd-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441ce-1aaa-11eb-a5a8-91debe8ed8a4>cpe</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441cf-1aaa-11eb-a5a8-91debe8ed8a4>domain_name</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441d1-1aaa-11eb-a5a8-91debe8ed8a4>ports</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441d4-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441d2-1aaa-11eb-a5a8-91debe8ed8a4>services</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2441d5-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441cd-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.1 Column **company\_name**

##### 2.1.2.5.3.1.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image42.png?raw=true)

##### 2.1.2.5.3.1.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441ce-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.2 Column **cpe**

##### 2.1.2.5.3.2.1 **cpe** Tree Diagram

![Hackolade image](/QScan%20documentation/image43.png?raw=true)

##### 2.1.2.5.3.2.2 **cpe** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>cpe</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441cf-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.3 Column **domain\_name**

##### 2.1.2.5.3.3.1 **domain\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image44.png?raw=true)

##### 2.1.2.5.3.3.2 **domain\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domain_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441d0-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.4 Column **ip\_address**

##### 2.1.2.5.3.4.1 **ip\_address** Tree Diagram

![Hackolade image](/QScan%20documentation/image45.png?raw=true)

##### 2.1.2.5.3.4.2 **ip\_address** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ip_address</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441d1-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.5 Column **ports**

##### 2.1.2.5.3.5.1 **ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image46.png?raw=true)

##### 2.1.2.5.3.5.2 **ports** Hierarchy

Parent Column: **by\_ipaddress**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd2441d4-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.5.3.5.3 **ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441d4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.6 Column **\[0\]**

##### 2.1.2.5.3.6.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image47.png?raw=true)

##### 2.1.2.5.3.6.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441d2-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.7 Column **services**

##### 2.1.2.5.3.7.1 **services** Tree Diagram

![Hackolade image](/QScan%20documentation/image48.png?raw=true)

##### 2.1.2.5.3.7.2 **services** Hierarchy

Parent Column: **by\_ipaddress**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd2441d5-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.5.3.7.3 **services** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>services</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441d5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.8 Column **\[0\]**

##### 2.1.2.5.3.8.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image49.png?raw=true)

##### 2.1.2.5.3.8.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2441d3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.5.3.9 Column **timestamp**

##### 2.1.2.5.3.9.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image50.png?raw=true)

##### 2.1.2.5.3.9.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.5.4 **by\_ipaddress** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_ipaddress",
    "properties": {
        "company_name": {
            "type": "string"
        },
        "cpe": {
            "type": "string"
        },
        "domain_name": {
            "type": "string"
        },
        "ip_address": {
            "type": "string"
        },
        "ports": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "services": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "ip_address",
        "timestamp"
    ]
}
```

##### 2.1.2.5.5 **by\_ipaddress** JSON data

```
{
    "company_name": "Lorem",
    "cpe": "Lorem",
    "domain_name": "Lorem",
    "ip_address": "Lorem",
    "ports": [
        "Lorem"
    ],
    "services": [
        "Lorem"
    ],
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.5.6 **by\_ipaddress** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_ipaddress" (
  "company_name" text,
  "cpe" text,
  "domain_name" text,
  "ip_address" text,
  "ports" list<text>,
  "services" list<text>,
  "timestamp" timestamp,
  PRIMARY KEY ("ip_address", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd2468d3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.6 Table **by\_port**

##### 2.1.2.6.1 **by\_port** Tree Diagram

![Hackolade image](/QScan%20documentation/image51.png?raw=true)

##### 2.1.2.6.2 **by\_port** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_port</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>port</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.6.3 **by\_port** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd2468d5-1aaa-11eb-a5a8-91debe8ed8a4>port</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2468d7-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2468d4-1aaa-11eb-a5a8-91debe8ed8a4>headers</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd2468d6-1aaa-11eb-a5a8-91debe8ed8a4>service</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2468d4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.6.3.1 Column **headers**

##### 2.1.2.6.3.1.1 **headers** Tree Diagram

![Hackolade image](/QScan%20documentation/image52.png?raw=true)

##### 2.1.2.6.3.1.2 **headers** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>headers</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2468d5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.6.3.2 Column **port**

##### 2.1.2.6.3.2.1 **port** Tree Diagram

![Hackolade image](/QScan%20documentation/image53.png?raw=true)

##### 2.1.2.6.3.2.2 **port** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>port</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2468d6-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.6.3.3 Column **service**

##### 2.1.2.6.3.3.1 **service** Tree Diagram

![Hackolade image](/QScan%20documentation/image54.png?raw=true)

##### 2.1.2.6.3.3.2 **service** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>service</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd2468d7-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.6.3.4 Column **timestamp**

##### 2.1.2.6.3.4.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image55.png?raw=true)

##### 2.1.2.6.3.4.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.6.4 **by\_port** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_port",
    "properties": {
        "headers": {
            "type": "string"
        },
        "port": {
            "type": "string"
        },
        "service": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "port",
        "timestamp"
    ]
}
```

##### 2.1.2.6.5 **by\_port** JSON data

```
{
    "headers": "Lorem",
    "port": "Lorem",
    "service": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.6.6 **by\_port** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_port" (
  "headers" text,
  "port" text,
  "service" text,
  "timestamp" timestamp,
  PRIMARY KEY ("port", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd248fe3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7 Table **by\_protocol**

##### 2.1.2.7.1 **by\_protocol** Tree Diagram

![Hackolade image](/QScan%20documentation/image56.png?raw=true)

##### 2.1.2.7.2 **by\_protocol** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_protocol</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>protocol</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.7.3 **by\_protocol** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd248fe7-1aaa-11eb-a5a8-91debe8ed8a4>protocol</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd248fe8-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd248fe4-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd248fe5-1aaa-11eb-a5a8-91debe8ed8a4>domains</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd248fe6-1aaa-11eb-a5a8-91debe8ed8a4>ports</a></td><td class="no-break-word">list&lt;num&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd248fe9-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd248fe4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7.3.1 Column **company\_name**

##### 2.1.2.7.3.1.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image57.png?raw=true)

##### 2.1.2.7.3.1.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd248fe5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7.3.2 Column **domains**

##### 2.1.2.7.3.2.1 **domains** Tree Diagram

![Hackolade image](/QScan%20documentation/image58.png?raw=true)

##### 2.1.2.7.3.2.2 **domains** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domains</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd248fe6-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7.3.3 Column **ports**

##### 2.1.2.7.3.3.1 **ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image59.png?raw=true)

##### 2.1.2.7.3.3.2 **ports** Hierarchy

Parent Column: **by\_protocol**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd248fe9-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">numeric</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.7.3.3.3 **ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;num&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd248fe9-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7.3.4 Column **\[0\]**

##### 2.1.2.7.3.4.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image60.png?raw=true)

##### 2.1.2.7.3.4.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd248fe7-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7.3.5 Column **protocol**

##### 2.1.2.7.3.5.1 **protocol** Tree Diagram

![Hackolade image](/QScan%20documentation/image61.png?raw=true)

##### 2.1.2.7.3.5.2 **protocol** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>protocol</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd248fe8-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.7.3.6 Column **timestamp**

##### 2.1.2.7.3.6.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image62.png?raw=true)

##### 2.1.2.7.3.6.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.7.4 **by\_protocol** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_protocol",
    "properties": {
        "company_name": {
            "type": "string"
        },
        "domains": {
            "type": "string"
        },
        "ports": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "number"
            }
        },
        "protocol": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "protocol",
        "timestamp"
    ]
}
```

##### 2.1.2.7.5 **by\_protocol** JSON data

```
{
    "company_name": "Lorem",
    "domains": "Lorem",
    "ports": [
        4
    ],
    "protocol": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.7.6 **by\_protocol** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_protocol" (
  "company_name" text,
  "domains" text,
  "ports" list<int>,
  "protocol" text,
  "timestamp" timestamp,
  PRIMARY KEY ("protocol", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd24b6f2-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.8 Table **by\_service\_name**

##### 2.1.2.8.1 **by\_service\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image63.png?raw=true)

##### 2.1.2.8.2 **by\_service\_name** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>by_service_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>service</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.8.3 **by\_service\_name** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd24b6f5-1aaa-11eb-a5a8-91debe8ed8a4>service</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6f6-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6f3-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6f4-1aaa-11eb-a5a8-91debe8ed8a4>ports</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6f7-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6f3-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.8.3.1 Column **company\_name**

##### 2.1.2.8.3.1.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image64.png?raw=true)

##### 2.1.2.8.3.1.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6f4-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.8.3.2 Column **ports**

##### 2.1.2.8.3.2.1 **ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image65.png?raw=true)

##### 2.1.2.8.3.2.2 **ports** Hierarchy

Parent Column: **by\_service\_name**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd24b6f7-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.8.3.2.3 **ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6f7-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.8.3.3 Column **\[0\]**

##### 2.1.2.8.3.3.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image66.png?raw=true)

##### 2.1.2.8.3.3.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6f5-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.8.3.4 Column **service**

##### 2.1.2.8.3.4.1 **service** Tree Diagram

![Hackolade image](/QScan%20documentation/image67.png?raw=true)

##### 2.1.2.8.3.4.2 **service** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>service</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6f6-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.8.3.5 Column **timestamp**

##### 2.1.2.8.3.5.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image68.png?raw=true)

##### 2.1.2.8.3.5.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.8.4 **by\_service\_name** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "by_service_name",
    "properties": {
        "company_name": {
            "type": "string"
        },
        "ports": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "service": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "service",
        "timestamp"
    ]
}
```

##### 2.1.2.8.5 **by\_service\_name** JSON data

```
{
    "company_name": "Lorem",
    "ports": [
        "Lorem"
    ],
    "service": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.8.6 **by\_service\_name** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_service_name" (
  "company_name" text,
  "ports" list<text>,
  "service" text,
  "timestamp" timestamp,
  PRIMARY KEY ("service", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd24b6fb-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9 Table **company\_scores**

##### 2.1.2.9.1 **company\_scores** Tree Diagram

![Hackolade image](/QScan%20documentation/image69.png?raw=true)

##### 2.1.2.9.2 **company\_scores** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>company_scores</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>company_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.9.3 **company\_scores** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd24b6fe-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b708-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6fc-1aaa-11eb-a5a8-91debe8ed8a4>ca</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b70a-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6fd-1aaa-11eb-a5a8-91debe8ed8a4>certificate_data</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b6ff-1aaa-11eb-a5a8-91debe8ed8a4>cpe</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b700-1aaa-11eb-a5a8-91debe8ed8a4>dmarc</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b701-1aaa-11eb-a5a8-91debe8ed8a4>high_impact_weight</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b702-1aaa-11eb-a5a8-91debe8ed8a4>low_impact_weight</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b703-1aaa-11eb-a5a8-91debe8ed8a4>medium_impact_weight</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b704-1aaa-11eb-a5a8-91debe8ed8a4>number_ip_addr</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b705-1aaa-11eb-a5a8-91debe8ed8a4>open_ports_non_standard</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b70b-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b706-1aaa-11eb-a5a8-91debe8ed8a4>open_ports_standard</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b70c-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b707-1aaa-11eb-a5a8-91debe8ed8a4>spf</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd24b709-1aaa-11eb-a5a8-91debe8ed8a4>total_core</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6fc-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.1 Column **ca**

##### 2.1.2.9.3.1.1 **ca** Tree Diagram

![Hackolade image](/QScan%20documentation/image70.png?raw=true)

##### 2.1.2.9.3.1.2 **ca** Hierarchy

Parent Column: **company\_scores**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd24b70a-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.9.3.1.3 **ca** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ca</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b70a-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.2 Column **\[0\]**

##### 2.1.2.9.3.2.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image71.png?raw=true)

##### 2.1.2.9.3.2.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6fd-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.3 Column **certificate\_data**

##### 2.1.2.9.3.3.1 **certificate\_data** Tree Diagram

![Hackolade image](/QScan%20documentation/image72.png?raw=true)

##### 2.1.2.9.3.3.2 **certificate\_data** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>certificate_data</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6fe-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.4 Column **company\_name**

##### 2.1.2.9.3.4.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image73.png?raw=true)

##### 2.1.2.9.3.4.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b6ff-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.5 Column **cpe**

##### 2.1.2.9.3.5.1 **cpe** Tree Diagram

![Hackolade image](/QScan%20documentation/image74.png?raw=true)

##### 2.1.2.9.3.5.2 **cpe** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>cpe</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b700-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.6 Column **dmarc**

##### 2.1.2.9.3.6.1 **dmarc** Tree Diagram

![Hackolade image](/QScan%20documentation/image75.png?raw=true)

##### 2.1.2.9.3.6.2 **dmarc** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>dmarc</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b701-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.7 Column **high\_impact\_weight**

##### 2.1.2.9.3.7.1 **high\_impact\_weight** Tree Diagram

![Hackolade image](/QScan%20documentation/image76.png?raw=true)

##### 2.1.2.9.3.7.2 **high\_impact\_weight** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>high_impact_weight</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b702-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.8 Column **low\_impact\_weight**

##### 2.1.2.9.3.8.1 **low\_impact\_weight** Tree Diagram

![Hackolade image](/QScan%20documentation/image77.png?raw=true)

##### 2.1.2.9.3.8.2 **low\_impact\_weight** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>low_impact_weight</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b703-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.9 Column **medium\_impact\_weight**

##### 2.1.2.9.3.9.1 **medium\_impact\_weight** Tree Diagram

![Hackolade image](/QScan%20documentation/image78.png?raw=true)

##### 2.1.2.9.3.9.2 **medium\_impact\_weight** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>medium_impact_weight</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b704-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.10 Column **number\_ip\_addr**

##### 2.1.2.9.3.10.1 **number\_ip\_addr** Tree Diagram

![Hackolade image](/QScan%20documentation/image79.png?raw=true)

##### 2.1.2.9.3.10.2 **number\_ip\_addr** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>number_ip_addr</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b705-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.11 Column **open\_ports\_non\_standard**

##### 2.1.2.9.3.11.1 **open\_ports\_non\_standard** Tree Diagram

![Hackolade image](/QScan%20documentation/image80.png?raw=true)

##### 2.1.2.9.3.11.2 **open\_ports\_non\_standard** Hierarchy

Parent Column: **company\_scores**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd24b70b-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.9.3.11.3 **open\_ports\_non\_standard** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>open_ports_non_standard</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b70b-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.12 Column **\[0\]**

##### 2.1.2.9.3.12.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image81.png?raw=true)

##### 2.1.2.9.3.12.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b706-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.13 Column **open\_ports\_standard**

##### 2.1.2.9.3.13.1 **open\_ports\_standard** Tree Diagram

![Hackolade image](/QScan%20documentation/image82.png?raw=true)

##### 2.1.2.9.3.13.2 **open\_ports\_standard** Hierarchy

Parent Column: **company\_scores**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd24b70c-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.9.3.13.3 **open\_ports\_standard** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>open_ports_standard</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b70c-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.14 Column **\[0\]**

##### 2.1.2.9.3.14.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image83.png?raw=true)

##### 2.1.2.9.3.14.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b707-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.15 Column **spf**

##### 2.1.2.9.3.15.1 **spf** Tree Diagram

![Hackolade image](/QScan%20documentation/image84.png?raw=true)

##### 2.1.2.9.3.15.2 **spf** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>spf</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b708-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.16 Column **timestamp**

##### 2.1.2.9.3.16.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image85.png?raw=true)

##### 2.1.2.9.3.16.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd24b709-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.9.3.17 Column **total\_core**

##### 2.1.2.9.3.17.1 **total\_core** Tree Diagram

![Hackolade image](/QScan%20documentation/image86.png?raw=true)

##### 2.1.2.9.3.17.2 **total\_core** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>total_core</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.9.4 **company\_scores** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "company_scores",
    "properties": {
        "ca": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "certificate_data": {
            "type": "string"
        },
        "company_name": {
            "type": "string"
        },
        "cpe": {
            "type": "string"
        },
        "dmarc": {
            "type": "string"
        },
        "high_impact_weight": {
            "type": "string"
        },
        "low_impact_weight": {
            "type": "string"
        },
        "medium_impact_weight": {
            "type": "string"
        },
        "number_ip_addr": {
            "type": "number"
        },
        "open_ports_non_standard": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "open_ports_standard": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "spf": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "total_core": {
            "type": "string"
        }
    },
    "required": [
        "company_name",
        "timestamp"
    ]
}
```

##### 2.1.2.9.5 **company\_scores** JSON data

```
{
    "ca": [
        "Lorem"
    ],
    "certificate_data": "Lorem",
    "company_name": "Lorem",
    "cpe": "Lorem",
    "dmarc": "Lorem",
    "high_impact_weight": "Lorem",
    "low_impact_weight": "Lorem",
    "medium_impact_weight": "Lorem",
    "number_ip_addr": -78,
    "open_ports_non_standard": [
        "Lorem"
    ],
    "open_ports_standard": [
        "Lorem"
    ],
    "spf": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000",
    "total_core": "Lorem"
}
```

##### 2.1.2.9.6 **company\_scores** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."company_scores" (
  "ca" list<text>,
  "certificate_data" text,
  "company_name" text,
  "cpe" text,
  "dmarc" text,
  "high_impact_weight" text,
  "low_impact_weight" text,
  "medium_impact_weight" text,
  "number_ip_addr" int,
  "open_ports_non_standard" list<text>,
  "open_ports_standard" list<text>,
  "spf" text,
  "timestamp" timestamp,
  "total_core" text,
  PRIMARY KEY ("company_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd250513-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.10 Table **domain\_company**

##### 2.1.2.10.1 **domain\_company** Tree Diagram

![Hackolade image](/QScan%20documentation/image87.png?raw=true)

##### 2.1.2.10.2 **domain\_company** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>domain_company</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>domain_name</td></tr><tr><td></td><td>company_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.10.3 **domain\_company** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd250515-1aaa-11eb-a5a8-91debe8ed8a4>domain_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd250514-1aaa-11eb-a5a8-91debe8ed8a4>company_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd250517-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd250516-1aaa-11eb-a5a8-91debe8ed8a4>port</a></td><td class="no-break-word">list&lt;num&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd250518-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd250514-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.10.3.1 Column **company\_name**

##### 2.1.2.10.3.1.1 **company\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image88.png?raw=true)

##### 2.1.2.10.3.1.2 **company\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>company_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd250515-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.10.3.2 Column **domain\_name**

##### 2.1.2.10.3.2.1 **domain\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image89.png?raw=true)

##### 2.1.2.10.3.2.2 **domain\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domain_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd250516-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.10.3.3 Column **port**

##### 2.1.2.10.3.3.1 **port** Tree Diagram

![Hackolade image](/QScan%20documentation/image90.png?raw=true)

##### 2.1.2.10.3.3.2 **port** Hierarchy

Parent Column: **domain\_company**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd250518-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">numeric</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.10.3.3.3 **port** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>port</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;num&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd250518-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.10.3.4 Column **\[0\]**

##### 2.1.2.10.3.4.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image91.png?raw=true)

##### 2.1.2.10.3.4.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd250517-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.10.3.5 Column **timestamp**

##### 2.1.2.10.3.5.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image92.png?raw=true)

##### 2.1.2.10.3.5.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.10.4 **domain\_company** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "domain_company",
    "properties": {
        "company_name": {
            "type": "string"
        },
        "domain_name": {
            "type": "string"
        },
        "port": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "number"
            }
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": [
        "company_name",
        "domain_name",
        "timestamp"
    ]
}
```

##### 2.1.2.10.5 **domain\_company** JSON data

```
{
    "company_name": "Lorem",
    "domain_name": "Lorem",
    "port": [
        -59
    ],
    "timestamp": "2011-02-03 04:05:00+0000"
}
```

##### 2.1.2.10.6 **domain\_company** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."domain_company" (
  "company_name" text,
  "domain_name" text,
  "port" list<int>,
  "timestamp" timestamp,
  PRIMARY KEY (("domain_name", "company_name"), "timestamp")
)
WITH bloom_filter_fp_chance = 0.01
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy','max_threshold':'32','min_threshold':'4'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd25051c-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11 Table **domain\_scores**

##### 2.1.2.11.1 **domain\_scores** Tree Diagram

![Hackolade image](/QScan%20documentation/image93.png?raw=true)

##### 2.1.2.11.2 **domain\_scores** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>domain_scores</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>domain_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.11.3 **domain\_scores** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd252c24-1aaa-11eb-a5a8-91debe8ed8a4>domain_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c2c-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c20-1aaa-11eb-a5a8-91debe8ed8a4>ca</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c2e-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c21-1aaa-11eb-a5a8-91debe8ed8a4>certificate_data</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c22-1aaa-11eb-a5a8-91debe8ed8a4>cpe</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c23-1aaa-11eb-a5a8-91debe8ed8a4>dmarc</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c25-1aaa-11eb-a5a8-91debe8ed8a4>high_impact_weight</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c26-1aaa-11eb-a5a8-91debe8ed8a4>low_impact_weight</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c27-1aaa-11eb-a5a8-91debe8ed8a4>medium_impact_weight</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c28-1aaa-11eb-a5a8-91debe8ed8a4>number_ip_addr</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c29-1aaa-11eb-a5a8-91debe8ed8a4>open_ports_non_standard</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c2f-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c2a-1aaa-11eb-a5a8-91debe8ed8a4>open_ports_standard</a></td><td class="no-break-word">list&lt;str&gt;</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c30-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c2b-1aaa-11eb-a5a8-91debe8ed8a4>spf</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd252c2d-1aaa-11eb-a5a8-91debe8ed8a4>total_score</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c20-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.1 Column **ca**

##### 2.1.2.11.3.1.1 **ca** Tree Diagram

![Hackolade image](/QScan%20documentation/image94.png?raw=true)

##### 2.1.2.11.3.1.2 **ca** Hierarchy

Parent Column: **domain\_scores**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd252c2e-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.11.3.1.3 **ca** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>ca</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c2e-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.2 Column **\[0\]**

##### 2.1.2.11.3.2.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image95.png?raw=true)

##### 2.1.2.11.3.2.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c21-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.3 Column **certificate\_data**

##### 2.1.2.11.3.3.1 **certificate\_data** Tree Diagram

![Hackolade image](/QScan%20documentation/image96.png?raw=true)

##### 2.1.2.11.3.3.2 **certificate\_data** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>certificate_data</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c22-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.4 Column **cpe**

##### 2.1.2.11.3.4.1 **cpe** Tree Diagram

![Hackolade image](/QScan%20documentation/image97.png?raw=true)

##### 2.1.2.11.3.4.2 **cpe** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>cpe</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c23-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.5 Column **dmarc**

##### 2.1.2.11.3.5.1 **dmarc** Tree Diagram

![Hackolade image](/QScan%20documentation/image98.png?raw=true)

##### 2.1.2.11.3.5.2 **dmarc** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>dmarc</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c24-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.6 Column **domain\_name**

##### 2.1.2.11.3.6.1 **domain\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image99.png?raw=true)

##### 2.1.2.11.3.6.2 **domain\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domain_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c25-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.7 Column **high\_impact\_weight**

##### 2.1.2.11.3.7.1 **high\_impact\_weight** Tree Diagram

![Hackolade image](/QScan%20documentation/image100.png?raw=true)

##### 2.1.2.11.3.7.2 **high\_impact\_weight** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>high_impact_weight</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c26-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.8 Column **low\_impact\_weight**

##### 2.1.2.11.3.8.1 **low\_impact\_weight** Tree Diagram

![Hackolade image](/QScan%20documentation/image101.png?raw=true)

##### 2.1.2.11.3.8.2 **low\_impact\_weight** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>low_impact_weight</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c27-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.9 Column **medium\_impact\_weight**

##### 2.1.2.11.3.9.1 **medium\_impact\_weight** Tree Diagram

![Hackolade image](/QScan%20documentation/image102.png?raw=true)

##### 2.1.2.11.3.9.2 **medium\_impact\_weight** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>medium_impact_weight</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c28-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.10 Column **number\_ip\_addr**

##### 2.1.2.11.3.10.1 **number\_ip\_addr** Tree Diagram

![Hackolade image](/QScan%20documentation/image103.png?raw=true)

##### 2.1.2.11.3.10.2 **number\_ip\_addr** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>number_ip_addr</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c29-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.11 Column **open\_ports\_non\_standard**

##### 2.1.2.11.3.11.1 **open\_ports\_non\_standard** Tree Diagram

![Hackolade image](/QScan%20documentation/image104.png?raw=true)

##### 2.1.2.11.3.11.2 **open\_ports\_non\_standard** Hierarchy

Parent Column: **domain\_scores**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd252c2f-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.11.3.11.3 **open\_ports\_non\_standard** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>open_ports_non_standard</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c2f-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.12 Column **\[0\]**

##### 2.1.2.11.3.12.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image105.png?raw=true)

##### 2.1.2.11.3.12.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c2a-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.13 Column **open\_ports\_standard**

##### 2.1.2.11.3.13.1 **open\_ports\_standard** Tree Diagram

![Hackolade image](/QScan%20documentation/image106.png?raw=true)

##### 2.1.2.11.3.13.2 **open\_ports\_standard** Hierarchy

Parent Column: **domain\_scores**

Child column(s):

<table class="field-properties-table"><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd252c30-1aaa-11eb-a5a8-91debe8ed8a4>[0]</a></td><td class="no-break-word">char</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.11.3.13.3 **open\_ports\_standard** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>open_ports_standard</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>list</td></tr><tr><td>Subtype</td><td>list&lt;str&gt;</td></tr><tr><td>Frozen</td><td>false</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Min items</td><td></td></tr><tr><td>Max items</td><td></td></tr><tr><td>Unique items</td><td>false</td></tr><tr><td>Additional items</td><td>true</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c30-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.14 Column **\[0\]**

##### 2.1.2.11.3.14.1 **\[0\]** Tree Diagram

![Hackolade image](/QScan%20documentation/image107.png?raw=true)

##### 2.1.2.11.3.14.2 **\[0\]** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Display name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td></td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c2b-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.15 Column **spf**

##### 2.1.2.11.3.15.1 **spf** Tree Diagram

![Hackolade image](/QScan%20documentation/image108.png?raw=true)

##### 2.1.2.11.3.15.2 **spf** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>spf</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c2c-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.16 Column **timestamp**

##### 2.1.2.11.3.16.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image109.png?raw=true)

##### 2.1.2.11.3.16.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd252c2d-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.11.3.17 Column **total\_score**

##### 2.1.2.11.3.17.1 **total\_score** Tree Diagram

![Hackolade image](/QScan%20documentation/image110.png?raw=true)

##### 2.1.2.11.3.17.2 **total\_score** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>total_score</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.11.4 **domain\_scores** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "domain_scores",
    "properties": {
        "ca": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "certificate_data": {
            "type": "string"
        },
        "cpe": {
            "type": "string"
        },
        "dmarc": {
            "type": "string"
        },
        "domain_name": {
            "type": "string"
        },
        "high_impact_weight": {
            "type": "string"
        },
        "low_impact_weight": {
            "type": "string"
        },
        "medium_impact_weight": {
            "type": "string"
        },
        "number_ip_addr": {
            "type": "number"
        },
        "open_ports_non_standard": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "open_ports_standard": {
            "type": "array",
            "additionalItems": true,
            "uniqueItems": false,
            "items": {
                "type": "string"
            }
        },
        "spf": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "total_score": {
            "type": "string"
        }
    },
    "required": [
        "domain_name",
        "timestamp"
    ]
}
```

##### 2.1.2.11.5 **domain\_scores** JSON data

```
{
    "ca": [
        "Lorem"
    ],
    "certificate_data": "Lorem",
    "cpe": "Lorem",
    "dmarc": "Lorem",
    "domain_name": "Lorem",
    "high_impact_weight": "Lorem",
    "low_impact_weight": "Lorem",
    "medium_impact_weight": "Lorem",
    "number_ip_addr": -72,
    "open_ports_non_standard": [
        "Lorem"
    ],
    "open_ports_standard": [
        "Lorem"
    ],
    "spf": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000",
    "total_score": "Lorem"
}
```

##### 2.1.2.11.6 **domain\_scores** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."domain_scores" (
  "ca" list<text>,
  "certificate_data" text,
  "cpe" text,
  "dmarc" text,
  "domain_name" text,
  "high_impact_weight" text,
  "low_impact_weight" text,
  "medium_impact_weight" text,
  "number_ip_addr" int,
  "open_ports_non_standard" list<text>,
  "open_ports_standard" list<text>,
  "spf" text,
  "timestamp" timestamp,
  "total_score" text,
  PRIMARY KEY ("domain_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="cd257a43-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12 Table **scanid\_domain**

##### 2.1.2.12.1 **scanid\_domain** Tree Diagram

![Hackolade image](/QScan%20documentation/image111.png?raw=true)

##### 2.1.2.12.2 **scanid\_domain** Properties

<table class="collection-properties-table"><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Table</td><td>scanid_domain</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Keyspace</td><td><a href=#cd72fe00-1aaa-11eb-a5a8-91debe8ed8a4>qscan</a></td></tr><tr><td>Additional properties</td><td>false</td></tr><tr><td colspan="2"><b>Partition key</b></td></tr><tr><td></td><td>scan_id</td></tr><tr><td></td><td>domain_name</td></tr><tr><td colspan="2"><b>Clustering key</b></td></tr><tr><td></td><td>timestamp</td></tr><tr><td>Options</td><td>[object Object]</td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.12.3 **scanid\_domain** Column

<table><thead><tr><td>Column</td><td>Type</td><td>Req</td><td>Key</td><td>Description</td><td>Comments</td></tr></thead><tbody><tr><td><a href=#cd257a4a-1aaa-11eb-a5a8-91debe8ed8a4>scan_id</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a45-1aaa-11eb-a5a8-91debe8ed8a4>domain_name</a></td><td class="no-break-word">text</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a4b-1aaa-11eb-a5a8-91debe8ed8a4>timestamp</a></td><td class="no-break-word">timestamp</td><td>true</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a44-1aaa-11eb-a5a8-91debe8ed8a4>certificate_data</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a46-1aaa-11eb-a5a8-91debe8ed8a4>number_ips</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a47-1aaa-11eb-a5a8-91debe8ed8a4>number_std_ports</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a48-1aaa-11eb-a5a8-91debe8ed8a4>number_websites</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a49-1aaa-11eb-a5a8-91debe8ed8a4>port_cpe</a></td><td class="no-break-word">text</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr><tr><td><a href=#cd257a4c-1aaa-11eb-a5a8-91debe8ed8a4>valid_websites</a></td><td class="no-break-word">int</td><td>false</td><td></td><td><div class="docs-markdown"></div></td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a44-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.1 Column **certificate\_data**

##### 2.1.2.12.3.1.1 **certificate\_data** Tree Diagram

![Hackolade image](/QScan%20documentation/image112.png?raw=true)

##### 2.1.2.12.3.1.2 **certificate\_data** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>certificate_data</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a45-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.2 Column **domain\_name**

##### 2.1.2.12.3.2.1 **domain\_name** Tree Diagram

![Hackolade image](/QScan%20documentation/image113.png?raw=true)

##### 2.1.2.12.3.2.2 **domain\_name** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>domain_name</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a46-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.3 Column **number\_ips**

##### 2.1.2.12.3.3.1 **number\_ips** Tree Diagram

![Hackolade image](/QScan%20documentation/image114.png?raw=true)

##### 2.1.2.12.3.3.2 **number\_ips** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>number_ips</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a47-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.4 Column **number\_std\_ports**

##### 2.1.2.12.3.4.1 **number\_std\_ports** Tree Diagram

![Hackolade image](/QScan%20documentation/image115.png?raw=true)

##### 2.1.2.12.3.4.2 **number\_std\_ports** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>number_std_ports</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a48-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.5 Column **number\_websites**

##### 2.1.2.12.3.5.1 **number\_websites** Tree Diagram

![Hackolade image](/QScan%20documentation/image116.png?raw=true)

##### 2.1.2.12.3.5.2 **number\_websites** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>number_websites</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a49-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.6 Column **port\_cpe**

##### 2.1.2.12.3.6.1 **port\_cpe** Tree Diagram

![Hackolade image](/QScan%20documentation/image117.png?raw=true)

##### 2.1.2.12.3.6.2 **port\_cpe** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>port_cpe</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a4a-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.7 Column **scan\_id**

##### 2.1.2.12.3.7.1 **scan\_id** Tree Diagram

![Hackolade image](/QScan%20documentation/image118.png?raw=true)

##### 2.1.2.12.3.7.2 **scan\_id** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>scan_id</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>char</td></tr><tr><td>Subtype</td><td>text</td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Partition key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Min length</td><td></td></tr><tr><td>Max length</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Format</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a4b-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.8 Column **timestamp**

##### 2.1.2.12.3.8.1 **timestamp** Tree Diagram

![Hackolade image](/QScan%20documentation/image119.png?raw=true)

##### 2.1.2.12.3.8.2 **timestamp** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>timestamp</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>timestamp</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>true</td></tr><tr><td>Clustering key</td><td>true</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

### <a id="cd257a4c-1aaa-11eb-a5a8-91debe8ed8a4"></a>2.1.2.12.3.9 Column **valid\_websites**

##### 2.1.2.12.3.9.1 **valid\_websites** Tree Diagram

![Hackolade image](/QScan%20documentation/image120.png?raw=true)

##### 2.1.2.12.3.9.2 **valid\_websites** properties

<table><thead><tr><td>Property</td><td>Value</td></tr></thead><tbody><tr><td>Name</td><td>valid_websites</td></tr><tr><td>Technical name</td><td></td></tr><tr><td>Activated</td><td>true</td></tr><tr><td>Id</td><td></td></tr><tr><td>Description</td><td><div class="docs-markdown"></div></td></tr><tr><td>Type</td><td>numeric</td></tr><tr><td>Subtype</td><td>int</td></tr><tr><td>Dependencies</td><td></td></tr><tr><td>Required</td><td>false</td></tr><tr><td>Static</td><td>false</td></tr><tr><td>Unit</td><td></td></tr><tr><td>Min value</td><td></td></tr><tr><td>Excl min</td><td>false</td></tr><tr><td>Max value</td><td></td></tr><tr><td>Excl max</td><td>false</td></tr><tr><td>Multiple of</td><td></td></tr><tr><td>Divisible by</td><td></td></tr><tr><td>Pattern</td><td></td></tr><tr><td>Default</td><td></td></tr><tr><td>Enum</td><td></td></tr><tr><td>Foreign table</td><td></td></tr><tr><td>Foreign field</td><td></td></tr><tr><td>Relationship type</td><td></td></tr><tr><td>Sample</td><td></td></tr><tr><td>Comments</td><td><div class="docs-markdown"></div></td></tr></tbody></table>

##### 2.1.2.12.4 **scanid\_domain** JSON Schema

```
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "title": "scanid_domain",
    "properties": {
        "certificate_data": {
            "type": "string"
        },
        "domain_name": {
            "type": "string"
        },
        "number_ips": {
            "type": "number"
        },
        "number_std_ports": {
            "type": "number"
        },
        "number_websites": {
            "type": "number"
        },
        "port_cpe": {
            "type": "string"
        },
        "scan_id": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "valid_websites": {
            "type": "number"
        }
    },
    "required": [
        "domain_name",
        "scan_id",
        "timestamp"
    ]
}
```

##### 2.1.2.12.5 **scanid\_domain** JSON data

```
{
    "certificate_data": "Lorem",
    "domain_name": "Lorem",
    "number_ips": -28,
    "number_std_ports": -54,
    "number_websites": -62,
    "port_cpe": "Lorem",
    "scan_id": "Lorem",
    "timestamp": "2011-02-03 04:05:00+0000",
    "valid_websites": -7
}
```

##### 2.1.2.12.6 **scanid\_domain** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."scanid_domain" (
  "certificate_data" text,
  "domain_name" text,
  "number_ips" int,
  "number_std_ports" int,
  "number_websites" int,
  "port_cpe" text,
  "scan_id" text,
  "timestamp" timestamp,
  "valid_websites" int,
  PRIMARY KEY (("scan_id", "domain_name"), "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

##### 2.1.3 **qscan** CQL Script

```
CREATE KEYSPACE IF NOT EXISTS "qscan" 
  WITH REPLICATION = {
    'class' : 'SimpleStrategy',
    'replication_factor' : 1
  }
AND DURABLE_WRITES = true; 

USE "qscan";

CREATE TABLE IF NOT EXISTS "qscan"."by_company_name" (
  "axfr" boolean,
  "company_name" text,
  "dmarc" boolean,
  "ip_addresses" list<text>,
  "ports" list<int>,
  "protocols" list<text>,
  "services" list<text>,
  "spf" boolean,
  "timestamp" timestamp,
  PRIMARY KEY ("company_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_company_protocol" (
  "company_name" text,
  "domains" text,
  "ports" list<int>,
  "protocol" text,
  "timestamp" timestamp,
  PRIMARY KEY ("company_name", "timestamp", "protocol")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC, "protocol" ASC);

CREATE TABLE IF NOT EXISTS "qscan"."by_domain_name" (
  "axfr" boolean,
  "dmarc" boolean,
  "domain_name" text,
  "ip_addresses" tuple<text>,
  "ports" list<int>,
  "spf" boolean,
  "timestamp" timestamp,
  PRIMARY KEY ("domain_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_ip_port" (
  "headers" text,
  "ip" text,
  "port" text,
  "service" text,
  "timestamp" timestamp,
  PRIMARY KEY (("ip", "port"), "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_ipaddress" (
  "company_name" text,
  "cpe" text,
  "domain_name" text,
  "ip_address" text,
  "ports" list<text>,
  "services" list<text>,
  "timestamp" timestamp,
  PRIMARY KEY ("ip_address", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_port" (
  "headers" text,
  "port" text,
  "service" text,
  "timestamp" timestamp,
  PRIMARY KEY ("port", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_protocol" (
  "company_name" text,
  "domains" text,
  "ports" list<int>,
  "protocol" text,
  "timestamp" timestamp,
  PRIMARY KEY ("protocol", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."by_service_name" (
  "company_name" text,
  "ports" list<text>,
  "service" text,
  "timestamp" timestamp,
  PRIMARY KEY ("service", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."company_scores" (
  "ca" list<text>,
  "certificate_data" text,
  "company_name" text,
  "cpe" text,
  "dmarc" text,
  "high_impact_weight" text,
  "low_impact_weight" text,
  "medium_impact_weight" text,
  "number_ip_addr" int,
  "open_ports_non_standard" list<text>,
  "open_ports_standard" list<text>,
  "spf" text,
  "timestamp" timestamp,
  "total_core" text,
  PRIMARY KEY ("company_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."domain_company" (
  "company_name" text,
  "domain_name" text,
  "port" list<int>,
  "timestamp" timestamp,
  PRIMARY KEY (("domain_name", "company_name"), "timestamp")
)
WITH bloom_filter_fp_chance = 0.01
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy','max_threshold':'32','min_threshold':'4'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."domain_scores" (
  "ca" list<text>,
  "certificate_data" text,
  "cpe" text,
  "dmarc" text,
  "domain_name" text,
  "high_impact_weight" text,
  "low_impact_weight" text,
  "medium_impact_weight" text,
  "number_ip_addr" int,
  "open_ports_non_standard" list<text>,
  "open_ports_standard" list<text>,
  "spf" text,
  "timestamp" timestamp,
  "total_score" text,
  PRIMARY KEY ("domain_name", "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);

CREATE TABLE IF NOT EXISTS "qscan"."scanid_domain" (
  "certificate_data" text,
  "domain_name" text,
  "number_ips" int,
  "number_std_ports" int,
  "number_websites" int,
  "port_cpe" text,
  "scan_id" text,
  "timestamp" timestamp,
  "valid_websites" int,
  PRIMARY KEY (("scan_id", "domain_name"), "timestamp")
)
WITH bloom_filter_fp_chance = 0.1
  AND caching = {'keys':'ALL','rows_per_partition':'NONE'}
  AND dclocal_read_repair_chance = 0.1
  AND default_time_to_live = 0
  AND gc_grace_seconds = 864000
  AND memtable_flush_period_in_ms = 0
  AND min_index_interval = 128
  AND max_index_interval = 2048
  AND read_repair_chance = 0
  AND speculative_retry = '99PERCENTILE'
  AND crc_check_chance = 1
  AND compression = {'chunk_length_in_kb':'64','class':'org.apache.cassandra.io.compress.LZ4Compressor'}
  AND compaction = {'class':'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
  AND CLUSTERING ORDER BY ("timestamp" DESC);
```

### <a id="edges"></a>

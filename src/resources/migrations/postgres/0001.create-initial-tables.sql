---- -- LEVEL 1
---- -- Tables and References

create schema enrichments;

create table enrichment.vulnerability
(
    -- Identifiers
    vulnerability_id              varchar not null -- id from `cve.cve_data_meta.id`
        constraint vulnerability_pkey
            primary key,

    -- References

    -- Metadata
    published_at                  timestamp,       -- Timestamp record was published
    last_modified_at              timestamp,       -- Timestamp record was modified

    -- CVE Data
    cve_type                      varchar,         -- always 'cve'
    cve_format                    varchar,         -- format of cve data
    cve_version                   varchar,         -- version of api when record was retrieved
    cve_assigner                  varchar,         -- assigner from `cve.cve_data_meta.assigner`
    cve_problem_type              varchar,         -- type of problem from `cve.problemtype.problemtypedata.description.value`
    cve_problem_type_lang         varchar,         -- language type of problem is in from `cve.problemtype.problemtypedata.description.lang`
    cve_description               varchar,         -- description of cve from `cve.description.description_data.value`
    cve_description_lang          varchar,         -- language of cve description from `cve.description.description_data.lang`

    -- Impact Data
    impact_version                varchar,         -- mapped from `impact.baseMetricV3.cvssV3.version`
    impact_vector_string          varchar,         -- mapped from `impact.baseMetricV3.cvssV3.vectorString`
    impact_attack_vector          varchar,         -- mapped from `impact.baseMetricV3.cvssV3.attackVector`
    impact_attack_complexity      varchar,         -- mapped from `impact.baseMetricV3.cvssV3.attackComplexity`
    impact_privileges_required    varchar,         -- mapped from `impact.baseMetricV3.cvssV3.privilegesRequired`
    impact_user_interaction       varchar,         -- mapped from `impact.baseMetricV3.cvssV3.userInteraction`
    impact_scope                  varchar,         -- mapped from `impact.baseMetricV3.cvssV3.scope`
    impact_confidentiality_impact varchar,         -- mapped from `impact.baseMetricV3.cvssV3.confidentialityImpact`
    impact_integrity_impact       varchar,         -- mapped from `impact.baseMetricV3.cvssV3.integrityImpact`
    impact_availability_impact    varchar,         -- mapped from `impact.baseMetricV3.cvssV3.availabilityImpact`
    impact_base_score             float,           -- mapped from `impact.baseMetricV3.cvssV3.baseScore`
    impact_base_severity          varchar,         -- mapped from `impact.baseMetricV3.cvssV3.baseSeverity`
    impact_exploitability_score   float,           -- mapped from `impact.baseMetricV3.exploitabilityScore`
    impact_score                  float,           -- mapped from `impact.baseMetricV3.impactScore`

    -- Additional filtering info
    has_exploit                   boolean
);

alter table enrichment.vulnerability
    owner to wcaasmgmt;

create table enrichment.vulnerable_service
(
    -- Identifiers
    service_id              varchar not null -- uuid assigned on data ingress
        constraint vulnerable_service_pkey
            primary key,

    -- References
    vulnerability_id        varchar,

    -- Data
    cpe_uri                 varchar,
    cpe_part                varchar,         -- derived from cpe_uri
    cpe_vendor              varchar,         -- derived from cpe_uri
    cpe_product             varchar,         -- derived from cpe_uri
    cpe_product_version     varchar,         -- derived from cpe_uri
    cpe_update              varchar,         -- derived from cpe_uri
    cpe_edition             varchar,         -- derived from cpe_uri
    cpe_language            varchar,         -- derived from cpe_uri
    cpe_sw_edition          varchar,         -- derived from cpe_uri
    cpe_target_sw           varchar,         -- derived from cpe_uri
    cpe_target_hw           varchar,         -- derived from cpe_uri
    cpe_other               varchar,         -- derived from cpe_uri
    version_start_including varchar,
    version_start_excluding varchar,
    version_end_including   varchar,
    version_end_excluding   varchar,
    is_vulnerable           boolean
);

alter table enrichment.vulnerable_service
    owner to wcaasmgmt;

create table enrichment.reference
(
    reference_id     varchar not null
        constraint reference_pkey
            primary key,
    vulnerability_id varchar,
    url              varchar,
    name             varchar,
    source           varchar
);

alter table enrichment.reference
    owner to wcaasmgmt;

create table enrichment.reference_tag
(
    reference_tag_id varchar not null
        constraint reference_tag_pkey
            primary key,
    name             varchar,
    created_at       timestamp
);

alter table enrichment.reference_tag
    owner to wcaasmgmt;

create table enrichment.reference_tags
(
    reference_id     varchar,
    reference_tag_id varchar
);

alter table enrichment.reference_tags
    owner to wcaasmgmt;


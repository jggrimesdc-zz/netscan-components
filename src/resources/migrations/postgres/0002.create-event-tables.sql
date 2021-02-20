CREATE TABLE enrichment.events
(
    id                                 integer PRIMARY KEY,
    source_event_id                    text,
    timestamp                          timestamp,
    event_date                         date,
    event_time                         timestamp,
    event_type                         text,
    event_name                         text,
    event_summary                      text,
    event_goal                         text,
    service_modified                   text,
    attack_vector                      text,
    distribution_vector                text,
    vulnerability_potential            text,
    article_links                      text,
    source_detail_url                  text,
    source_of_event_data               text,
    event_additional_notes             text,
    infectious_potential_name          text,
    infectious_potential_data          text,
    depth_of_impact_name               text,
    depth_of_impact_data               text,
    business_associate_present         text,
    prop                               text,
    app_count                          integer,
    entity_notes                       text,
    entity_affected                    text,
    count_of_individuals_affected      integer,
    entity_naics_id                    integer,
    entity_type                        text,
    entity_state_code                  text,
    entity_zip_codes                   text,
    entity_country_code                text,
    entity_reason_targeted             text,
    entity_revenue_amount              text,
    entity_revenue_currency_code       text,
    entity_count_of_locations_affected integer,
    entity_secondary_victim_name       text,
    entity_secondary_victim_amount     integer,
    entity_secondary_victim_notes      text,
    cves                               text,
    campaign_id                        text,
    report_accuracy_confidence         text,
    control_failure                    text,
    cost_corrective_action             text,
    security_incident_state            text
);

CREATE TABLE enrichment.event_veris_supplemental_info
(
    event_id              integer PRIMARY KEY,
    event_attributes      json,
    event_discovery       json,
    event_results         json,
    event_notes           json,
    entity_assets         json,
    additional_info       json,
    value_chain           json,
    discovery_info        json,
    impact                json,
    timeline              json,
    source_schema_version text,
    event_target          text,
    veris_source_id       text
);

CREATE TABLE enrichment.incident_attacker_relationship
(
    incident_attacker_id integer PRIMARY KEY,
    event_id             integer,
    attacker_id          integer
        UNIQUE (event_id, attacker_id)
);

CREATE TABLE enrichment.event_attacker
(
    attacker_id                  integer PRIMARY KEY,
    attacker_name                text,
    attacker_type                text,
    state_code_of_attacker       text,
    source_of_attacker_data      text,
    attacker_country_code        text,
    attacker_relationship        text,
    attacker_notes               text,
    attacker_zip_code            text,
    attacker_internal_job_change text,
    attacker_naics_id            integer,
    attacker_naics_name          text,
    attacker_malware_name        text
);

CREATE TABLE enrichment.naics_reference
(
    naics_id      integer PRIMARY KEY,
    naics_code    integer,
    industry_name text
);

ALTER TABLE enrichment.events
    ADD FOREIGN KEY (id) REFERENCES enrichment.event_veris_supplemental_info (event_id);

ALTER TABLE enrichment.events
    ADD FOREIGN KEY (id) REFERENCES enrichment.incident_attacker_relationship (event_id);

ALTER TABLE enrichment.incident_attacker_relationship
    ADD FOREIGN KEY (attacker_id) REFERENCES enrichment.event_attacker (attacker_id);

ALTER TABLE enrichment.naics_reference
    ADD FOREIGN KEY (naics_id) REFERENCES enrichment.event_attacker (attacker_naics_id);

ALTER TABLE enrichment.naics_reference
    ADD FOREIGN KEY (naics_id) REFERENCES enrichment.events (entity_naics_id);

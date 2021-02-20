CREATE SCHEMA threat_actor;

CREATE TABLE threat_actor.tactic
(
    id                SERIAL NOT NULL PRIMARY KEY,
    name              TEXT,
    description       TEXT,
    type              TEXT,
    short_name        TEXT,
    internal_id       TEXT,
    external_id       TEXT,
    external_url      TEXT,
    ext_references_id INTEGER,
    created           TIMESTAMP,
    modified          TIMESTAMP
);

CREATE TABLE threat_actor.technique
(
    id                    SERIAL NOT NULL PRIMARY KEY,
    name                  TEXT,
    description           TEXT,
    type                  TEXT,
    internal_id           TEXT,
    external_id           TEXT,
    external_url          TEXT,
    version               TEXT,
    is_subtechnique       BOOLEAN,
    deprecated            BOOLEAN,
    remote_support        BOOLEAN,
    revoked               BOOLEAN,
    network_requirements  BOOLEAN,
    detection             TEXT,
    defense_bypassed      TEXT[],
    platforms             TEXT[],
    tactics               TEXT[],
    contributors          TEXT[],
    impact_type           TEXT[],
    data_sources          TEXT[],
    effective_permissions TEXT[],
    permissions_required  TEXT[],
    system_requirements   TEXT[],
    ext_references_id     INTEGER,
    created               TIMESTAMP,
    modified              TIMESTAMP
);

CREATE TABLE threat_actor.group
(
    id                SERIAL NOT NULL PRIMARY KEY,
    name              TEXT,
    description       TEXT,
    type              TEXT,
    internal_id       TEXT,
    external_id       TEXT,
    external_url      TEXT,
    aliases           TEXT[],
    version           TEXT,
    contributors      TEXT[],
    revoked           BOOLEAN,
    ext_references_id INTEGER,
    aliases_vector    TSVECTOR,
    created           TIMESTAMP,
    modified          TIMESTAMP
);

CREATE FUNCTION threat_actor_set_aliases() RETURNS trigger AS $$
begin
  new.aliases_vector
:= array_to_tsvector(new.aliases) ||
    to_tsvector(new.external_id || ' ');
return new;
end
$$
LANGUAGE plpgsql;

CREATE TRIGGER threat_actor_vector_update
    BEFORE INSERT OR
UPDATE
    ON threat_actor.group FOR EACH ROW EXECUTE PROCEDURE threat_actor_set_aliases();

CREATE TABLE threat_actor.software
(
    id                SERIAL NOT NULL PRIMARY KEY,
    name              TEXT,
    description       TEXT,
    type              TEXT,
    internal_id       TEXT,
    external_id       TEXT,
    external_url      TEXT,
    aliases           TEXT[],
    platforms         TEXT[],
    contributors      TEXT[],
    labels            TEXT[],
    revoked           BOOLEAN,
    version           TEXT,
    ext_references_id INTEGER,
    created           TIMESTAMP,
    modified          TIMESTAMP
);

CREATE TABLE threat_actor.mitigation
(
    id                SERIAL NOT NULL PRIMARY KEY,
    name              TEXT,
    description       TEXT,
    type              TEXT,
    internal_id       TEXT,
    external_id       TEXT,
    external_url      TEXT,
    version           TEXT,
    old_attack_id     TEXT,
    deprecated        BOOLEAN,
    ext_references_id INTEGER,
    created           TIMESTAMP,
    modified          TIMESTAMP
);

CREATE TABLE threat_actor.ext_reference
(
    id          INTEGER PRIMARY KEY,
    source_name TEXT,
    source_url  TEXT,
    external_id TEXT,
    description TEXT
);

CREATE TABLE threat_actor.relationship
(
    id                SERIAL  NOT NULL PRIMARY KEY,
    source_id         INTEGER NOT NULL,
    source_type       TEXT,
    target_id         INTEGER NOT NULL,
    target_type       TEXT,
    relationship_type text
);

CREATE VIEW threat_actor.id_mapping AS
select id, internal_id
from threat_actor.tactic
union
select id, internal_id
from threat_actor.technique
union
select id, internal_id
from threat_actor.group
union
select id, internal_id
from threat_actor.software
union
select id, internal_id
from threat_actor.mitigation;

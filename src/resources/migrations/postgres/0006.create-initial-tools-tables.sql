CREATE TABLE IF NOT EXISTS tool.tool
(
    "ID"
    SERIAL
    PRIMARY
    KEY,
    "NAME"
    text,
    "CATEGORY"
    text[],
    "DESCRIPTION"
    text,
    "PACKAGE_URL"
    text,
    "AUTHOR"
    text,
    "LICENSE"
    text,
    "PACKAGE_VERSION"
    text,
    "PACKAGE_RELEASE"
    text,
    "ARCH"
    text[],
    "DEPENDS"
    text[],
    "DLAGENTS"
    text[],
    "SHA512SUMS"
    text
[],
    "SOURCE_OF_TOOL"
    text
);

CREATE TABLE IF NOT EXISTS "tool.mitre_crosswalk"
(
    "ID"
    SERIAL
    PRIMARY
    KEY,
    "TOOL_ID"
    int,
    "MITRE_SOFTWARE_ID"
    int
);

ALTER TABLE "tool.mitre_crosswalk"
    ADD FOREIGN KEY ("TOOL_ID") REFERENCES tool.tool ("ID");

-- view for summary view
create view tools_summary_view as
select t_t."NAME",
       t_t."CATEGORY",
       t_t."DESCRIPTION",
       t_t."PACKAGE_URL",
       t_t."SOURCE_OF_TOOL",
       ta_s.external_id,
       ta_s.external_url
from tool.tool AS t_t
         INNER JOIN tool.mitre_crosswalk AS t_mc ON (t_t."ID" = t_mc."TOOL_ID")
         INNER JOIN threat_actor.software AS ta_s ON (t_mc."MITRE_SOFTWARE_ID" = ta_s.id);

-- view for ttp query relationship view
create view ttp_tools_relationship_view as
select ta_t.external_id  as tactic_external_id,
       ta_t.name,
       ta_t.description,
       ta_t.type,
       ta_t.external_url as tactic_external_url,
       ta_t.tactics,
       t_t."NAME",
       t_t."CATEGORY",
       t_t."DESCRIPTION",
       t_t."PACKAGE_URL",
       t_t."SOURCE_OF_TOOL",
       ta_s.external_id  as software_external_id,
       ta_s.external_url as software_external_url,
       ta_r.target_type,
       ta_r.relationship_type
from tool.tool AS t_t
         INNER JOIN tool.mitre_crosswalk AS t_mc ON (t_t."ID" = t_mc."TOOL_ID")
         INNER JOIN threat_actor.software AS ta_s ON (t_mc."MITRE_SOFTWARE_ID" = ta_s.id)
         INNER JOIN threat_actor.relationship AS ta_r ON (ta_s.id = ta_r.source_id)
         INNER JOIN threat_actor.technique AS ta_t ON (ta_r.target_id = ta_t.id)
;

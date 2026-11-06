# MTW-v1-2026 — title width study

852 eligible English GOV.UK guide-title strings from a fixed 859-record frame. Measured in one recorded environment: DejaVu Sans Book 2.37 at 20 CSS px and Chromium 141.0.7390.37. Original measurements were finalized on 20 October 2026. This public projection and its validation note were prepared on 30 October 2026.

Canonical study: https://moltoyo.com/research/title-width-study

## Files and fields

- measurements.csv / measurements.json: the same 852 records, with source URL and title metadata, Unicode counts and original Canvas/DOM widths. source_id is the canonical path; recorded_source_id retains historical metadata. source_id_corrected marks the documented path-only correction. No title or width was replaced.
- by-length.csv / by-length.json: all 74 exact-codepoint groups. n is the number of titles. Minimum, P10, median, P90, maximum and sample SD are CSS pixels. primary_stratum means n>=10, a descriptive presentation convention. Sparse groups remain present. Null sample SD for n=1 is undefined, not zero.
- metadata.json: conditions, definitions, source rights, dates and limitations.
- validation-note.md: the later hinting check and its limitations.
- checksums.sha256: SHA-256 of these public files. The private retained export has its own distinct hash.

## Reproduce descriptive statistics

Group measurements by exact codepoints and use canvas_width_px without rounding or remeasurement. Sort widths within each group. For quantile q, interpolate at h=(n-1)*q between adjacent sorted observations (Type 7). Sample SD uses n-1 when n>1. P90-P10 is descriptive spread, not a confidence interval.

The 12 records at 60 codepoints have minimum 581, P10 585.6, median 605.5, P90 629.4 and maximum 642 CSS px. Compare all 74 groups, not only the examples.

## Moltoyo measurements, compilation and documentation

The original measurements, compilation and original documentation produced by Moltoyo in this package are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0), only to the extent Moltoyo holds those rights.
https://creativecommons.org/licenses/by/4.0/

Attribute Moltoyo, name dataset version MTW-v1-2026, link to the study page and licence, and indicate if you made changes. This does not grant a new licence over GOV.UK source material, third-party source works or other third-party rights.

## Source material, attribution and rights

GOV.UK title metadata and source information remain subject to the Open Government Licence v3.0 and its stated exclusions. Contains public sector information licensed under the Open Government Licence v3.0.
https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
https://www.gov.uk/help/reuse-govuk-content

No official endorsement is implied. Per-source notice checks are not an exhaustive guarantee about third-party rights. No page bodies or font binaries are included. The underlying DejaVu font has its own licence; DejaVu changes being public domain does not put the whole font in the public domain: https://dejavu-fonts.github.io/License.html

## Limits

Guide-title strings are not asserted to be complete HTML title elements. The frame is one publisher, not a random web sample. Counts are codepoints, not a universal character definition. The historical hinting setting was not recorded; a later full-hinting check reproduces 23 checked strings, not all 852. Retained widths are whole pixels. Read validation-note.md. These data do not measure Google results, title rewriting, truncation frequency, rankings or CTR and do not establish universal character or pixel limits.

Citation: Moltoyo (2026). Same Character Count, Different Text Widths: 852 GOV.UK Guide Titles. MTW-v1-2026. https://moltoyo.com/research/title-width-study

# Verification and provenance — 6 November 2026

This record distinguishes checks of the public numerical files from verification of the original source passages. The frozen dataset versions and measurements have not changed.

## Text density: MTD-v1-2026

The five files in `data/` match the canonical [Moltoyo downloads](https://moltoyo.com/research/text-density-study) and the [Kaggle version 1 download](https://www.kaggle.com/datasets/stefanoperrelli/characters-per-word-in-english-250-text-samples/versions/1) byte for byte as checked on 6 November 2026. Their SHA-256 values are listed in `checksums.sha256`.

The numerical check covers 250 distinct sample IDs and source URLs, 50 samples in each category, 500 words per sample, five academic quotas of 10, and CSV/JSON equivalence. All sample locators span 500 inclusive token positions. Counts differ by exactly 499 spaces, as expected for 500 tokens joined with single spaces. Ratios and percentage errors agree with the recorded counts; the six published category/overall summaries reproduce.

Per-sample absolute percentage errors were retained to six decimal places. The frozen methodology's MAPE is the mean of those retained values, rounded for presentation. This can differ at a sub-millionth percentage-point scale from averaging newly calculated unrounded errors; the published two-decimal results agree.

### What remains conditional

The retained source-notice review is dated **5 October 2026**. It was inspected for this verification; all 250 source notices were not freshly rechecked on 6 November. Its classification was 187 verified notices and 63 conditional notices. “Verified” means the notice was checked, not that all rights were cleared.

| Source group | Retained open issue |
| --- | --- |
| Seven Wikinews records | Pre-cutover dates and associated licence corrections already disclosed in `data/metadata-errata.json`; retained in v1. An eighth date-only correction is also preserved. |
| Four Global Voices records | Partner republication/attribution questions; a general site footer does not resolve the originator's terms. |
| Two Wikipedia records | Imported-content attribution questions. Historical revisions were reconstructed from history at the recorded retrieval time; they were not recorded as acquisition snapshots. |
| Fifty Project Gutenberg records | Notices establish a United States status. Edition, translation, contributor and other-jurisdiction questions remain incomplete. |

The retained Gutenberg attribution metadata names 38 authors, with at most two works per named author, consistent with the stated quota. This does not resolve edition or translation rights.

Relevant source policies are [Wikinews copyright](https://en.wikinews.org/wiki/Wikinews:Copyright), [Global Voices republishing guidelines](https://globalvoices.org/about/global-voices-attribution-policy/) and [Project Gutenberg terms](https://www.gutenberg.org/policy/terms_of_use.html). Source-specific exceptions still matter.

The public package contains no original passages. Fingerprints and locators identify retained samples but cannot by themselves prove the source cleanup, eligible pool, hash-ranked selection or deterministic extraction. Those operations require the original private study records. This check did not rerun acquisition or extraction and does not claim end-to-end reproduction of the original corpus.

## Title width: MTW-v1-2026

The separate companion package in `title-width/MTW-v1-2026/` is copied from the approved [canonical title-width study](https://moltoyo.com/research/title-width-study). All eight files retain their published bytes. It is not an additional set of density samples and must not be appended to the text-density table.

The numerical check reproduces 852 distinct title records and all 74 exact-codepoint groups, using Type 7 interpolation and sample standard deviation. There are 46 groups with at least 10 titles, containing 782 titles. CSV/JSON agree, codepoint/UTF-16 counts reproduce, and the one documented path-only correction remains explicit.

The files preserve whole-pixel widths. Historical font hinting was not recorded; the later validation covered 23 strings and does not establish the historical configuration for all 852. No browser measurement was rerun in this verification. No source-page bodies or font binaries are included.

### Kaggle mirror verified — 7 November 2026

The [title-width Kaggle mirror](https://www.kaggle.com/datasets/stefanoperrelli/title-widths-852-english-gov-uk-guide-titles) is public as Kaggle version 1. Its unauthenticated download returned HTTP 200. All eight ZIP members match this repository's approved companion files byte for byte, including `checksums.sha256`; the seven listed checksums agree. See [download evidence](title-width/kaggle-verification-2026-11-07.json).

Only the mirror and this verification record were added. Dataset version MTW-v1-2026, original measurement/public-projection dates and all frozen files remain unchanged. Kaggle's single licence selector reads “Other (specified in description)”; the data card and unchanged files distinguish Moltoyo-owned CC BY 4.0 work from GOV.UK material under OGL v3.0 and its exclusions.

## Reproduce the file and arithmetic checks

From this repository with Python 3.10 or newer:

```sh
python3 verify_research.py --density data --title-width title-width/MTW-v1-2026
```

The script uses the Python standard library, checks the 13 frozen file hashes and numerical relationships, and makes no network requests. It is a new verification utility; it does not expose the private Lab code or corpus. The same check runs in this repository's CI.

Licence scope and the original citations remain unchanged: CC BY 4.0 covers Moltoyo-owned measurements, compilation and original documentation only. Third-party source rights are excluded; GOV.UK title metadata retains OGL v3.0 and its attribution.

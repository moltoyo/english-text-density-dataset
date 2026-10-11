# Characters per Word in English: 250 Text Samples

This dataset measures the average number of characters per word in English text, including spaces, and tests the familiar six-characters-per-word estimate. It contains **250 samples of 500 words each**, covering 125,000 words across five text types.

The corpus average is **6.33 characters per word including spaces**. This is a result for these samples, not a universal conversion factor for English.

[Original study and methodology](https://moltoyo.com/research/text-density-study) · [Kaggle dataset](https://www.kaggle.com/datasets/stefanoperrelli/characters-per-word-in-english-250-text-samples)

## Average characters per word by text type

| Text type | Samples | Characters per word, including spaces | Six-character estimate: mean absolute percentage error |
|---|---:|---:|---:|
| News | 50 | 6.30 | 6.41% |
| General informational | 50 | 6.33 | 6.75% |
| Academic | 50 | 6.73 | 10.67% |
| Technical and instructional | 50 | 6.76 | 12.41% |
| Classic fiction | 50 | 5.53 | 8.92% |
| Overall | 250 | 6.33 | 9.03% |

For a 500-word sample, the six-character rule predicts 3,000 characters. Each sample's absolute percentage error is `100 × abs(actual − 3,000) / actual`. The table reports the average of those errors, not a maximum error or a confidence interval.

## Download the data

| File | Contents |
|---|---|
| [measurements.csv](data/measurements.csv) | Primary table: 250 rows and 11 columns. |
| [measurements.json](data/measurements.json) | The same records under the `rows` key, with numeric JSON values. |
| [sources.json](data/sources.json) | 250 source links under the `sources` key. |
| [methodology.json](data/methodology.json) | Sampling procedure, definitions, final source mix, results and review notes. |
| [metadata-errata.json](data/metadata-errata.json) | Documented source-date and licence corrections. |

The five files are copies of the published MTD-v1-2026 downloads. They contain measurements and metadata only, with no original passages, full texts, abstracts, images or PDFs.

## How to use the measurements

Use the CSV to compare text density across categories, plot sample-level distributions or evaluate alternative word-to-character estimates. The JSON contains the same measurements; do not combine the formats as separate observations.

Characters per word **including spaces** differs from average word length excluding spaces. To calculate the latter under this study's definitions, divide `characters_without_whitespace` by `moltoyo_words`.

The dataset is suitable for exploratory numerical analysis. It does not contain a text corpus for language-model training or passage-level text classification.

## Sampling and counting definitions

Non-prose content was removed and whitespace collapsed to single spaces before sampling. Each eligible document had at least 750 cleaned words. Selection used category quotas, a fixed seed and hash-based ranking; each sample is a contiguous passage selected at a deterministic starting token. The full procedure is in [methodology.json](data/methodology.json).

A word is a whitespace-separated token. Characters are Unicode code points, not bytes or user-perceived characters. Start and end locators refer to tokens in the cleaned source document, not character offsets; the end is inclusive.

## Field dictionary

| Column | Definition |
|---|---|
| `public_sample_id` | Stable sample identifier; joins measurements to the source register. |
| `category` | Text type: news, general_informational, academic, technical_instructional or classic_fiction. |
| `subdiscipline` | Academic subject group; blank for other categories. |
| `moltoyo_words` | Whitespace-separated tokens under the study definition; always 500. |
| `characters_with_spaces` | Unicode code points in the normalized sample, including spaces. |
| `characters_without_whitespace` | Unicode code points excluding whitespace. |
| `characters_per_moltoyo_word_with_spaces` | characters_with_spaces / moltoyo_words; includes spaces. |
| `absolute_percentage_error_vs_6_rule` | 100 * abs(characters_with_spaces - 3000) / characters_with_spaces; percentage units. |
| `sample_sha256` | SHA-256 of the normalized sample; does not establish rights. |
| `sample_start_locator` | Zero-based starting token index in the normalized source document. |
| `sample_end_locator` | Zero-based ending token index, inclusive; start + 499. |

## Source documents

News samples come from Wikinews and Global Voices. General informational writing comes from Wikipedia, GOV.UK and the European Commission. Academic and most technical samples were sourced through Europe PMC; the remaining technical samples come from GOV.UK. Classic fiction comes from Project Gutenberg, with no more than two works per author.

Consult [sources.json](data/sources.json) for document URLs. Source works retain their respective rights and licences; their inclusion in the analysis does not grant rights to redistribute their text.

## Limitations and metadata corrections

- The corpus is balanced across categories, not representative of all English writing.
- The 750-word minimum favours long-form documents; classic fiction does not represent all contemporary fiction.
- Academic and technical sources lean heavily on scientific publications.
- No confidence intervals are reported.
- Moltoyo's live tools use different counting rules following the October 2026 update.
- Eight Wikinews publication dates require correction, including seven associated licence corrections. Those seven documents also fall outside the original date requirement. They remain in v1 with deviations documented in [metadata-errata.json](data/metadata-errata.json). Measurements are unchanged. Other source rights and attribution checks remain open.

## Licence and citation

Original measurements, compilation and original documentation owned by Moltoyo are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Third-party source works and rights are excluded. See [LICENSE.md](LICENSE.md) for scope and attribution.

> Moltoyo. (2026). Moltoyo Text Density Study, MTD-v1-2026. https://moltoyo.com/research/text-density-study

Data version: **MTD-v1-2026**, dated 26 September 2026. Original study page first published 5 October 2026. This repository distributes that version; it is not a new set of measurements.

For practical estimates, see the [words and characters guide](https://moltoyo.com/guides/how-many-characters-is). For your own text, use the [Character Counter](https://moltoyo.com/character-counter) or [Word Counter](https://moltoyo.com/word-counter), noting the definition differences above.

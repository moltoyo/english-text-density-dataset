# Measurement validation note — 30 October 2026

All retained MTW-v1-2026 Canvas and DOM widths are whole CSS-pixel values. The unchanged runner reads Canvas TextMetrics.width and an unwrapped DOM width without explicitly rounding those raw values. The historical runs did not record the system font-hinting configuration.

A later check used the same recorded Chromium version (141.0.7390.37), DejaVu Sans Book 2.37 font file (SHA-256 58568c88a01b80dfc056daca3eeafd434a0380df1a48dda53f0de0d716109bbd), 20 px size and unchanged runner. The current light-hinting environment produced fractional widths. Enabling full hinting reproduced the retained widths for 10 pilot strings and 13 strings from the final batch exactly; the 13-row CSV was byte-identical. Each runner invocation used two independent browser launches. Sixteen additional synthetic control strings were also checked.

This demonstrates a configuration capable of reproducing 23 checked strings. It strongly supports font hinting as an explanation, but cannot prove which configuration was used historically or validate every retained measurement against another environment. The current kernel was 6.12.114; retained batch records were 6.12.111. In the 10 pilot strings, light-hinting versus retained widths differed by approximately -2.57 to +1.96 px. That observation is not an error bound for the 852-title corpus.

The original 852 retained measurements, frozen protocol and raw results were not changed or recollected. These are descriptive, environment-specific advance widths. Internal repeatability and agreement between Canvas and DOM do not establish subpixel precision, cross-platform accuracy or Google search-result behavior. No whole-corpus comparison under a newly specified hinting configuration was performed.

Moltoyo's original validation documentation is shared under CC BY 4.0, for rights held by Moltoyo: https://creativecommons.org/licenses/by/4.0/ . Source material and third-party rights remain separately governed as described in README.md.

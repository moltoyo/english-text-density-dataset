"""Reproduce Moltoyo's published numerical tables without collecting source text.

Python standard library only. Checks exported measurements, not original passage
extraction, source rights, historical rendering or a new measurement run.
"""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import statistics


# Frozen public releases: change only for an explicitly reviewed new projection.
EXPECTED_HASHES = {
    "MTD-v1-2026": {
        "measurements.csv": "8a76ff940ca4d9ffebcaf9cd816c7d6db9837fbc865e3bb20510277995695372",
        "measurements.json": "63cedb50d6e2c263712d4644addfb0a21bc276866daccfcb59489d71f41ce638",
        "metadata-errata.json": "6dbd03a04ff693bf505a800db4f8cdda9d73938195878a8a48d0c1fe45d52a10",
        "methodology.json": "834b81c4acf8a7f8fcb48481acc9291298179787901103875ad304d0b637003b",
        "sources.json": "5195dba4183ee11fd423b3607e76eb0de0b82fb992d2969c5e7b6bdd4e6f5342"
    },
    "MTW-v1-2026": {
        "README.md": "2f5c7d9d97dd834741c94b345f6e720f6b1fc0ba93e992cd6d539db4e6b0a609",
        "by-length.csv": "4ea0a08a54985072d51b8e25cb580649e99e4f6472b557a451465b36b0d3596e",
        "by-length.json": "d46a5e289a60bdf61eb09f035cf1f50963e405c6991f4b3a8830240d25831a62",
        "checksums.sha256": "dd787d019900bf0fe68c998a04ba0a59ddbe978f7ebb3886f09b9a856ccf16d4",
        "measurements.csv": "38f1e2bf1e28bf7eed73609099202a0f93899fce99a976bc5c12d5ec9146e234",
        "measurements.json": "01ae4f28e9fe669950d1de4258edc1e264f42156377f0d710df9d0f2b2a50c6c",
        "metadata.json": "b27f71d1424e61e42cea3124be8f62fa3bb56b9865f7e8eb41cb03987144b7e3",
        "validation-note.md": "c43966e7e650e524d7aa4ef9086664380581256aa4307cb8b42335a963aee4b0"
    }
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def close(actual, expected, tolerance=1e-10):
    return math.isfinite(actual) and math.isclose(actual, expected, rel_tol=0, abs_tol=tolerance)


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def hashes(directory, version):
    for name, expected in EXPECTED_HASHES[version].items():
        actual = hashlib.sha256((directory / name).read_bytes()).hexdigest()
        require(actual == expected, f"Frozen file differs: {version}/{name}")


def csv_matches(path, rows):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == list(rows[0]), f"CSV fields differ: {path.name}")
        records = list(reader)
    require(len(records) == len(rows), f"CSV row count differs: {path.name}")
    for index, (expected, actual) in enumerate(zip(rows, records)):
        for key, value in expected.items():
            text = actual[key]
            if isinstance(value, bool):
                same = text.lower() == str(value).lower()
            elif value is None:
                same = text == ""
            elif isinstance(value, (int, float)):
                same = close(float(text), value)
            else:
                same = text == value
            require(same, f"CSV/JSON mismatch: {path.name}, row {index + 1}, {key}")


def density(directory):
    hashes(directory, "MTD-v1-2026")
    measurements = load(directory / "measurements.json")
    sources = load(directory / "sources.json")
    methodology = load(directory / "methodology.json")
    errata = load(directory / "metadata-errata.json")
    rows = measurements["rows"]
    require(measurements["row_count"] == len(rows) == 250, "Expected 250 density samples")
    identifiers = {row["public_sample_id"] for row in rows}
    require(len(identifiers) == 250, "Density sample IDs must be unique")
    require(sources["row_count"] == len(sources["sources"]) == 250, "Expected 250 sources")
    require(identifiers == {row["sample_id"] for row in sources["sources"]}, "Source join differs")
    require(len({row["url"] for row in sources["sources"]}) == 250, "Source URLs must be unique")
    require(len({row["sample_sha256"] for row in rows}) == 250, "Sample fingerprints repeat")
    for row in rows:
        require(row["moltoyo_words"] == 500, "Density sample word count differs")
        require(row["characters_with_spaces"] - row["characters_without_whitespace"] == 499,
                "Expected 499 single-space separators")
        require(row["sample_start_locator"] >= 0 and
                row["sample_end_locator"] == row["sample_start_locator"] + 499,
                "Inclusive density sample locators differ")
        require(re.fullmatch(r"[0-9a-f]{64}", row["sample_sha256"]), "Invalid sample fingerprint")
        require(close(row["characters_per_moltoyo_word_with_spaces"], row["characters_with_spaces"] / 500),
                "Per-sample density ratio differs")
        expected_error = 100 * abs(row["characters_with_spaces"] - 3000) / row["characters_with_spaces"]
        require(close(row["absolute_percentage_error_vs_6_rule"], expected_error, 0.00000051),
                "Per-sample percentage error differs")
    csv_matches(directory / "measurements.csv", rows)
    results = {}
    for name, stored in methodology["results"].items():
        selected = [row for row in rows if name == "overall" or row["category"] == name]
        require(len(selected) == stored["n"] == (250 if name == "overall" else 50),
                f"Density category quota differs: {name}")
        ratio = statistics.mean(row["characters_with_spaces"] / 500 for row in selected)
        # The frozen export averages the retained six-decimal row errors;
        # each row was checked against its unrounded formula above.
        mape = statistics.mean(row["absolute_percentage_error_vs_6_rule"] for row in selected)
        require(close(stored["mean_chars_per_word"], ratio, 0.00000051) and
                close(stored["mape_6_rule"], mape, 0.00000051), f"Density result differs: {name}")
        results[name] = {"n": len(selected), "mean_chars_per_word": ratio, "mape_6_rule": mape}
    academic = [row for row in rows if row["category"] == "academic"]
    subjects = {row["subdiscipline"] for row in academic}
    require(len(subjects) == 5 and all(sum(row["subdiscipline"] == s for row in academic) == 10
                                     for s in subjects), "Academic quotas differ")
    require(errata["row_count"] == len(errata["rows"]) == 8, "Expected eight preserved errata")
    require(all(row["sample_id"] in identifiers for row in errata["rows"]), "Erratum has no sample")
    require(sum(row["corrected"].get("license") == "CC BY 2.5" for row in errata["rows"]) == 7,
            "Expected seven preserved Wikinews licence corrections")
    return {"samples": len(rows), "total_words": sum(row["moltoyo_words"] for row in rows),
            "sources": len(sources["sources"]), "results": results}


def percentile(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    low = math.floor(position)
    high = math.ceil(position)
    return ordered[low] + (position - low) * (ordered[high] - ordered[low])


def title_width(directory, projection=None):
    hashes(directory, "MTW-v1-2026")
    rows = load(directory / "measurements.json")["measurements"]
    groups = load(directory / "by-length.json")
    metadata = load(directory / "metadata.json")
    require(len(rows) == metadata["analysed_titles"] == 852, "Expected 852 titles")
    require(len({row["source_id"] for row in rows}) == 852 and
            len({row["title"] for row in rows}) == 852, "Repeated title or source ID")
    require(metadata["frame_records"] - metadata["excluded_records"] == 852,
            "Frame/exclusion arithmetic differs")
    corrected = []
    for row in rows:
        require(len(row["title"]) == row["codepoints"] and
                len(row["title"].encode("utf-16-le")) // 2 == row["utf16_units"], "Title counts differ")
        require(row["canvas_width_px"] == row["dom_width_px"] > 0 and
                float(row["canvas_width_px"]).is_integer(), "Retained original widths differ")
        require(row["source_url"] == "https://www.gov.uk" + row["source_id"], "Source URL differs")
        if row["source_id_corrected"]:
            corrected.append(row)
        else:
            require(row["source_id"] == row["recorded_source_id"], "Unmarked source-path correction")
    require(len(corrected) == 1 and corrected[0]["recorded_source_id"] == "/expenses-benefits-third-party-awards"
            and corrected[0]["source_id"] == "/expenses-and-benefits-third-party-awards",
            "Documented path-only correction differs")
    require(len(groups) == metadata["length_groups"] == 74, "Expected 74 exact-length groups")
    require({g["codepoints"] for g in groups} == {r["codepoints"] for r in rows}, "Group membership differs")
    for group in groups:
        widths = [row["canvas_width_px"] for row in rows if row["codepoints"] == group["codepoints"]]
        p10, p90 = percentile(widths, .1), percentile(widths, .9)
        expected = {"n": len(widths), "primary_stratum": len(widths) >= 10,
                    "min_px": min(widths), "p10_px": p10, "median_px": percentile(widths, .5),
                    "p90_px": p90, "max_px": max(widths),
                    "sample_sd_px": statistics.stdev(widths) if len(widths) > 1 else None,
                    "p90_minus_p10_px": p90 - p10, "p90_div_p10": p90 / p10}
        for field, value in expected.items():
            actual = group[field]
            same = actual == value if isinstance(value, bool) or value is None else close(actual, value)
            require(same, f"Title-width statistic differs: {group['codepoints']}, {field}")
    require(sum(g["n"] for g in groups) == 852, "Group record counts differ")
    require(sum(g["primary_stratum"] for g in groups) == metadata["groups_with_n_at_least_10"] == 46,
            "Primary group count differs")
    require(sum(g["n"] for g in groups if g["primary_stratum"]) == metadata["titles_in_those_groups"] == 782,
            "Primary title count differs")
    csv_matches(directory / "measurements.csv", rows)
    csv_matches(directory / "by-length.csv", groups)
    if projection is not None:
        require(load(projection)["strata"] == groups, "Website's displayed groups differ from downloads")
    return {"titles": len(rows), "length_groups": len(groups), "primary_groups": 46,
            "primary_titles": 782, "path_only_corrections": 1,
            "historical_font_hinting": metadata["measurement"]["historical_font_hinting"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--density", type=Path)
    parser.add_argument("--title-width", type=Path)
    parser.add_argument("--projection", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    require(args.density or args.title_width, "Select at least one published dataset")
    require(not args.projection or args.title_width, "Projection requires the title-width dataset")
    result = {"status": "passed", "scope": "Frozen files and numerical tables only; no text collection or remeasurement."}
    try:
        if args.density:
            result["MTD-v1-2026"] = density(args.density)
        if args.title_width:
            result["MTW-v1-2026"] = title_width(args.title_width, args.projection)
    except (ValueError, KeyError, OSError) as error:
        result.update(status="failed", error=str(error))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

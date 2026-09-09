# SPDX-License-Identifier: GPL-3.0-only
"""Redraw all visits in the requested original four-panel PNG format.

Uses the previously validated NPZ measurements; performs no new image reduction.
All finite accepted measurements are included, with no percentile clipping.
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter
import numpy as np


plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 12, "axes.labelsize": 12,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    "axes.linewidth": 0.8, "savefig.facecolor": "white",
    "axes.spines.top": True, "axes.spines.right": True,
})


def load(root, entry):
    stem = f"{entry['field']}_{entry['band']}_{entry['visit']}"
    with np.load(root / "measurements" / (stem + ".npz")) as archive:
        data = {k: archive[k] for k in archive.files}
    data["ellip"] = np.hypot(data["e1"], data["e2"])
    data["good_fit"] = np.isfinite(data["fwhm_pix"]) & np.isin(data["fit_status"], [1, 2, 3, 4])
    return data


def bounds(values):
    values = values[np.isfinite(values)]
    lo, hi = float(values.min()), float(values.max())
    pad = (hi - lo) * 0.045
    return lo - pad, hi + pad


def render(entry, data, xy_limits, target):
    visit = entry["visit"]
    width, panel_width, hist_height = 11.8, 4.15, 3.2
    xspan = xy_limits["ra"][1] - xy_limits["ra"][0]
    yspan = xy_limits["dec"][1] - xy_limits["dec"][0]
    # FRB retains the previous square panel's physical dimensions while its
    # declination range is zoomed to 58.8--60.0 degrees at the user's request.
    map_height = panel_width if entry["field"] == "FRB" else panel_width * yspan / xspan
    hist_bottom, map_bottom = 0.57, 0.57 + hist_height + 0.95
    height = map_bottom + map_height + 0.40
    fig = plt.figure(figsize=(width, height), dpi=240, facecolor="white")
    lefts = [0.78, 6.5]
    axes = []
    for bottom, h in [(map_bottom, map_height), (hist_bottom, hist_height)]:
        for left in lefts:
            axes.append(fig.add_axes([left / width, bottom / height,
                                      panel_width / width, h / height]))
    titles = [f"v{visit}: 2D Moffat FWHM [pix]",
              f"v{visit}: SDSS 2nd-moment e",
              f"v{visit}: 2D Moffat FWHM distribution",
              f"v{visit}: SDSS 2nd-moment e distribution"]
    coord = np.isfinite(data["ra"]) & np.isfinite(data["dec"])
    valid_e = np.isfinite(data["ellip"])
    for i, (key, use, median_key, precision) in enumerate([
        ("fwhm_pix", data["good_fit"], "fwhm_pix_median", 1),
        ("ellip", valid_e, "ellipticity_median", 2),
    ]):
        ax = axes[i]
        use = use & coord
        # The legacy plots use viridis at low alpha, yielding the blue-green
        # pastel color bar in the supplied reference. Both maps use it here.
        scatter = ax.scatter(data["ra"][use], data["dec"][use],
                             c=data[key][use], s=5, alpha=0.2,
                             cmap="viridis", edgecolors="none")
        ax.set(xlim=xy_limits["ra"], ylim=xy_limits["dec"],
               xlabel="RA [deg]", ylabel="DEC [deg]")
        ax.set_aspect("auto" if entry["field"] == "FRB" else "equal", adjustable="box")
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
        for axis in [ax.xaxis, ax.yaxis]:
            formatter = ScalarFormatter(useOffset=False)
            formatter.set_scientific(False)
            axis.set_major_formatter(formatter)
        cax = fig.add_axes([(lefts[i] + panel_width + 0.16) / width,
                            map_bottom / height, 0.17 / width,
                            map_height / height])
        colorbar = fig.colorbar(scatter, cax=cax)
        colorbar.locator = MaxNLocator(nbins=6)
        colorbar.update_ticks()
        for detector in entry["detectors"]:
            within = (data["ccd"] == detector["ccd"]) & coord
            if not within.any():
                continue
            x = (data["ra"][within].min() + data["ra"][within].max()) / 2
            y = (data["dec"][within].min() + data["dec"][within].max()) / 2
            median = detector[median_key]
            ax.text(x, y, f"CCD{detector['ccd']:02d}\nmed{median:.{precision}f}",
                    ha="center", va="center", fontsize=6.4,
                    fontweight="bold", linespacing=1.0, zorder=3)
    for ax, key, use, xlabel in [
        (axes[2], "fwhm_arcsec", data["good_fit"], "FWHM [arcsec]"),
        (axes[3], "ellip", valid_e, "ellip"),
    ]:
        values = data[key][use]
        counts, _, _ = ax.hist(values, bins=50, histtype="step",
                               color="#1f77b4", linewidth=1.15)
        assert int(counts.sum()) == len(values), "Histogram lost measurements"
        ax.set_xlabel(xlabel)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
        ax.margins(x=0.05)
        ax.set_ylim(bottom=0)
        # Deliberately no fill, median line, legend, or statistics annotation.
    for letter, ax, title in zip("abcd", axes, titles):
        ax.set_title(title, pad=8)
        position = ax.get_position()
        fig.text(position.x0 - 0.064, position.y1 + 0.008,
                 f"({letter})", fontsize=18, ha="left", va="bottom")
    fig.canvas.draw()
    for ax in axes[:2]:
        origin = ax.transData.transform((0, 0))
        unit_x = ax.transData.transform((1, 0)) - origin
        unit_y = ax.transData.transform((0, 1)) - origin
        if entry["field"] == "FRB":
            assert np.allclose(ax.get_ylim(), [58.8, 60.0], rtol=0, atol=1e-12)
            assert np.isclose(ax.bbox.width, ax.bbox.height, rtol=1e-10)
        else:
            assert np.isclose(np.linalg.norm(unit_x), np.linalg.norm(unit_y), rtol=1e-10)
    renderer = fig.canvas.get_renderer()
    for artist in [*fig.texts, *(ax.title for ax in axes)]:
        box = artist.get_window_extent(renderer)
        assert box.x0 >= 0 and box.x1 <= fig.bbox.width, "Clipped panel title/letter"
        assert box.y0 >= 0 and box.y1 <= fig.bbox.height, "Clipped panel title/letter"
    assert fig._suptitle is None and fig._supxlabel is None
    fig.savefig(target, dpi=240, facecolor="white", transparent=False)
    plt.close(fig)
    return {"field": entry["field"], "band": entry["band"], "visit": visit,
            "file": target.name, "titles": titles,
            "map_aspect": "auto" if entry["field"] == "FRB" else "equal",
            "cmap": "viridis", "scatter_alpha": 0.2, "hist_bins": 50,
            "n_fwhm": int(data["good_fit"].sum()), "n_ellip": int(valid_e.sum()),
            "n_fwhm_outside_histogram": 0, "n_ellip_outside_histogram": 0,
            "map_limits": xy_limits}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("qc_data"))
    parser.add_argument("--output", type=Path, default=Path("figures/qc_original_style"))
    parser.add_argument("--visit", type=int, nargs="*")
    parser.add_argument("--field", choices=["ClusterRot", "FRB"])
    args = parser.parse_args()
    manifest = json.loads((args.data / "qc_manifest.json").read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)
    plots = []
    for field in ["ClusterRot", "FRB"]:
        if args.field and field != args.field:
            continue
        entries = [v for v in manifest["visits"] if v["field"] == field]
        all_data = [load(args.data, v) for v in entries]
        xy_limits = {key: bounds(np.concatenate([d[key] for d in all_data]))
                     for key in ["ra", "dec"]}
        if field == "FRB":
            # Preserve the previous horizontal range exactly, but expand the
            # plotted vertical scale inside the same square physical panel.
            span = max(hi - lo for lo, hi in xy_limits.values())
            xy_limits = {key: ((lo + hi - span) / 2, (lo + hi + span) / 2)
                         for key, (lo, hi) in xy_limits.items()}
            xy_limits["dec"] = (58.8, 60.0)
        for entry, data in zip(entries, all_data):
            if args.visit and entry["visit"] not in args.visit:
                continue
            token = "cluster" if field == "ClusterRot" else "FRB"
            target = args.output / f"fig-qc_{token}_{entry['visit']}.png"
            plots.append(render(entry, data, xy_limits, target))
            print(f"Saved {target}", flush=True)
    # Keep provenance outside the PNG directory and leave the previous manifest
    # and the previous publication/PDF renderer untouched.
    if not args.visit:
        metadata_path = args.data / "original_style_plot_manifest.json"
        if args.field and metadata_path.exists():
            previous = json.loads(metadata_path.read_text(encoding="utf-8"))
            updates = {plot["file"]: plot for plot in plots}
            plots_for_metadata = [updates.pop(plot["file"], plot) for plot in previous]
            plots_for_metadata.extend(updates.values())
        else:
            plots_for_metadata = plots
        metadata_path.write_text(json.dumps(plots_for_metadata, indent=2), encoding="utf-8")
    print(f"COMPLETE: {len(plots)} PNG files", flush=True)


if __name__ == "__main__":
    main()

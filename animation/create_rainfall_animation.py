import cv2
import matplotlib.patches as patches
from matplotlib.colors import Normalize, LinearSegmentedColormap
import matplotlib.pyplot as plt
import os
import re
from glob import glob
import numpy as np
from osgeo import gdal


def _natural_key(s: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', os.path.basename(s))]


def create_precip_video(
    input_dir="temp/maps",
    output_path="temp/maps/rainfall_animation.mp4",
    resolution=(1920, 1080),
    fps=1,
    cmap=None,                 # if None, use white->dark-blue colormap created below
    vmin=None,
    vmax=None,
    fig_padding=0.08,
    map_area_frac=0.9,
    title="Precipitation (mm)",
    border=True,               # activate/deactivate border
    border_color="black",      # border color
    border_width=2.0           # border width (px in figure space)
):
    """
    Read .asc rasters from input_dir and create an MP4 video with a fixed
    resolution. Raster images are centered and a global color scale is applied
    across all frames. The default colormap is white->dark-blue and a border
    may be drawn around raster pixels.
    """
    # Colormap: white->dark-blue
    if cmap is None:
        cmap = LinearSegmentedColormap.from_list(
            "white_to_darkblue",
            ["#ffffff", "#b3cde3", "#005b96", "#011f4b"]
        )

    width_px, height_px = resolution
    dpi = 100
    fig_w_in = width_px / dpi
    fig_h_in = height_px / dpi

    # Order files
    files = sorted(glob(os.path.join(input_dir, "*.asc")), key=_natural_key)
    if not files:
        raise FileNotFoundError(f"Nenhum .asc encontrado em: {input_dir}")

    # Global Min/max values
    global_min, global_max = np.inf, -np.inf
    for f in files:
        ds = gdal.Open(f)
        if ds is None:
            continue
        band = ds.GetRasterBand(1)
        arr = band.ReadAsArray().astype(float)
        # nodata handling
        nd = band.GetNoDataValue()
        if nd is not None:
            arr[arr == nd] = np.nan
        # compute stats ignoring NaN
        if np.isnan(arr).all():
            continue
        data_min = np.nanmin(arr)
        data_max = np.nanmax(arr)
        if np.isfinite(data_min):
            global_min = min(global_min, float(data_min))
        if np.isfinite(data_max):
            global_max = max(global_max, float(data_max))

    if vmin is None:
        vmin = global_min if np.isfinite(global_min) else 0.0
    if vmax is None:
        vmax = global_max if np.isfinite(global_max) else 1.0

    if not (np.isfinite(vmin) and np.isfinite(vmax)) or vmin == vmax:
        raise ValueError("Could not determine valid global vmin/vmax values.")

    norm = Normalize(vmin=vmin, vmax=vmax)

    # Video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width_px, height_px))
    if not writer.isOpened():
        raise RuntimeError(
            "Failed to open VideoWriter. Check codecs and output path.")

    # Figura base
    plt.ioff()
    fig = plt.figure(figsize=(fig_w_in, fig_h_in), dpi=dpi)

    left = fig_padding
    right = 1 - fig_padding
    bottom = fig_padding
    top = 1 - fig_padding

    cbar_frac = 0.05
    cbar_pad = 0.02
    title_height = 0.07

    map_left = left
    map_right = right - cbar_frac - cbar_pad
    map_bottom = bottom
    map_top = top - title_height

    map_w = (map_right - map_left) * map_area_frac
    map_h = (map_top - map_bottom) * map_area_frac
    map_x = map_left + ((map_right - map_left) - map_w) / 2
    map_y = map_bottom + ((map_top - map_bottom) - map_h) / 2

    ax = fig.add_axes([map_x, map_y, map_w, map_h])
    ax.set_axis_off()

    ax_title = fig.add_axes(
        [left, top - title_height, (right - left), title_height])
    ax_title.set_axis_off()

    ax_cbar = fig.add_axes([map_right + cbar_pad, map_y, cbar_frac, map_h])

    # Loop through files to generate frames
    try:
        for f in files:
            ds = gdal.Open(f)
            if ds is None:
                continue
            band = ds.GetRasterBand(1)
            data = band.ReadAsArray().astype(float)
            nd = band.GetNoDataValue()
            if nd is not None:
                data[data == nd] = np.nan
            nrows, ncols = data.shape
            # Clear axes
            ax.clear()
            ax.set_axis_off()
            ax_title.clear()
            ax_title.set_axis_off()
            ax_cbar.clear()

            # Plot main image
            im = ax.imshow(
                data,
                cmap=cmap,
                norm=norm,
                interpolation="nearest",
                aspect="equal",
                origin="upper"   # rows counting start from 0
            )

            # frame-aligned border:
            # we use (-0.5, -0.5) to (ncols-0.5, nrows-0.5) to match the pixel edges
            if border:
                rect = patches.Rectangle(
                    (-0.5, -0.5),
                    ncols, nrows,
                    linewidth=border_width,
                    edgecolor=border_color,
                    facecolor='none',
                    zorder=10
                )
                ax.add_patch(rect)

            # Title
            frame_title = os.path.splitext(os.path.basename(f))[0]
            ax_title.text(
                0.5, 0.5,
                f"{frame_title} min",
                ha="center", va="center",
                fontsize=16, fontweight="bold"
            )

            # Global colorbar
            cbar = fig.colorbar(im, cax=ax_cbar)
            cbar.set_label("mm", rotation=90)

            # Render to frame
            fig.canvas.draw()

            # Get actual canvas size (width, height)
            try:
                canvas_w, canvas_h = fig.canvas.get_width_height()
            except Exception:
                # fallback to expected resolution
                canvas_w, canvas_h = width_px, height_px

            # Try to obtain RGBA buffer; different backends expose different methods
            frame_rgb = None
            try:
                # Preferred modern API that returns RGBA bytes
                buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
                arr = buf.reshape((canvas_h, canvas_w, 4))
                frame_rgb = arr[:, :, :3]
            except Exception:
                try:
                    # Fallback: some backends expose ARGB ordering
                    buf = np.frombuffer(
                        fig.canvas.tostring_argb(), dtype=np.uint8)
                    arr = buf.reshape((canvas_h, canvas_w, 4))
                    # convert ARGB -> RGB by taking R,G,B channels
                    frame_rgb = arr[:, :, 1:4]
                except Exception:
                    # As last resort, try tostring_rgb (older backends)
                    try:
                        buf = np.frombuffer(
                            fig.canvas.tostring_rgb(), dtype=np.uint8)
                        arr = buf.reshape((canvas_h, canvas_w, 3))
                        frame_rgb = arr
                    except Exception as exc:
                        writer.release()
                        plt.close(fig)
                        raise RuntimeError(
                            f"Unable to obtain canvas pixel buffer: {exc}")

            # Ensure frame size matches requested resolution; resize if necessary
            if (canvas_w, canvas_h) != (width_px, height_px):
                frame_rgb = cv2.resize(
                    frame_rgb, (width_px, height_px), interpolation=cv2.INTER_AREA)

            # Convert RGB -> BGR for OpenCV and write
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            writer.write(frame_bgr)
    finally:
        writer.release()
        plt.close(fig)
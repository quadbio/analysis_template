# Dataset structure

-   `raw`: bytes as they arrived (instrument output, downloads). Never written by analysis.
-   `resources`: curated inputs that are not data: gene lists, marker tables, panel descriptions.
-   `processed`: objects code loads to do new work, as AnnData `.zarr` stores.
-   `results`: a notebook's own outputs, file names prefixed with the notebook's stem.

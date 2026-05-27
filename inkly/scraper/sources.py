from __future__ import annotations

# Curated list of trusted HPC documentation sources known to contain
# Gaussian-related content. Each entry has a URL to scrape and a label
# used to identify the source in stored snippets.
#
# These are all public-facing research computing documentation sites from
# universities and national labs. Adding a new source is as simple as
# appending an entry to this list.

GAUSSIAN_SOURCES = [
    {
        "label": "Harvard RC — Gaussian",
        "url": "https://docs.rc.fas.harvard.edu/kb/gaussian/",
    },
    {
        "label": "NERSC — Gaussian",
        "url": "https://docs.nersc.gov/applications/chemistry/gaussian/",
    },
    {
        "label": "Princeton RC — Gaussian",
        "url": "https://researchcomputing.princeton.edu/support/knowledge-base/gaussian",
    },
    {
        "label": "University of Michigan — Gaussian",
        "url": "https://arc-ts.umich.edu/software/gaussian/",
    },
    {
        "label": "Ohio Supercomputer Center — Gaussian",
        "url": "https://www.osc.edu/resources/available_software/software_list/gaussian",
    },
]

# Keywords used to decide whether a paragraph is relevant enough to keep.
# A passage must contain at least one of these (case-insensitive) to be retained.
GAUSSIAN_KEYWORDS = [
    "gaussian",
    "g09",
    "g16",
    "computational chemistry",
    "quantum chemistry",
    "slurm",
    "sbatch",
    "module load",
    "mem=",
    "nproc=",
    "%mem",
    "%nproc",
    "basis set",
    "dft",
    "density functional",
]

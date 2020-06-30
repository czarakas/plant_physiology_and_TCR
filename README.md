# plant_physiology_and_TCR

This repository contains code to reproduce the analysis in Zarakas et al. (2020), **"Plant Physiology Increases
the Magnitude and Spread of the Transient Climate Response to CO<sub>2</sub> in CMIP6 Earth System Models"** ([EarthArXiv Link](https://eartharxiv.org/emgxb/))

To run this code:
1. Edit the directory structure in plants_and_TCR/analysis_parameters/directory_information.py (lines 2-6) to reflect your working directory and where your data is stored
2. Generate data dictionary to use in analysis by running all cells in the Jupyter notebook replace_figures/Make_data_dictionaries.ipynb

The code in /plants_and_TCR/ performs all analysis, and notebooks in /replicate_figures/ uses that code to replicate the figures in the paper.

```bash
├── README.md
├── plants_and_TCR.yml
├── data/
├── docs/
├── plants_and_TCR/
│   ├── analysis_parameters
│   ├── analyze_data
│   ├── generate_figures
│   ├── make_data_dictionary
│   └── process_data
├── replicate_figures
│   ├── Figure_1.ipynb
```

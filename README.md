# Health Analysis

Over the past two years I've gathered a variety of information.  Some of this information is in totality of those two years, most isnt.
* A picture of every meal I've eaten
* A caption describing the contents of the meal
* My weight every morning
* Time and classification of my bowel movements
* Workouts at my weightlifting gym

This project is the initiative to
* digitize and clean all the collected data,
* analyse the data,
* build models to predict future behavior,
* streamline the extension of datasets,
* visualize the data and analysis,
* and report on what I've learned as a result of analysis.

## Data Pipeline

Raw data will be stored external to this repository.

1) Each data source is individually pulled into `cleaned` after being cleaned _individually_.
2) Additional data generated from `cleaned` data is placed into `extended`.
3) All relevant data in `cleaned` and `extended` is finally joined into `prepared`.

In `prepared` is all the data needed for modeling and visualization.

## Data Visualization

The goal is to make a dashboard.  I'm going to experiment with some new technology, maybe.

* tabler: a library that can be integrated into an html file to designing a dashboard
* apexcharts: a plugin for tabler that makes charts, similar to plotly

Unforunately these all are intended for integration into larger web frameworks.  I don't want to dive into that so I'm going to use the most basic templating engine: mustache.

* mustache: a dead simple templating engine...template + config => output

But to be extra difficult I want to still write in toml so

* yj: a converter for json/toml/yaml

I create a config in toml and a template file with preprogrammed charts.  But I guess they need data pulled from sqlite dont they?  Then there needs to be more preprocessing anyway, why don't I just use plotly and dash?  yeah, this might be too complicated

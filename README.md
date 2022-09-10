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

The raw data will be stored in a location on my machine outside of this repository.  The location of these raw data sources will be listed in the `data_sources` table in the `config.toml` file.  Each type of data will be pulled into a directory defined as `cleaned` after going through a transformation to simplify the data format and filter unnecessary data.  Then the data will be pulled into a directory defined as `prepared` which will contain the final form the data, after all cleaning and joining of different datasets.  Any intermediate output will also sit inside the `cleaned` directory.  Scripts that pull raw data into the `cleaned` directory will be stored in directory defined as `clean`.  Likewise for `prepared` the scripts will sit in `prepare`.

# Health Analysis

Since August of 2022 I've been recording information about my health.
* A picture of every meal I've eaten
* A caption describing the contents of the meal
* My weight every morning
* Time and classification of my bowel movements
* Workouts at my weightlifting gym

This project is the collection, transformation, and analysis of those datasets to understand my health better.

## Data Pipeline

Raw data will be stored external to this repository.

1) Each data source is pulled into `cleaned` after being cleaned _individually_, isolated from other data sources.
2) Additional data generated from `cleaned` data is placed into `extended`.
3) All relevant data in `cleaned` and `extended` is finally joined into `prepared`.

In `prepared` is all the data needed for modeling and visualization.

## Data Visualization

A dashboard is created using plotly/dash.

# Progress

This is a list of accomplishments and goals.

## Data Sources

These are existing data sources that need to be digitized or scraped, and cleaned.

- [x] My weight from scale
- [ ] Time weight was taken
- [x] Instagram posts of my food
- [ ] Full photos taken of my food
- [ ] Bowel movements
- [ ] Workouts at weightlifting gym

## Data Transformation

This is information that needs to be generated or calculated from existing data sources.

- [ ] Meals (photos of food taken within a time interval)
- [x] Interpolate weight values
- [x] Average weight across days
- [ ] Clean labels of instagram posts
- [ ] Food classification (desert, bread, meat, vegetables, etc)

## Data Modeling and Visualization

These are stated in the form of questions that I'd like to answer.  These could be answered using a model, a summary statistic, SQL query, or interactive visualization.  These are considered complete when integrated, in some way, into the dashboard.

- [ ] How did the number of meals I ate a certain day effect my weight?
- [ ] How did the type of food (meat, vegetable, dairy, etc.) effect my weight?
- [ ] How long did it take me, on average, to post an image to instagram after I took it?
- [ ] What were my most frequent times to eat?
- [ ] When did I fast?
- [ ] How did trips and vacations effect my eating habits and weight?

## Reporting and Blogging

It would be nice to summarize my experience collecting the data, as well as analysing it.  The best medium for me to do this is through my blog.

- [ ] My experience with Instagram for posting my meals
- [ ] Effects of fasting
- [ ] Creation of this project

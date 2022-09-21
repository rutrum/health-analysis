-- daily columns:
-- day_num: day number (from first day at 0)
-- date: formatted date
-- weight
-- total_posts: number of instagram posts

CREATE VIEW daily AS
SELECT 
  CAST((weight.date - min_timestamp) / 60 / 60 / 24 as INT) as day_num,
  COUNT(food_images.filename) AS total_images,
  date(weight.date, 'unixepoch') AS date,
  weight.weight AS weight,
  weight.interpolated AS interpolated_weight,
  weight.average AS average_weight
  --COUNT(post.id) AS total_posts
FROM weight

--LEFT JOIN post
--ON date(weight.date, 'unixepoch') = date(post.timestamp, 'unixepoch')

JOIN food_images
ON date(weight.date, 'unixepoch') = date(food_images.timestamp, 'unixepoch')

JOIN (SELECT min(unixepoch(date(date, 'unixepoch'))) as min_timestamp FROM weight)

GROUP BY date

-- working:
-- select date(timestamp, 'unixepoch') as D, count(filename), weight from food_images join weight on D = date(weight.date, 'unixepoch') GROUP BY D ORDER BY D;

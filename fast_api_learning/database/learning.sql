-- See all trips
SELECT *
FROM trips;


-- See all itinerary items
SELECT *
FROM itinerary_items;

SELECT id, destination, start_date, end_date
FROM trips
ORDER BY id;
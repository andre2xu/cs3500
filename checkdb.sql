SELECT * FROM growthreq;
DELETE FROM growthreq;

UPDATE growthreq
SET harvest_date = '2022-12-01'
WHERE plot_num = 0;
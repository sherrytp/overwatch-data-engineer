-- Creating a partition and cluster table
CREATE OR REPLACE TABLE `radiant-arcanum-413707.owl_data.match_stats_partitioned`
PARTITION BY DATE(start_time) AS
(SELECT * FROM `radiant-arcanum-413707.owl_data.match_stats`);


-- Impact of partition

-- Query from the dataset without partition
SELECT COUNT(*) FROM `radiant-arcanum-413707.owl_data.match_stats`
WHERE esports_match_id = '37224'

-- Query from the dataset with partition
SELECT COUNT(*) FROM `radiant-arcanum-413707.owl_data.match_stats_partitioned`
WHERE esports_match_id = '37224'

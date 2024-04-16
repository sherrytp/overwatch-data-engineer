-- Calculate total dmg by player (2_plot)

SELECT player_name, SUM(stat_amount) AS total_dmg
FROM `radiant-arcanum-413707.owl_data.match_stats`
WHERE stat_name = 'Hero Damage Done'
GROUP BY player_name
ORDER BY total_dmg DESC;

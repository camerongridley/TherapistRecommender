WITH gtx AS (
        SELECT gt.game_id
        , gt.team_score
        , te.team_id
        , te.team_name
        FROM games_teams gt
        JOIN teams te ON te.team_id = gt.team_id
        )
SELECT ga.game_id 
        , ga.game_name
        , ga.game_duration
        , g1.team_name, g1.team_score
        , g2.team_name, g2.team_score
FROM games ga
JOIN gtx g1 ON g1.game_id = ga.game_id
JOIN gtx g2 ON g2.game_id = ga.game_id
WHERE g1.team_id < g2.team_id
  ;





WITH lookup_joined_right_alias AS (
        SELECT lookup.game_id
        , lookup.team_score
        , te.team_id
        , te.team_name
        FROM games_teams gt
        JOIN teams te ON te.team_id = gt.team_id
        )
SELECT ga.game_id 
        , ga.game_name
        , ga.game_duration
        , g1.team_name, g1.team_score
        , g2.team_name, g2.team_score
FROM games ga
JOIN gtx g1 ON g1.game_id = ga.game_id
JOIN gtx g2 ON g2.game_id = ga.game_id
WHERE g1.team_id < g2.team_id
  ;
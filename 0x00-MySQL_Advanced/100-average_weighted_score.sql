-- Create a stored procedure named ComputeAverageWeightedScoreForUser
--       to compute and store the average weighted score for a given student.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id_param INT)
BEGIN
    -- Declare variables
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_weighted_score FLOAT;

    -- Calculate the total weighted score for the user
    SELECT SUM(c.score * p.weight)
    INTO total_weighted_score
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id_param;

    -- Calculate the total weight for the user
    SELECT SUM(p.weight)
    INTO total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id_param;

    -- Calculate the average weighted score
    IF total_weight > 0 THEN
        SET average_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    -- Update the user's average_score in the users table
    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = user_id_param;

END //

DELIMITER ;

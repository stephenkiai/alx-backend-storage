-- Task: Create a stored procedure named ComputeAverageWeightedScoreForUsers
--       to compute and store the average weighted score for all students.
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare variables
    DECLARE user_id_param INT;
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_weighted_score FLOAT;

    -- Declare cursor for all user IDs
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;

    -- Open cursor
    OPEN user_cursor;

    -- Loop through each user ID
    user_loop: LOOP
        -- Fetch the next user ID
        FETCH user_cursor INTO user_id_param;

        -- Exit loop if no more users
        IF user_id_param IS NULL THEN
            LEAVE user_loop;
        END IF;

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

    END LOOP;

    -- Close cursor
    CLOSE user_cursor;

END //

DELIMITER ;

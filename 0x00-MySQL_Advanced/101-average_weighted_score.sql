-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    JOIN (
        SELECT users.id, SUM(score * weight) / SUM(weight) AS weight_avg
        FROM users
        JOIN corrections ON users.id=corrections.user_id
        JOIN projects ON corrections.project_id=projects.id
        GROUP BY users.id
    ) AS collection ON users.id = collection.id
    SET users.average_score = collection.weight_avg;
END
$$
DELIMITER ;

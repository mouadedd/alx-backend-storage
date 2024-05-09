-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    user_id INT
)
BEGIN
    DECLARE weight_avg_score FLOAT;
    SET weight_avg_score = (SELECT SUM(score * weight) / SUM(weight)
                        FROM users
                        JOIN corrections ON users.id=Corrections.user_id
                        JOIN projects ON corrections.project_id=projects.id
                        WHERE users.id=user_id);
    UPDATE users SET average_score = weight_avg_score WHERE id=user_id;
END
$$
DELIMITER ;

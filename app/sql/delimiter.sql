
-- create the EnforceCourseLimit trigger
DELIMITER $$
CREATE TRIGGER EnforceCourseLimit
BEFORE INSERT ON StudentCourse
FOR EACH ROW
BEGIN
    DECLARE course_count INT;
    SELECT COUNT(*) INTO course_count FROM StudentCourse WHERE student_id = NEW.student_id;
    IF course_count >= 6 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in maximum number of courses';
    END IF;
    IF course_count < 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student must be enrolled in at least three courses';
    END IF;
END$$
DELIMITER ;
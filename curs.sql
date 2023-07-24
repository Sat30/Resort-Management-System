CREATE TABLE `Curbackup_foodItem` (
  
  `food_id` int(11) DEFAULT NULL,
  `food_name` varchar(30) DEFAULT NULL,
  `price` int(11) DEFAULT NULL
);

DELIMITER $$
CREATE PROCEDURE curs()
BEGIN
DECLARE done INT DEFAULT 0;
DECLARE foodid , price int(10);
DECLARE foodname VARCHAR(20);
DECLARE cur CURSOR FOR SELECT * FROM food_item;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
OPEN cur;
label: LOOP
FETCH cur INTO foodid ,  foodname , price;
INSERT INTO Curbackup_foodItem VALUES(foodid ,  foodname , price);
IF done = 1 THEN LEAVE label;
END IF;
END LOOP;
CLOSE cur;
END;$$
DELIMITER ;



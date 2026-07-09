CREATE DATABASE IF NOT EXISTS `youtube_analytics`;
USE `youtube_analytics`;

DROP TABLE IF EXISTS `trending_videos`;

CREATE TABLE `trending_videos` (
    `video_id` VARCHAR(50),
    `title` TEXT,
    `channel_title` VARCHAR(255),
    `category_id` INT,
    `publish_time` DATETIME,
    `trending_date` DATETIME,
    `views` BIGINT,
    `likes` BIGINT,
    `dislikes` BIGINT,
    `comment_count` BIGINT,
    `tags` TEXT,
    `comments_disabled` BOOLEAN,
    `ratings_disabled` BOOLEAN,
    `video_error_or_removed` BOOLEAN,
    `description` TEXT,
    `country` VARCHAR(10),
    `category` VARCHAR(100),
    `Engagement` DOUBLE,
    `Like_Ratio` DOUBLE,
    `Comment_Ratio` DOUBLE,
    `Video_Age` INT,
    `publish_day` VARCHAR(20),
    `publish_month` VARCHAR(20),
    `publish_hour` INT
);
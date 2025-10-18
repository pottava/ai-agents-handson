#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL
    CREATE TABLE visit_appointments (
        appointment_id          SERIAL PRIMARY KEY,                          -- Unique appointment ID
        customer_name           VARCHAR(255) NOT NULL,                       -- Customer's name
        customer_phone          VARCHAR(20) NOT NULL,                        -- Customer's phone number
        appointment_datetime    TIMESTAMP WITH TIME ZONE NOT NULL,           -- Scheduled date and time of the visit
        purpose                 VARCHAR(255) NOT NULL,                       -- Purpose of the visit (e.g., viewing, grooming)
        pet_id_of_interest      INTEGER,                                     -- ID of a specific pet of interest (can be null)
        status                  VARCHAR(50) NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'completed', 'canceled')) -- Status of the appointment
    );

    INSERT INTO visit_appointments (customer_name, customer_phone, appointment_datetime, purpose, pet_id_of_interest, status) VALUES
    ('稲垣 吾郎', '090-3333-4444', '2025-09-24 14:00:00 JST', 'ペットの見学', 121, 'scheduled'),
    ('草彅 剛', '090-4444-5555', '2025-09-27 10:30:00 JST', '購入相談', 122, 'scheduled'),
    ('香取 慎吾', '090-5555-6666', '2025-09-30 13:00:00 JST', 'ペットの見学', 115, 'scheduled'),
    ('長瀬 智也', '080-1234-5678', '2025-09-01 15:00:00 JST', 'グルーミング予約', 105, 'scheduled'),
    ('国分 太一', '080-2345-6789', '2025-10-01 11:00:00 JST', 'ペットの見学', 123, 'scheduled'),
    ('松岡 昌宏', '080-3456-7890', '2025-10-01 14:30:00 JST', '健康相談', NULL, 'scheduled'),
    ('城島 茂', '080-4567-8901', '2025-10-02 10:00:00 JST', 'ペットの見学', 124, 'scheduled'),
    ('堂本 光一', '070-1122-3344', '2025-10-02 13:30:00 JST', '購入相談', 125, 'scheduled'),
    ('岡田 准一', '090-6789-0123', '2025-10-03 15:00:00 JST', 'グルーミング予約', 111, 'scheduled'),
    ('坂本 昌行', '090-7890-1234', '2025-10-04 10:30:00 JST', 'ペットの見学', 127, 'scheduled'),
    ('長野 博', '090-8901-2345', '2025-10-04 14:00:00 JST', '健康相談', NULL, 'scheduled'),
    ('森田 剛', '080-5555-1111', '2025-10-05 16:00:00 JST', '購入相談', 129, 'scheduled'),
    ('三宅 健', '080-6666-2222', '2025-10-06 10:00:00 JST', 'ペットの見学', 130, 'scheduled'),
    ('木村 拓也', '090-1111-2222', '2025-09-19 10:00:00 JST', 'ペットの見学', 118, 'completed'),
    ('中居 正広', '090-2222-3333', '2025-09-20 11:30:00 JST', 'グルーミング相談', NULL, 'completed'),
    ('佐藤 健', '070-7777-3333', '2025-09-20 16:00:00 JST', 'ペットの見学', 117, 'completed'),
    ('鈴木 亮平', '070-8888-4444', '2025-09-23 11:00:00 JST', 'グルーミング予約', 102, 'completed'),
    ('高橋 一生', '070-9999-5555', '2025-09-20 16:00:00 JST', 'ペットの見学', 119, 'canceled'),
    ('堂本 剛', '070-2233-4455', '2025-10-03 11:00:00 JST', 'ペットの見学', 126, 'canceled'),
    ('井ノ原 快彦', '090-9012-3456', '2025-10-05 11:30:00 JST', 'ペットの見学', 128, 'canceled');
EOSQL

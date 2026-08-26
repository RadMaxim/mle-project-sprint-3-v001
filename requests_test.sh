#!/bin/bash

URL="http://localhost:1702/api/churn/?user_id=5"

for i in {1..1000}
do
    floor=$((RANDOM % 20 + 1))

    kitchen_area=$(awk -v min=5 -v max=30 'BEGIN{srand(); print min+rand()*(max-min)}')

    living_area=$(awk -v min=10 -v max=100 'BEGIN{srand(); print min+rand()*(max-min)}')

    rooms=$((RANDOM % 5))

    total_area=$(awk -v min=20 -v max=150 'BEGIN{srand(); print min+rand()*(max-min)}')

    build_year=$((RANDOM % 130 + 1900))

    building_type_int=$((RANDOM % 10 + 1))

    latitude=$(awk -v min=55.5 -v max=55.9 'BEGIN{srand(); print min+rand()*(max-min)}')

    longitude=$(awk -v min=37.3 -v max=37.9 'BEGIN{srand(); print min+rand()*(max-min)}')

    ceiling_height=$(awk -v min=2.0 -v max=4.0 'BEGIN{srand(); print min+rand()*(max-min)}')

    flats_count=$((RANDOM % 200 + 1))

    floors_total=$((RANDOM % 30 + 1))

    is_apartment=$([ $((RANDOM % 2)) -eq 0 ] && echo false || echo true)

    studio=$([ $((RANDOM % 2)) -eq 0 ] && echo false || echo true)

    has_elevator=$([ $((RANDOM % 2)) -eq 0 ] && echo false || echo true)

    echo "Request $i"

    curl -s -o /dev/null \
        -w "HTTP status: %{http_code}\n" \
        -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d "{
            \"floor\": $floor,
            \"kitchen_area\": $kitchen_area,
            \"living_area\": $living_area,
            \"rooms\": $rooms,
            \"is_apartment\": $is_apartment,
            \"studio\": $studio,
            \"total_area\": $total_area,
            \"build_year\": $build_year,
            \"building_type_int\": $building_type_int,
            \"latitude\": $latitude,
            \"longitude\": $longitude,
            \"ceiling_height\": $ceiling_height,
            \"flats_count\": $flats_count,
            \"floors_total\": $floors_total,
            \"has_elevator\": $has_elevator
        }" &
done

wait

echo "Load test completed."
//Game Info Table Creation
CREATE TABLE GameInfo (
    game_id UUID PRIMARY KEY,
    name TEXT,
    type TEXT,
    current_state TEXT,
    world_layout TEXT
);

//Game Object Table Creation
CREATE TABLE GameObject (
    game_id UUID,
    object_id TEXT,
    type TEXT,
    position_x INT,
    position_y INT,
    position_z INT,
    attributes MAP<TEXT, TEXT>,
    PRIMARY KEY (game_id, object_id)
);

// Game Event Table Creation
CREATE TABLE GameEvents (
    event_id UUID,
    event_type TEXT,
    player_id INT,
    timestamp TIMESTAMP,
    event_details MAP<TEXT, TEXT>,
    PRIMARY KEY (event_id)
);
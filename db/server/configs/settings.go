package settings

import (
	"os"
	"time"
)

// Database configs
var MOONSTREAM_DB_MAX_IDLE_CONNS int = 30
var MOONSTREAM_DB_CONN_MAX_LIFETIME = 30 * time.Minute
var MOONSTREAM_DB_URI = os.Getenv("MOONSTREAM_DB_URI")

// CORS
var MOONSTREAM_CORS_ALLOWED_ORIGINS = os.Getenv("MOONSTREAM_CORS_ALLOWED_ORIGINS")

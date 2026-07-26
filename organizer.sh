#!/bin/bash
#
# organizer.sh
# Archives the current grades.csv with a timestamp, resets a fresh empty
# grades.csv for the next batch, and logs the operation to organizer.log.

ARCHIVE_DIR="archive"
SOURCE_FILE="grades.csv"
LOG_FILE="organizer.log"

# 1. Ensure the archive directory exists
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi

# 2. Guard: nothing to archive if grades.csv doesn't exist
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

# 3. Generate a timestamp for this run
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"

# 4. Move (rename) the current grades.csv into the archive directory
mv "$SOURCE_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"
echo "Archived '$SOURCE_FILE' as '$ARCHIVE_DIR/$ARCHIVED_NAME'"

# 5. Reset the workspace: create a fresh, empty grades.csv
touch "$SOURCE_FILE"
echo "Created a fresh, empty '$SOURCE_FILE' for the next batch of grades."

# 6. Log the operation (append so history accumulates across runs)
echo "[$TIMESTAMP] Archived '$SOURCE_FILE' -> '$ARCHIVE_DIR/$ARCHIVED_NAME'" >> "$LOG_FILE"
echo "Logged this operation to '$LOG_FILE'."

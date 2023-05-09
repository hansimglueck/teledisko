#!/bin/bash
xset s off
xset -dpms
xset s noblank

# Start the Flask app in the background
python3 /home/Desktop/teledisko/flask-server/app.py  &

# Wait for the Flask app to start
sleep 5

# Launch Chromium in kiosk mode with the Flask app URL
chromium-browser --disable-infobars --kiosk http://localhost:5000

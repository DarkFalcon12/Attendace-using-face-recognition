# Attendace-using-face-recognition

# Face Recognition Attendance System

## Description
This project is a Face Recognition-based Attendance System that automatically marks attendance by detecting and recognizing faces using OpenCV and the face_recognition library. It also includes a Flask web application to store and retrieve attendance records.

## Features
- Real-time face recognition using a webcam.
- Automatic attendance marking.
- Flask-based web server for storing and retrieving attendance records.
- Attendance records saved in a JSON file.
- Late attendance detection.

## Technologies Used
- Python
- OpenCV
- face_recognition
- Flask
- JSON
- NumPy

## Installation
### Prerequisites
Ensure you have Python installed and install the required libraries using:
```sh
pip install opencv-python numpy face_recognition flask requests
```

### Clone the Repository
```sh
git clone https://github.com/yourusername/attendance-system.git
cd attendance-system
```

## Usage
### Step 1: Store Known Faces
- Place images of known individuals inside the `Test Images` folder.
- Each image filename should be the person's name (e.g., `John_Doe.jpg`).

### Step 2: Run the Flask Server
```sh
python app.py
```
This will start a local server at `http://127.0.0.1:5000`.

### Step 3: Run the Face Recognition Script
```sh
python face.py
```
- This script will start the webcam and detect faces in real-time.
- If a recognized face is detected, it sends an attendance request to the Flask server.
- Press 'q' to exit the face recognition window.

## API Endpoints
- `POST /mark_attendance` - Marks attendance for a recognized person.
- `GET /get_attendance?date=YYYY-MM-DD` - Retrieves attendance records for a specific date.

## Notes
- The system considers attendance **Late** if marked after `08:00:00 AM`.
- Attendance records are stored in `data/attendance.json`.
- The Flask app provides a simple web interface for viewing attendance records.

## Contributing
Feel free to fork this repository and submit pull requests.

## License
This project is open-source under the MIT License.


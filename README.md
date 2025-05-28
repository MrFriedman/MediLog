# NOTE: Not done the README so dont follow this (for now)

## Backend Setup

The backend is built using Flask and several Python libraries for speech processing.

### Requirements

- pip3
- homebrew
- python3
- Python Virtual Environment (venv)

### Installation

1. Navigate to backend directory

   ```bash
   git clone https://

   cd blahblah
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Install `espeak-ng` and other necessary libraries:

   ```bash
   brew install espeak-ng
   brew install ncurses libx11
   ```

5. Download and install Festival and MBROLA voices:

   ```bash
   curl -O https://raw.githubusercontent.com/pettarin/setup-festival-mbrola/master/setup_festival_mbrola.sh
   ```

   ```bash
   bash setup_festival_mbrola.sh . festival
   ```

6. Run the Redis server (in a separate terminal):

   ```bash
   redis-server
   ```

   If it fails running on port then:

   ```bash
   redis-server --port <xxxx>
   ```

7. Start the Flask development server:

   ```bash
   flask run
   ```

The Flask backend will be running on [http://localhost:5000](http://localhost:5000).

### Configuration

In `app.py`, ensure that your `UPLOAD_FOLDER` is correctly set in the app configuration:

```python
app.config['UPLOAD_FOLDER'] = 'path_to_your_upload_folder'
```
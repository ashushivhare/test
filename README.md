# test
# dialog_viewer

## Watson to Google CCAI Migration Tool

This tool helps you migrate IBM Watson Assistant dialogs to Google Contact Center AI (CCAI) format.

### Setup

1. Install the required dependencies:
   ```
   pip install flask graphviz google-cloud-dialogflow-cx
   ```

2. Set up Google Cloud credentials:
   - Create a service account in Google Cloud Console
   - Download the JSON credentials file
   - Rename it to `google_credentials.json` and place it in the project root
   - Update the project_id, location, and agent_id in the `dialog_viewer` function

3. Run the application:
   ```
   python dialogviewerscript.py
   ```

4. Access the web interface at http://localhost:5000

### Features

- View Watson Assistant dialogs
- Export dialogs to Google CCAI format
- Visualize dialog flows as diagrams

### Migration Process

1. Select a dialog from the dropdown menu
2. View the dialog visualization
3. Click "Export to Google CCAI" to convert the dialog
4. Download the exported JSON file
5. Import the JSON into Google Dialogflow CX
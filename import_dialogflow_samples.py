import json
import os
import argparse
from google.cloud import dialogflowcx_v3
from google.oauth2 import service_account

def import_flow(client, parent, flow_json):
    """
    Import a flow into Dialogflow CX
    
    Args:
        client: Dialogflow CX FlowsClient
        parent: Parent resource name (agent)
        flow_json: JSON representation of the flow
    
    Returns:
        The created flow
    """
    print(f"Importing flow: {flow_json.get('displayName', 'Unknown')}")
    
    # Create the flow
    flow = dialogflowcx_v3.Flow()
    flow.display_name = flow_json.get("displayName", "Imported Flow")
    flow.description = flow_json.get("description", "")
    
    # Create the flow in Dialogflow
    created_flow = client.create_flow(parent=parent, flow=flow)
    print(f"Created flow: {created_flow.display_name} ({created_flow.name})")
    
    # Create pages
    for page_json in flow_json.get("pages", []):
        page = dialogflowcx_v3.Page()
        page.display_name = page_json.get("displayName", "Unnamed Page")
        
        # Add entry fulfillment if present
        if "entryFulfillment" in page_json:
            page.entry_fulfillment = dialogflowcx_v3.Fulfillment()
            
            # Add messages
            for message_json in page_json.get("entryFulfillment", {}).get("messages", []):
                if "text" in message_json:
                    text = dialogflowcx_v3.ResponseMessage.Text()
                    text.text = message_json["text"].get("text", [])
                    message = dialogflowcx_v3.ResponseMessage()
                    message.text = text
                    page.entry_fulfillment.messages.append(message)
        
        # Create the page
        page_parent = created_flow.name
        created_page = client.create_page(parent=page_parent, page=page)
        print(f"  Created page: {created_page.display_name}")
    
    # Add transition routes after all pages are created
    for route_json in flow_json.get("transitionRoutes", []):
        route = dialogflowcx_v3.TransitionRoute()
        
        # Set intent if present
        if "intent" in route_json:
            route.intent = f"projects/sample-project/locations/us-central1/agents/sample-agent/intents/{route_json['intent']}"
        
        # Set condition if present
        if "condition" in route_json:
            route.condition = route_json["condition"]
        
        # Set target page if present
        if "targetPage" in route_json:
            # In a real implementation, you would need to map the page ID to the actual page resource name
            # For this sample, we'll just use a placeholder
            route.target_page = f"{created_flow.name}/pages/{route_json['targetPage']}"
        
        # Add the route to the flow
        client.update_flow(flow=created_flow)
        print("  Added transition route")
    
    return created_flow

def import_dialogflow_samples(project_id, location, agent_id, samples_dir="dialogflow_samples"):
    """
    Import sample dialogs into Dialogflow CX
    
    Args:
        project_id: Google Cloud project ID
        location: Google Cloud location
        agent_id: Dialogflow CX agent ID
        samples_dir: Directory containing sample dialogs
    """
    print(f"Importing samples from {samples_dir} to project {project_id}, location {location}, agent {agent_id}")
    
    # Check if credentials file exists
    if not os.path.exists('google_credentials.json'):
        print("Error: google_credentials.json not found. Please create this file with your Google Cloud credentials.")
        return
    
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file('google_credentials.json')
    
    # Create Dialogflow CX client
    client = dialogflowcx_v3.FlowsClient(credentials=credentials)
    
    # Parent resource name
    parent = f"projects/{project_id}/locations/{location}/agents/{agent_id}"
    
    # Check if samples directory exists
    if not os.path.exists(samples_dir):
        print(f"Error: Samples directory {samples_dir} not found. Run create_dialogflow_samples.py first.")
        return
    
    # Get list of sample files
    sample_files = [f for f in os.listdir(samples_dir) if f.endswith('.json') and f != 'all_samples.json']
    
    if not sample_files:
        print(f"No sample files found in {samples_dir}")
        return
    
    print(f"Found {len(sample_files)} sample files")
    
    # Import each sample
    for sample_file in sample_files:
        file_path = os.path.join(samples_dir, sample_file)
        print(f"Processing {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                flow_json = json.load(f)
            
            import_flow(client, parent, flow_json)
            print(f"Successfully imported {sample_file}")
            
        except Exception as e:
            print(f"Error importing {sample_file}: {e}")
    
    print("Import completed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import sample dialogs into Dialogflow CX")
    parser.add_argument("--project-id", required=True, help="Google Cloud project ID")
    parser.add_argument("--location", default="us-central1", help="Google Cloud location")
    parser.add_argument("--agent-id", required=True, help="Dialogflow CX agent ID")
    parser.add_argument("--samples-dir", default="dialogflow_samples", help="Directory containing sample dialogs")
    
    args = parser.parse_args()
    
    import_dialogflow_samples(args.project_id, args.location, args.agent_id, args.samples_dir)
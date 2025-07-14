import json
import uuid
import os
from datetime import datetime

def create_sample_dialog(name, description, intents, responses):
    """
    Create a sample dialog in Dialogflow CX format
    
    Args:
        name: Name of the dialog/flow
        description: Description of the dialog
        intents: List of intents to trigger the dialog
        responses: List of response texts
    
    Returns:
        Dictionary representing a Dialogflow CX flow
    """
    print(f"Creating sample dialog: {name}")
    
    # Generate unique IDs
    flow_id = str(uuid.uuid4())
    start_page_id = str(uuid.uuid4())
    response_page_id = str(uuid.uuid4())
    
    # Create the flow structure
    flow = {
        "name": f"projects/sample-project/locations/us-central1/agents/sample-agent/flows/{flow_id}",
        "displayName": name,
        "description": description,
        "transitionRoutes": [
            {
                "intent": intent,
                "targetPage": response_page_id
            } for intent in intents
        ],
        "pages": [
            {
                "name": f"projects/sample-project/locations/us-central1/agents/sample-agent/flows/{flow_id}/pages/{start_page_id}",
                "displayName": "Start Page",
                "transitionRoutes": [
                    {
                        "intent": intent,
                        "targetPage": response_page_id
                    } for intent in intents
                ]
            },
            {
                "name": f"projects/sample-project/locations/us-central1/agents/sample-agent/flows/{flow_id}/pages/{response_page_id}",
                "displayName": "Response Page",
                "form": {
                    "parameters": []
                },
                "entryFulfillment": {
                    "messages": [
                        {
                            "text": {
                                "text": [response]
                            }
                        } for response in responses
                    ]
                }
            }
        ]
    }
    
    return flow

def create_sample_dialogs():
    """Create a set of sample dialogs for testing"""
    print("Starting to create sample dialogs...")
    
    # Create output directory if it doesn't exist
    output_dir = "dialogflow_samples"
    os.makedirs(output_dir, exist_ok=True)
    
    # Sample dialogs
    dialogs = [
        {
            "name": "Account Information",
            "description": "Provides account information to the user",
            "intents": ["account_info", "account_details", "my_account"],
            "responses": [
                "Your account was created on January 15, 2023. Your current plan is the Business Premium Plan with 5 active lines.",
                "Would you like to know more about your account features?"
            ]
        },
        {
            "name": "Billing Inquiry",
            "description": "Handles billing related questions",
            "intents": ["billing_inquiry", "bill_question", "payment_question"],
            "responses": [
                "Your current bill is $125.45 due on May 15, 2024.",
                "You can pay your bill online at att.com/pay or through the myAT&T app."
            ]
        },
        {
            "name": "Add New Line",
            "description": "Helps users add a new line to their account",
            "intents": ["add_line", "new_line", "additional_line"],
            "responses": [
                "To add a new line to your account, I'll need to collect some information.",
                "First, let me check if you're eligible for any promotions on a new line.",
                "You qualify for our Buy One Get One promotion on select devices!"
            ]
        },
        {
            "name": "Technical Support",
            "description": "Provides technical support for common issues",
            "intents": ["tech_support", "help_with_device", "troubleshoot"],
            "responses": [
                "I'm sorry you're experiencing technical difficulties. Let's troubleshoot together.",
                "First, have you tried restarting your device?",
                "If that doesn't work, we can try resetting your network settings."
            ]
        },
        {
            "name": "Plan Upgrade",
            "description": "Helps users upgrade their current plan",
            "intents": ["upgrade_plan", "better_plan", "change_plan"],
            "responses": [
                "Based on your usage, I recommend upgrading to our Unlimited Elite plan.",
                "This plan includes unlimited talk, text, and data with no throttling, plus HBO Max included.",
                "The cost would be $85/month for your first line, with discounts for additional lines."
            ]
        }
    ]
    
    # Create each dialog and save to file
    for dialog in dialogs:
        flow = create_sample_dialog(
            dialog["name"],
            dialog["description"],
            dialog["intents"],
            dialog["responses"]
        )
        
        # Save to file
        filename = f"{output_dir}/{dialog['name'].lower().replace(' ', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(flow, f, indent=2)
        print(f"Created sample dialog: {filename}")
    
    # Create a combined file with all dialogs
    all_dialogs = {
        "flows": [
            create_sample_dialog(
                dialog["name"],
                dialog["description"],
                dialog["intents"],
                dialog["responses"]
            ) for dialog in dialogs
        ],
        "metadata": {
            "created": datetime.now().isoformat(),
            "description": "Sample dialogs for testing Dialogflow CX import",
            "count": len(dialogs)
        }
    }
    
    with open(f"{output_dir}/all_samples.json", 'w') as f:
        json.dump(all_dialogs, f, indent=2)
    
    print(f"Created combined file with all {len(dialogs)} dialogs: {output_dir}/all_samples.json")
    print(f"Sample dialogs have been created in the '{output_dir}' directory")

if __name__ == "__main__":
    create_sample_dialogs()
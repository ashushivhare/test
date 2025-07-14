from flask import Flask, render_template, request
from flask import jsonify, redirect, url_for
import threading
import tkinter as tk
from tkinter import Canvas
from graphviz import Digraph
import re
import os
import json
import uuid
from google.cloud import dialogflow_cx_v3
from google.oauth2 import service_account

app = Flask(__name__)

# Google CCAI Configuration
def get_google_credentials():
    try:
        # Check if credentials file exists
        if os.path.exists('google_credentials.json'):
            credentials = service_account.Credentials.from_service_account_file(
                'google_credentials.json')
            return credentials
        else:
            return None
    except Exception as e:
        print(f"Error loading Google credentials: {e}")
        return None

def create_ccai_flow(dialog_data, project_id, location, agent_id):
    """Convert Watson dialog to Google CCAI flow format"""
    credentials = get_google_credentials()
    if not credentials:
        return {"error": "Google credentials not found"}
    
    try:
        # Create Dialogflow CX client
        client = dialogflow_cx_v3.FlowsClient(credentials=credentials)
        
        # Create a new flow
        parent = f"projects/{project_id}/locations/{location}/agents/{agent_id}"
        flow = dialogflow_cx_v3.Flow()
        flow.display_name = dialog_data.get('title', 'Imported Watson Dialog')
        flow.description = f"Imported from Watson Assistant: {dialog_data.get('title', '')}"
        
        # Create pages for each dialog node
        pages = []
        routes = []
        
        # Process dialog nodes
        for key, value in dialog_data.items():
            if 'title' in key and not key == 'title':
                # Create a page for this dialog node
                page_id = str(uuid.uuid4())
                page = {
                    "id": page_id,
                    "display_name": value,
                    "entry_fulfillment": {
                        "messages": []
                    }
                }
                
                # Find associated dialog text
                dialog_key = key.replace('title', 'dialog')
                if dialog_key in dialog_data and dialog_data[dialog_key]:
                    page["entry_fulfillment"]["messages"].append({
                        "text": {
                            "text": [dialog_data[dialog_key]]
                        }
                    })
                
                pages.append(page)
                
                # Create routes
                jump_key = key.replace('title', 'jump')
                if jump_key in dialog_data and dialog_data[jump_key]:
                    # This is a jump to another node
                    routes.append({
                        "source": page_id,
                        "target": dialog_data[jump_key],
                        "condition": "true"
                    })
        
        # Create the CCAI export format
        ccai_export = {
            "flow": {
                "name": f"projects/{project_id}/locations/{location}/agents/{agent_id}/flows/{str(uuid.uuid4())}",
                "display_name": dialog_data.get('title', 'Imported Watson Dialog'),
                "description": f"Imported from Watson Assistant: {dialog_data.get('title', '')}",
                "pages": pages,
                "routes": routes
            }
        }
        
        return ccai_export
    
    except Exception as e:
        print(f"Error creating CCAI flow: {e}")
        return {"error": str(e)}

# Function to draw the Data Flow Diagram
def dialog_viewer(selected_item):
        from ibm_watson import AssistantV1
        from ibm_watson import AssistantV2
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        import json
        # V2 libraries can't see old V1 libraries
        authenticator = IAMAuthenticator('qpLmPC9InrkehNB3dYCJFpD4Q0f8eHUjJf1c0JF94mP-')

        assistant = AssistantV1(
            version='2021-06-14',
            authenticator=authenticator
        )

        assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com/instances/988e9164-c283-425d-ab70-be1e07fd65c7')
        def get_workspace_map():
            response=assistant.list_workspaces().get_result()
            list_workspaces=[]
            for workspaces in response['workspaces']:
                workspace={'name':workspaces['name'],'ID':workspaces['workspace_id']}
                list_workspaces.append(workspace)
        #print(assistant.list_workspaces())
        #List of skills for Premier
        Premier_workspace_list={selected_item}
        #Downloading the Skill
        def download_a_workspace(assistant, workspace_name):
            '''
            This function is used to download a skill by workspace_id.
            '''
            response = assistant.list_workspaces(sort='name').get_result()
            workspaces = response['workspaces']
            downloaded_workspaces = []
            for workspace in workspaces:
                if workspace['name'] == workspace_name:
                    downloaded_workspace = assistant.get_workspace(workspace_id = workspace['workspace_id'], 
                                                                export=True, 
                                                                include_audit=None).get_result()
                    downloaded_workspaces.append(downloaded_workspace)
            return downloaded_workspaces
        #download all skills for premierlist
        Skill_list=[]
        for name in Premier_workspace_list:

            response=download_a_workspace(assistant,name)
            skill={'name':name,'response':response}
            Skill_list.append(skill)
        #print(len(Skill_list))
        #Download skills for the list 
        for skill in Skill_list:
            #print(skill.values())
            response=skill['response']
           # response=list(skill.values())
            #dialog_nodes=response['dialog_nodes']
            #value=response[0]
            #print(dialog_nodes)
            dialog_nodes=response[0]['dialog_nodes']
        #new approach to get all childs
        skill_dialog_map=[]
        multivalued_nodes=[]
        root_nodes=[]
        child_nodes=[] 
        node_list=[]
        for skill in Skill_list:
                response=skill['response']
                dialog_nodes=response[0]['dialog_nodes']


                for nodes in dialog_nodes:
                    if(nodes['type']=='standard'):
                        node_list.append(nodes)

                for nodes in dialog_nodes:
                    if(nodes['type']=='response_condition'):
                        multivalued_nodes.append(nodes)
                #print(multivalued_nodes)

                for nodes in node_list:
                    if('parent' in nodes):
                        child_nodes.append(nodes)
                    else:
                        root_nodes.append(nodes)
        #print(root_nodes)
        def get_jump_Node(nodekey):
                    #print(nodekey)
                    title='not found'
                    for nodes in (dialog_nodes):
                        if(nodes['dialog_node']==nodekey):
                            if('title'in nodes):
                                title= nodes['title']
                    return  title       
        def getchildnodes(child_nodes,data,dialognode,lastname,level):
                            j=0


                            for child in child_nodes:
                                endsearch=False
                                if dialognode==child['parent']:

                                    name=lastname+"level"+str(level)
                                    if(lastname is not None):
                                        name=lastname+"_level"+str(level)

                                    j=j+1
                                    name=name+"child"+str(j)
                                    if('title'in child):
                                        data[name+'title']=child['title']
                                        #print(child['title'])
                                    if('conditions' in child):
                                        data[name+'condition']=child['conditions']
                                    if('output' in child ):
                                        #print(chield['output'])
                                        if('generic' in child['output']):
                                            generic=child['output']['generic']

                                            for values in generic:
                                                if 'values' in values:
                                                    for text in values['values']:

                                                        data[name+'dialog']=text['text']
                                    if('next_step' in child):
                                        next_step=child['next_step']
                                        if('behavior' in next_step):
                                            if(next_step['behavior']=='jump_to'):

                                                jump_node_title=get_jump_Node(next_step['dialog_node'])

                                                data[name+'jump']=jump_node_title
                                                endsearch=True
                                    if('context' in child):
                                            if('waFlags' in child['context']):
                                                if('Switch_Workspace') in child['context']['waFlags']:

                                                    if(child['context']['waFlags']['Switch_Workspace']!='Router_WCS'):
                                                        endsearch=True

                                                        data[name+'waFlags']=child['context']['waFlags']['Switch_Workspace'] 

                                                if('endSession') in child['context']['waFlags']:
                                                    data[name+'waFlags']="End Chat"
                                                    endsearch=True

                                    #waflags="End Chat"
                                    #print(endsearch)
                                    if('metadata' in child):
                                        if('_customization' in child['metadata']):
                                            if(child['metadata']['_customization']['mcr']==True):
                                                root_condition=name+'nodeoption'
                                                root_dialog=name+'nodetext'
                                                jump=name+'nodeend'
                                                waflags=name+'nodeflags'
                                                data=getrootconditionnodes(multivalued_nodes,data,root_condition,root_dialog,child['dialog_node'],jump,waflags)


                                    if not endsearch:
                                        childlevel=level+1
                                        data,childlevel=getchildnodes(child_nodes,data,child['dialog_node'],name,childlevel)


                            return data,level 

        def getrootconditionnodes(multivalued_nodes,data,root_condition,root_dialog,nodes,jump,waflags):
                            i=0
                            #data=[]
                            for  multinodes in multivalued_nodes:

                                if nodes== multinodes['parent']:

                                    i=i+1
                                    condition=root_condition+str(i)
                                    Dialog=root_dialog+str(i)
                                    waflag=waflags+str(i)
                                    data[condition]=""
                                    data[Dialog]=""
                                    if('conditions' in multinodes):
                                        data[condition]=multinodes['conditions']


                                    if('output' in multinodes ):

                                        if('text' in multinodes['output']):
                                                    #text=multinodes['output']['text']
                                                    values=multinodes['output']['text']['values']
                                                    for value in values:
                                                        data[Dialog]=value

                                                        #print(value)
                                        if('generic' in multinodes['output']):
                                                    generic=multinodes['output']['generic']

                                                    for values in generic:
                                                        for text in values['values']: 
                                                            if isinstance(text['text'], list):
                                                                data[Dialog]=text['text'][0]
                                                            else:
                                                                data[Dialog]=text['text']
                                        if('next_step' in multinodes):
                                            next_step=multinodes['next_step']
                                            if('behavior' in next_step):
                                                if(next_step['behavior']=='jump_to'):

                                                    jump_node_title=get_jump_Node(next_step['dialog_node'])


                                                    data[jump+str(i)]=jump_node_title
                                        if('context' in multinodes):
                                            if('waFlags' in multinodes['context']):
                                                if('Switch_Workspace') in multinodes['context']['waFlags']:

                                                    data[waflag]=multinodes['context']['waFlags']['Switch_Workspace']
                                                if('endSession') in multinodes['context']['waFlags']:
                                                    data[waflag]="End Chat"
                                       # Data.append(data)


                            return data

        Data=[]

        for nodes in (root_nodes):

                        dialog=''
                        waflags=''
                        rootjumpnodetitle=''
                        if('conditions' in nodes):
                            intent=nodes['conditions']
                        if('output' in nodes):
                            if('generic' in nodes['output']):

                                generic=nodes['output']['generic']

                                for values in generic:
                                    for text in values['values']:
                                        #print(text['text'])
                                        dialog=text['text']
                                #print(values)
                        if('title' in nodes):
                            title=nodes['title']

                            #dialog=nodes['output'][0]['text']
                        if('context' in nodes):
                            if('waFlags' in nodes['context']):
                                if('Switch_Workspace') in nodes['context']['waFlags']:
                                    waflags=nodes['context']['waFlags']['Switch_Workspace']
                                if('endSession') in nodes['context']['waFlags']:
                                    waflags="End Chat"
                        if('next_step' in nodes): 
                            if('behavior' in nodes['next_step']):
                                next_step=nodes['next_step']['behavior']
                                if(next_step=='jump_to'):
                                    rootjumpnodetitle=get_jump_Node(nodes['next_step']['dialog_node'])
                                    
                                    
                                    

                        data={'intent':intent,'title':title,'dialog':dialog,'waFlags':waflags,'root_nodetitle':rootjumpnodetitle}

                        data=getrootconditionnodes(multivalued_nodes,data,'root_condition','root_dialog',nodes['dialog_node'],'root_jump','root_waFlags')

                        data,level=getchildnodes(child_nodes,data,nodes['dialog_node'],'',1)

                        Data.append(data)
        return Data

def count_level(obj):
            count = 0


            for key, value in obj.items():
                    #print(key)
                    nextcount = key.count('_')  # Check in keys
                    if nextcount>count:
                        count=nextcount


            return count
def getnumberofnode(nodekey,obj):
            node=0
            for key,value in obj.items():

                if(nodekey in key):
                    node=node+1
            return node
def getjumpKeys(jumpkey,obj):
            jumpkeylist=[]
            for key,value in obj.items():
                    if(jumpkey in key):
                        lastdigit=re.search(r'\d+$', key).group()
                        jumpkeylist.append(lastdigit)
            return jumpkeylist
def getnode(rootkey,obj):
            node=''
            for key,values in obj.items():
                if(rootkey+'nodeoption' in key):                            
                         if(len(obj[key]))<1:
                                node=key
            return node                    
def draw_dfd(map_obj,output_dir,dfd_files):
            DFD_list=[]
            for obj in map_obj:
                try:
                #if(selected_item == obj['title']):
                    childnodelist=[]
                    rootconditionlist=[]
                    nodechildconditionlist=[]
                    dfd = Digraph('DFD', filename='dfd', format='pdf')
                    #dfd.attr(splines="polyline")  # Smooth edges with minimal crossings

                    if(len(obj.keys())>25):
                        dfd.attr(rankdir='LR', size='50,50',bgcolor="azure",ordering="out",splines="polyline")
                    else:
                        dfd.attr(rankdir='TB', size='20',bgcolor="azure",ordering="out",splines="polyline")


                    # Root process
                    dfd.node('Title', str(obj['title']).replace('"', '\\"'),fontsize="9", shape='rectangle',style='filled',fillcolor='lightblue')

                    # Intent condition
                    dfd.node('Intent', obj['intent'], shape='diamond',fontsize="9" ,style='filled',fillcolor='lightblue')

                    dfd.edge('Title', 'Intent', label='Intent')
                    if 'waFlags' in obj :
                        if(len(obj['waFlags'])>0):
                            dfd.node(obj['waFlags'], obj['waFlags'], shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')
                            if("End Chat" in obj['waFlags']):
                                dfd.edge('Intent', obj['waFlags'],minlen="2")
                            else:
                                dfd.edge('Intent', obj['waFlags'], label='Switch Workspace')
                    dialogpresent=False
                    if len(obj['dialog'])>0:

                        dialogpresent=True
                    rootdialogpresent=False
                    level=count_level(obj)
                    for key,value in obj.items():
                           if(key.count('_') >0):

                                if('nodeoption' in key and len(obj[key])>0):
                                       dfd.node(key, value, shape='diamond',fontsize="9" ,style='filled',fillcolor='lightgrey')
                                elif('nodetext' in key):
                                       if(len(obj[key])>0): 
                                            dfd.node(key, value, shape='rectangle',fontsize="9" ,style='filled',fillcolor='lightyellow')
                                elif('nodeflags' in key):
                                       dfd.node(key, value, shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')
                                elif('nodeend' in key):
                                       dfd.node(key, value, shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')
                                elif('root_condition' in key):
                                       if(len(obj[key])>0): 
                                           dfd.node(key, value, shape='diamond',fontsize="9" ,style='filled',fillcolor='lightgrey')
                                elif('root_dialog' in key):
                                       if(len(obj[key])>0):
                                            rootkey=key.replace('dialog','condition')
                                            if(len(obj[rootkey])>0):
                                                clean_dialog = re.sub(r'</?p>', '', value)
                                                dfd.node(key, clean_dialog, shape='rectangle',fontsize="9" ,style='filled',fillcolor='lightyellow')
                                            elif(dialogpresent):
                                                rootdialogpresent=True
                                                clean_dialog = re.sub(r'</?p>', '', obj['dialog'])
                                                dfd.node('Dialog', clean_dialog, shape='rectangle',fontsize='9',style='filled',fillcolor='lightyellow')
                                                dfd.edge('Intent','Dialog', label='Dialog',minlen="2")
                                elif('root_flags' in key):
                                       dfd.node(key, value, shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')


                                elif('title' in key):
                                       dfd.node(key, value, shape='diamond',fontsize="9" ,style='filled',fillcolor='lightblue')
                                elif('dialog' in key):
                                       if('root_dialog' in key):
                                            root_condition=key.replace('root_dialog','root_condition')
                                            if(len(obj[root_condition])>0):
                                               clean_dialog=re.sub(r'</?p>', '', value)  
                                               dfd.node(key, clean_dialog, shape='rectangle',fontsize="9" ,style='filled',fillcolor='lightyellow')

                                       elif(len(obj[key])>0):  
                                           clean_dialog=re.sub(r'</?p>', '', value) 
                                           dfd.node(key, clean_dialog, shape='rectangle',fontsize="9" ,style='filled',fillcolor='lightyellow')

                                elif('waFlags' in key):
                                       dfd.node(key, value, shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')
                                elif('jump' in key):
                                       dfd.node(key, value, shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')
                                elif('root_nodetitle' in key):
                                       dfd.node(key, value, shape='ellipse',fontsize="9" ,style='filled',fillcolor='lightgreen')
                                       dfd.edge('Dialog','root_jumpnodetitle', label='jump',minlen="2") 
                    if(rootdialogpresent==False and dialogpresent):
                        newvalue=re.sub(r'</?p>', '', obj['dialog'])
                        dfd.node('Dialog', newvalue, shape='rectangle',fontsize='9',style='filled',fillcolor='lightyellow')
                        dfd.edge('Intent','Dialog', label='Dialog',minlen="2")

                    for key,value in obj.items():
                        count=key.count('_')
                        if(count>0):
                            if(count==1):
                                   if ('nodeoption' in key and len(obj[key])>0):
                                        lastdigit=re.search(r'\d+$', key).group()

                                        condition='nodeoption'+str(lastdigit)

                                        rootkey=key.replace(condition,'title')
                                        #print(rootkey)

                                        dfd.edge(rootkey, key) 
                                   elif ('nodetext' in key and len(obj[key])>0):
                                        #text = key.rsplit('_', 1)[-1]
                                        #print(text)
                                        rootkey=key.replace('text','option')
                                        if(len(obj[rootkey])>0):
                                            dfd.edge(rootkey, key)
                                        else:
                                            lastdigit=re.search(r'\d+$', key).group()
                                            nodetext='nodetext'+str(lastdigit)
                                            rootkey=key.replace(nodetext,'title')
                                            dfd.edge(rootkey, key)
        #                                 else:
        #                                     rootkey=key.replace('nodeoption','title')
        #                                     dfd.edge(rootkey, key)

                                   elif('title' in key):
                                        if(dialogpresent):
                                            dfd.edge('Dialog', key) 
                                        else:
                                            dfd.edge('Intent', key) 
                                   elif('root_dialog' in key):

                                            rootkey=key.replace('dialog','condition')
                                            if len(obj[key])>0:

                                                if(len(obj[rootkey])>0):
                                                    dfd.edge(rootkey, key)
        #                                         else:
        #                                             dfd.edge('Intent', key)

                                   elif('root_condition' in key):
                                        if(len(obj[key])>0):
                                            dfd.edge('Intent', key)

                                   elif('root_jump' in key):

                                        oldkey=key.replace('jump','dialog')
                                        if(len(obj[oldkey])>0):
                                            dfd.edge(oldkey, key,label='Jump To') 
                                        else:
                                            oldkey=key.replace('jump','condition')
                                            if(len(obj[oldkey])>0):
                                                dfd.edge(oldkey, key,label='Jump To')
                                            else:
                                                dfd.edge('Intent',key,label='Jump To')
                                   elif('root_waFlags' in key):
                                        oldkey=key.replace('waFlags','dialog')
                                        if(len(obj[oldkey])>0):
                                            dfd.edge(oldkey,key)
                                        else:
                                            oldkey=key.replace('waFlags','condition')
                                            if(len(obj[oldkey])>0):
                                                if(obj[key]!='End Chat'):
                                                    dfd.edge(oldkey,key,label='Switch Workspace')
                                                else:
                                                    dfd.edge(oldkey, key)    
                                            else:
                                                if(obj[key]!='End Chat'):
                                                    dfd.edge('Intent',key,label='Switch Workspace')
                                                else:
                                                    dfd.edge(oldkey, key)    

                                   elif('dialog' in key ):
                                        oldkey=key.replace('dialog','title')

                                        dfd.edge(oldkey, key)
                                   elif('nodeend' in key):
                                        newkey=key.replace('nodeend','nodeoption')
                                        if(len(obj[newkey])>0):
                                            dfd.edge(newkey, key,label='Jump To') 

                                        else:

                                             lastdigit=re.search(r'\d+$', key).group()
                                             newkey=key.replace('nodened'+str(lastdigit),'title')
                                             dfd.edge(newkey, key,label='Jump To')
                                        #dfd.edge(oldkey,key,label='Jump To')
                                   elif('jump' in key):
                                        oldkey=key.replace('jump','title')
                                        dfd.edge(oldkey, key,label='Jump To')      
                                   elif('nodeflags' in key):
                                        oldkey=key.replace('flags','text')
                                        if(len(obj[oldkey])>0): 
                                            if(obj[key]!='End Chat'):
                                                dfd.edge(oldkey, key,label='Switch Workspace')
                                            else:
                                                    dfd.edge(oldkey, key)    
                                        else:
                                            oldkey=key.replace('flags','option')
                                            if(len(obj[oldkey])>0):
                                                if(obj[key]!='End Chat'):
                                                    dfd.edge(oldkey, key,label='Switch Workspace')
                                                else:
                                                    dfd.edge(oldkey, key)    
                                            else:
                                                lastdigit=re.search(r'\d+$', key).group()
                                                oldkey=key.replace('nodeflags'+str(lastdigit),'title')
                                                if(obj[key]!='End Chat'):
                                                    dfd.edge(oldkey, key,label='Switch Workspace')
                                                else:
                                                    dfd.edge(oldkey, key)    
                                   elif('waFlags' in key):
                                        oldkey=key.replace('waFlags','dialog')
                                        if(oldkey in obj):
                                            if(obj[key]!='End Chat'):
                                                dfd.edge(oldkey, key,label='Switch Workspace')
                                            else:
                                                dfd.edge(oldkey, key)    
                                        elif(key.replace('waFlags','title') in obj):
                                            oldkey=key.replace('waFlags','title')
                                            if(obj[key]!='End Chat'):
                                                dfd.edge(oldkey, key,label='Switch Workspace')
                                            else:
                                                dfd.edge(oldkey, key)    
                                        #dfd.edge(oldkey, key)     
                            if(count>1):
                                     if('nodeoption' in key):
                                        #print(key)
                                        if(len(obj[key])>0):
                                            lastdigit=re.search(r'\d+$', key).group()
                                            rootkey=key.replace('nodeoption'+str(lastdigit),'title')
                                            dfd.edge(rootkey, key)

                                     elif('title' in key):

                                        rootkey= key.rsplit('_', 1)[0]
                                        node=getnode(rootkey,obj)     


                                        if(len(node)>0):
                                            node=node.replace('option','text')
                                            #print(node)
                                            if(len(obj[node])>0):
                                                dfd.edge(node, key) 
                                            else:
                                                node=node.replace('text','option')
                                                if(len(obj[node])>0):
                                                    dfd.edge(node, key)
                                                else:
                                                    rootkey=rootkey+'title'       
                                                    dfd.edge(rootkey, key)
                                        else:    
                                            rootkey=rootkey+'title'       
                                            dfd.edge(rootkey, key) 
                                     elif('nodetext' in key ):
                                        if( len(obj[key])>0):
                                            rootkey=key.replace('text','option') 
                                            if(len(obj[rootkey])>0):
                                                dfd.edge(rootkey, key)
                                            else:
                                                lastdigit=re.search(r'\d+$', key).group()
                                                #rootkey=rootkey+str(lastdigit)
                                                rootkey=key.replace('nodetext'+str(lastdigit),'title')
                                                print(rootkey)
                                                dfd.edge(rootkey, key)
                                     elif('nodeflags' in key):

                                        rootkey=key.replace('flags','text') 
                                        if(len(obj[rootkey])>0):
                                             if(obj[key]!='End Chat'):
                                                    dfd.edge(rootkey, key,label='Switch Workspace')
                                             else:
                                                    dfd.edge(rootkey, key)
                                        else:
                                            rootkey=key.replace('flags','option')
                                            if(len(obj[rootkey])>0):
                                                if(obj[key]!='End Chat'):
                                                    dfd.edge(rootkey, key,label='Switch Workspace')
                                                else:
                                                    dfd.edge(rootkey, key)    
                                            else:
                                                lastdigit=re.search(r'\d+$', key).group()
                                                rootkey=key.replace('nodeflags'+str(lastdigit),'title')
                                                if(obj[key]!='End Chat'):
                                                    dfd.edge(rootkey, key,label='Switch Workspace')
                                                else:
                                                    dfd.edge(rootkey, key)

                                     elif('root_dialog' in key and len(obj[key])>0):
                                        #rootkey=key.replace('dialog','title')
                                        dfd.edge('Intent', key)   
                                     elif('dialog' in key):
                                        rootkey=key.replace('dialog','title')
                                        dfd.edge(rootkey, key)
                                     elif('waFlags' in key):

                                        rootkey=key.replace('waFlags','dialog')
                                        if(rootkey in obj):
                                            if(obj[key]!='End Chat'):
                                                dfd.edge(rootkey, key,label='Switch Workspace')
                                            else:
                                                dfd.edge(rootkey, key)    
                                        elif(key.replace('waFlags','title') in obj):
                                            rootkey=key.replace('waFlags','title')
                                            if(obj[key]!='End Chat'):
                                                dfd.edge(rootkey, key,label='Switch Workspace')
                                            else:
                                                dfd.edge(rootkey, key)

                                     elif('nodeend' in key):

                                        rootkey=key.replace('nodeend','nodeoption')
                                        #print(rootkey,'key->',key)
                                        if(len(obj[rootkey])>0):
                                            dfd.edge(rootkey, key,label='Jump To') 
                                        else:
                                            rootkey=key.replace('nodeend','nodetext')
                                            if(len(obj[rootkey])>0):
                                                dfd.edge(rootkey, key,label='Jump To')
                                            else:
                                                lastdigit=re.search(r'\d+$', key).group()
                                                rootkey=key.replace('nodened'+str(lastdigit),'title')
                                                dfd.edge(rootkey, key,label='Jump To')
                                     elif('jump' in key):
                                        rootkey=key.replace('jump','title')
                                        dfd.edge(rootkey, key,label='Jump To')    




                    filename=re.sub(r'[^a-zA-Z0-9_-]', '_', obj['title'])
                    
                    
                    file_path = os.path.join(output_dir, filename)
                    dfd.render(file_path, format="pdf", cleanup=False)
                    DFD_list.append(dfd)
                    dfd_files.append(f"pdfs/{filename}.pdf")
                except Exception as e:
                    print(f"⚠️ Error processing object '{obj.get('title', 'Unknown')}': {e}")
                    continue  # Skip this object and continue with the next one
            return  dfd_files

        # Function to handle item selection from the listbox


        



# Custom names for navigation buttons and dropdown items
menu_data = {
    "Premier": ['Add_A_New_Line','Autopay','Balance Due','Billing Reports','Data Usage','Login_and_Registration','Pay Bill','Payment Arrangements','Payment Confirmation','Router_WCS','Upgrade_Eligibility','View Bill'],
    "SMB": ['SMB'],
    "MyAtt": ['myATT_FirstNet',"myATT_FirstNet_Central"],
    "Premierfirstnet": ['Premier_FirstNet'],
    "BC": ["BC_PreLogin", "BC Get Ticket Status","BC_Router"],
    "FN Central":["FN_Central"]

}


@app.route("/")
def home():
    return render_template("page.html", title="Home", menu_data=menu_data, pdfs=[], selected_item="")

@app.route("/<category>/<item>")
def category_item(category, item):
    if category not in menu_data:
        return "Page Not Found", 404
    else:
        dfd_files = []
        output_dir = "static/pdfs"
        os.makedirs(output_dir, exist_ok=True)
        Data=dialog_viewer(item)
        dfd_files=draw_dfd(Data,output_dir,dfd_files)
        
            
    return render_template("page.html", title=category, menu_data=menu_data, pdfs=dfd_files, selected_item=item, category=category)

@app.route("/export_to_ccai/<category>/<item>", methods=["POST"])
def export_to_ccai(category, item):
    # Get the dialog data
    Data = dialog_viewer(item)
    
    # Get selected dialogs to migrate
    selected_dialogs = request.form.getlist('selected_dialogs')
    
    if not selected_dialogs:
        return "No dialogs selected for migration", 400
    
    # Filter the data to only include selected dialogs
    filtered_data = []
    for dialog in Data:
        if dialog.get('title') in selected_dialogs:
            filtered_data.append(dialog)
    
    # Configure Google CCAI parameters
    # These should be set by the user or stored in configuration
    project_id = "your-project-id"  # Replace with actual project ID
    location = "us-central1"        # Replace with actual location
    agent_id = "your-agent-id"      # Replace with actual agent ID
    
    # Convert to CCAI format
    ccai_data = []
    for dialog in filtered_data:
        ccai_flow = create_ccai_flow(dialog, project_id, location, agent_id)
        ccai_data.append(ccai_flow)
    
    # Save the CCAI data to a file
    os.makedirs("static/ccai_exports", exist_ok=True)
    filename = f"{item}_ccai_export.json"
    file_path = os.path.join("static/ccai_exports", filename)
    
    with open(file_path, 'w') as f:
        json.dump(ccai_data, f, indent=2)
    
    return render_template("export_success.html", item=item, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)



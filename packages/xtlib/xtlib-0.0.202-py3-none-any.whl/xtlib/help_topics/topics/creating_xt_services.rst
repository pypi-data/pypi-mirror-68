.. _creating_xt_services:

========================================
Creating XT Services
========================================

XT uses a set of Azure cloud services to run jobs on cloud computers, log stats, and store experiment artifacts. 
After you install XT, you run the **xt create team** command to create the template for the services. This topic shows you how to set up all the Azure cloud services you need for successful operation of XT.

------------------------------
Team Setups
------------------------------

If you are a member of a development team that wants to share a single set of services, select a team member to be the XT admin.  The XT admin manages creation of the XT services and maintains a list of your service users.

If you are setting up XT for your own use, you just create the XT services yourself.

------------------------------
Sandbox Services
------------------------------

Your organization may also have built a set of Sandbox services. Sandbox Services are designed for trying out and learning how to use XT. When you are ready to do work, you will want to create the complete set of services for your team.

--------------------------
Adding a new XT Team
--------------------------

Multiple XT users can share a set of XT services; the group is referred to as an **XT Team**.

When you add a new team to XT, you create several Azure services and add them to your local XT config file. 

This page provides a step-by-step guide for how to create the Azure services and add the config file changes.

The processes to add a new team should take the following time periods:
    - Create the 6 Azure services (20 mins);
    - Add the service keys and XT certificate to the key value (15 mins);
    - Edit the local XT config file (15 mins).

--------------------------
The Azure Services for XT
--------------------------

Every XT team uses 6 Azure services:

    - **Storage**            Provides cloud storage for your experiments
    - **Mongo DB**           Database for statistics and metrics of your experiments
    - **Key Vault**          Secure credential storage for Azure services
    - **Azure Batch**        A general compute service for on-demand Virtual Machine deployment
    - **Azure ML**           Compute services designed for Machine Learning on VMs
    - **Container Registry** Storage for Docker images

The following steps illustrate how to create these services from the Azure Portal (https://portal.azure.com).  We 
use default settings for service creation except where noted. 

--------------------------
Create Team Command
--------------------------

You start by creating the 6 Azure services, by running the **xt create team** command.  It generates an Azure template that you run in the Azure Portal.  For details, see the :ref:`Create Team Command <create_team>` description.

---------------------------------------------------
Creating the Vault Secret
---------------------------------------------------

Create a single secret (containing the keys for 4 of your services) and add it to your vault.  Part of the task involves accessing your newly created Azure services.  To access services in the Azure Portal, we suggest:

    - click on "Resource groups" in the left-most sidebar 
    - click on your team resource group
    - find and click on the desired service (ignore the service names with extra text appended to them)

1. Using a code or text editor, paste the following JSON dictionary string into an empty file::

    { 
        "phoenixstorage": "key",   
        "phoenixmongodb": "key",  
        "phonenixbatch": "key", 
        "phoenixregistry": "key"
    }

2. Replace each of the service names in the above with your Azure service names (suggestion: do an editor search & replace of "phoenix" to your team name).

3. For each of the "key" strings, replace them with the associated service key or connection string values.  For this step, you  navigate to each service in the Azure Portal, click on the **Keys** or **Connection string** tab in the left side panel, and copy the primary key or connection string value:

    a. for the Storage service:
        - navigate to your storage service
        - click on the "Access Keys" tab in the service's side panel
        - click on the "Key 1" copy-to-clipboard button
        - paste into your editor for the storage service key value 

    b. for the Mongo DB service:
        - navigate to your mongodb service
        - click on the "Connection string" tab in the service's side panel
        - click on the "PRIMARY CONNECTION STRING" copy-to-clipboard button
        - paste into your editor for the mongodb key value 

    c. for the Azure Batch service:
        - navigate to your batch service
        - click on the "Keys" tab in the service's side panel
        - click on the "Primary access key" copy-to-clipboard button
        - paste into your editor for the batch key value 

    d. for the Container Registry service:
        - navigate to your registry service
        - click on the "Access Keys" tab in the service's side panel
        - click on the "Enable" Admin User button
        - click on the "Password" copy-to-clipboard button
        - paste into your editor for the registry service key value 

4. From your code/text editor, copy the JSON dictionary string that you modified (both service names and keys) into your clipboard

5. In the Azure Portal::

    - navigate to your team Key Vault service 
    - click on the "Secrets" sidebar tab
    - click on the "+ Generate/Import" button
    - for "Name", enter "xt-keys"
    - for "Value", paste it the clipboard string (of your JSON dictionary)
    - click on "Create"

6. Finally, clean up::

    - note the filename associated with the JSON dictionary string in your editor (if any)
    - close JSON dictionary string file in your editor
    - delete the file from your local hard drive (if it exists)

---------------------------------------------------
Adding the XT certs to the vault
---------------------------------------------------

1. In the Azure Portal::

    - navigate to your team Key Vault service 
    - click on the "Certificates" tab in the service sidebar 

    a. create the CLIENT CERT
    - click on the "+ Generate/Import" button
    - for "Method of Certificate Creation", select "Generate"
    - for "Certificate Name", enter "xt-clientcert"
    - for "Subject", enter "CN-xtclient.com"
    - for "Content Type", change it to "PEM"
    - click on "Create"

    b. create the SERVER CERT
    - click on the "+ Generate/Import" button
    - for "Method of Certificate Creation", select "Generate"
    - for "Certificate Name", enter "xt-servercert"
    - for "Subject", enter "CN-xtserver.com"
    - for "Content Type", change it to "PEM"
    - click on "Create"


-----------------------------------------------------------
Create a Compute Instance for your AML service
-----------------------------------------------------------

1. Navigate to your Azure ML service

#. Select the "Compute" tab button in the service sidebar.

#. Click the "+ New" button.

#. For "Compute Name", we suggest the team name followed by "compute" (e.g., phoenixcompute).

#. For "Virtual Machine Size", select the CPU/GPU configuration for the VMs your service will use.

#. Click "Create"


-----------------------------------------------------------
Editing your local XT config file 
-----------------------------------------------------------

To edit your local XT config file ('xt config' cmd), do the following:

1. Copy/paste the following sections (or merge them with existing sections of the same name)::

    external-services:
        phoenixbatch: {type: "batch", key: "$vault", url: "xxx"}
        phoenixaml: {type: "aml", subscription-id: "xxx", resource-group: "phoenix"}
        phoenixstorage: {type: "storage", provider: "azure-blob-21", key: "$vault"}
        phoenixmongodb: {type: "mongo", mongo-connection-string: "$vault"}
        phoenixkeyvault: {type: "vault", url: "xxx"}
        phoenixregistry: {type: "registry", login-server: "xxx", username: "xxx", password: "$vault", login: "true"}

    xt-services:
        storage: "phoenixstorage"        # storage for all services 
        mongo: "phoenixmongodb"          # database used for all runs across services
        vault: "phoenixkeyvault"         # where to keep sensitive data (service credentials)

    compute-targets:
        batch: {service: "phoenixbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm", docker: "none"}
        philly: {service: "philly", vc: "msrlabs", cluster: "rr2", sku: "G1", nodes: 1, low-pri: true}
        aml: {service: "phoenixaml", compute: "xxx", vm-size: "Standard_NC6", nodes: 1, low-pri: false}

    general:
        workspace: "xxx"
        experiment: "xxx"
        primary-metric: "test-acc"             # name of metric to optimize in roll-ups, hyperparameter search, and early stopping
        maximize-metric: true                  # how primary metric is aggregated for hp search, hp explorer, early stopping 
        xt-team-name: "phoenix"                # for use with XT Grok
        bigbatch: {service: "labcoatbatch", vm-size: "Standard_NC6", azure-image: "dsvm", nodes: 1, low-pri: true,  box-class: "dsvm"}
        pip-packages: ["torch==1.2.0", "torchvision==0.4.1", "Pillow==6.2.0", "watchdog==0.9.0", "seaborn", "pandas", "xtlib==*"]       # packages to be installed by pip (xtlib, etc.)

    setups:
        local: {activate: "$call conda activate $current_conda_env", conda-packages: [], pip-packages: ["xtlib==*"]}
        py36: {activate: "$call conda activate py36", conda-packages: [], pip-packages: ["xtlib==*"]}
        aml: {pip-packages: ["torch==1.2.0", "torchvision==0.4.1", "Pillow==6.2.0", "watchdog==0.9.0", "xtlib==*"] }

#. Replace all occurences of "phoenix" with the name of your team  

#. Replace all "xxx" values with the associated property of the specified service, using information from the Azure Portal.

#. For the "compute-targets" and "general" sections, review the settings and edit as needed.  See the XT Config File help topic for additional information about these properties.

-----------------------------------------------------------
Test your new team
-----------------------------------------------------------

Test your new XT team configuration by running XT in the directory that contains your local XT config file.  Try the
following commands in the specified order::

    - xt list workspaces:
        - this will test that your Key Value and Storage services are configured correctly
        - if an error occurs here, double check the Key Vault service properties and XT configuration file properties for these services

    - xt create workspace ws-test 
        - this will ensure your Storage account is writable 
        - if you see an error here about "Block blobs are not supported", you likely selected the wrong version of the storage "kind" property.  If this is the case,
          you will need to recreate the storage services.

    - xt run <script>
        - this will ensure that the Mongo DB service is configured correctly
        - if you see the error "getaddrinfo failed", you likely have specified the wrong connection string for mongodb.  if so, you 
          will have to update the xt-keys secret in the vault.

    - xt run --target=batch <script>
        - this will ensure that the Batch service is configured correctly

    - xt run --target=aml <script>
        - this will ensure that the Batch service is configured correctly


If you need to recreate 1 or more of the services::

    - delete the old service.
    - create the new service using the same name.  Note: some services may take 5-10 minutes before the name can be reused.
    - get the keys string from the "xt-keys" secret in the Key Vault.
    - use an editor to update the keys for any new services.
    - create a new version of the xt-keys secret with the updated JSON dictionary string.
    - on your local machine, be sure to run "xt kill cache" before trying further testing.

.. seealso:: 

    - :ref:`create team cmd <create_team>`
    - :ref:`XT Config file <xt_config_file>`
    - :ref:`Preparing A New Project <prepare_new_project>`
    - :ref:`Manually Creating the XT Services <manual_service_creation>`

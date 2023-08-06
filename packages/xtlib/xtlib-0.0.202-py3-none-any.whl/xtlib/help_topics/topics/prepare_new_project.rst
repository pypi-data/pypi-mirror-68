.. _prepare_new_project:

========================================
Preparing a new project for XT 
========================================

This page describes how to prepare a new project to be used with XT.  

This assumes you already have configured XT for a set of services (storage, compute, etc.) - either done
by you or your team adminstrator.  If this step hasn't been done yet, refer to the link at the bottom of this page.

Preparing a new project for XT consists of 3 overall steps:
    - adding code to your ML app for XT logging, checkpointing, and data/model loading
    - uploading your dataset and model to XT shares
    - creating a new local XT config file for your project
    

In the following sections, those that being with "Code:" describe the code changes you should consider making to your ML app. 
Those that being with "Upload:" describe files that you should consider uploading to your XT storage.  Finally, those
sections that being with "Config:" describe changes you should consider making to your XT config file.

----------------------------------------
Code: Benefits of Code Changes for XT
----------------------------------------

You can run your ML scripts under XT without changing any of the code, but by adding a small set of code snippets, 
you can realize several benefits:

    - uniform access to local and cloud-resident datasets and models 
    - easy model checkpointing
    - centralized logging for hyperparameters and metrics 
    - hyperparameter searches
    - run and job reports that reflect your project's hyperparameters and metrics
    - ad-hoc plots with your project's metrics

---------------------------------
Code: Creating an XT Run Object
---------------------------------

The first step is to create an XT Run object.  With an XT Run object, your ML app can log hyperparameter settings, 
train and test metrics, and upload or download needed files.  The recommended snippet for creating an XT
run object is::

    from xtlib.run import Run
    xt_run = Run(tb_path="logs")

This will create an instance of Run that is enabled for XT and Tensorboard logging.  If you want to 
do your own Tensorboard logging, you can omit the **tb_path** argument.

------------------------------
Code: Hyperparameter Logging 
------------------------------

To log the value of your hyperparameters, you will pass a dictionary of hyperparameter names and their values.  If
you use command line arguments for your hyperparameters and parse them with the **argsparse** library, we recommend 
the following snippet::

        # log hyperparameters to XT
        if xt_run:
            xt_run.log_hparams( argv.__dict__ )

If you don't already have your hyperparameters in their own dictionary, we recommend a snippet like the following, but
with your app's actual hyperparameter names and values:

        # log hyperparameters to XT
        if xt_run:
            hp_dict = {"seed": seed, "batch-size": batch_size, "epochs": epochs, "lr": lr, 
                "momentum": momentum, "channels1": channels1, "channels2": channels2, "kernel_size": kernel_size, 
                    "mlp-units": mlp_units, "weight-decay": weight_decay, "optimizer": optimizer, 
                    "mid-conv": mid_conv, "gpu": gpu, "log-interval": log_interval}

            xt_run.log_hparams(hp_dict)

You should place your hyperparameter logging snipper after the creation of the xt_run object, but before
your ML app starts its training operation.  If your ML app is not doing training, you can skip the logging of 
hyperparameters.

------------------------
Code: Metrics Logging
------------------------

Here is an example code snippet for logging metrics during training, but it will need to modified to reflect your app's actual metric
names and values:

        if xt_run:
            # log TRAINING stats to XT
            xt_run.log_metrics({"epoch": epoch, "loss": train_loss, "acc": train_acc}, step_name="epoch", stage="train")

In the above snippet, if you use **step** or another name for each interval of training, you should replace the 3 
instances of "epoch" with your interval name.  

Likewise, here is an example of logging metrics during evaluation (it will also need to be modified):

        if xt_run:
            # log EVAL stats to XT
            xt_run.log_metrics({"epoch": epoch, "loss": eval_loss, "acc": eval_acc}, step_name="epoch", stage="eval")

Since these logging calls result in cloud-based database access, it is recommended that you don't log too often (for example, 
no more than once every 30 seconds).  

------------------------
Code: XT_DATA_DIR
------------------------

When you job starts to run on a compute node, XT can optionally map a local path to the data share path of your project's 
dataset.  Alternately, it can download your dataset to a local path.  Both of the actions are controlled by the **data** 
section of your XT config file.  

To enable your ML app to access the mapped or downloaded data, XT sets the environment variable **XT_DATA_DIR** to the local
path of the data.  We recommend the following code snippet to get the path to your dataset::

    data_dir = os.getenv("XT_DATA_DIR", args.data)

The above snippet will use the **XT_DATA_DIR** as the data directory if XT has set it, otherwise, it will use the 
parsed command line argument for **data** (in this example).  You should change **args.data** above to be the location
of your dataset on your local machine, as needed.

------------------------
Code: XT_MODEL_DIR
------------------------

This section pertains to scnarios where you want to upload a model to a model share (cloud storage) and then direct your 
ML app to use that model (for evaluation or model analysis, for example).  For checkpointing model loading, please
refer to the **checkpoint** section below.

When you job starts to run on a compute node, XT can optionally map a local path to the model share path of your project's 
model file(s).  Alternately, it can download your model to a local path.  Both of the actions are controlled by the **model** 
section of your XT config file.  

To enable your ML app to access the mapped or downloaded model, XT sets the environment variable **XT_MODEL_DIR** to the local
path of the model.  We recommend the following code snippet to get the path to your model::

    model_dir = os.getenv("XT_MODEL_DIR", args.model)

The above snippet will use the **XT_MODEL_DIR** as the model directory if XT has set it, otherwise, it will use the 
parsed command line argument for **model** (in this example).  You should change **args.model** above to be the location
of your model on your local machine, as needed.

------------------------
Code: XT_OUTPUT_DIR
------------------------

When you job starts to run on a compute node (backend service or a Linux VM), XT will map your run's storage location in the cloud to a local path and 
set the environment variable **XT_OUTPUT_DIR** to that value.  You can use this path to write your output logs and anything you would 
like to be written saved to the cloud before your run completes.  Note that there is a separate mechanism for capturing selected files
when your job has competed (the **after-files** section of the XT config file controls this).

The recommended snippet for getting the value of the **XT_OUTPUT_DIR** is::

    output_dir = os.getenv("XT_OUTPUT_DIR", "output")

The above snippet will use the **XT_OUTPUT_DIR** as the output directory if XT has set it, otherwise, it will use the 
directory **output** (in this example).  You should change **output** above to be the location on your local machine that
you use for output files, as needed.

If you are doing your own explict Tensorboard logging to the **XT_OUTPUT_DIR**, you will need an additional code snippet
to have Tensorboard logging work as expected.  Please use the **Tensorboard** link at the bottom of the page for more details.

------------------------
Code: Checkpointing
------------------------

Checkpointing your model is an ML best practice, and a must if you are running on preemptable nodes, where your job can 
get interrupted and restarted at any time.

You can use your output directory from **XT_OUTPUT_DIR** to check for the existence of a model at the beginning of your run.  If found,
you can safely assume your run has been restarted and load the model to continue your training. 

Here is our recommended snippet to load a PyTorch model from your output directory::

    fn_model = os.path.join(output_dir, "model.pt")
    if os.path.exists(fn_model):
        model.load_state_dict(torch.load(fn_checkpoint))


In addition, you should save your model to your output directory occasionally (for example, every 30 minutes), so that you 
have a recent model to restart from.

Here is our recommended snippet to save a PyTorch model to your output directory::

    fn_model = os.path.join(output_dir, "model.pt")
    torch.save(model.state_dict(), fn_model)

------------------------
Code: Run Script
------------------------

Normally, you specify your run's environment and datset dependencies in your XT config file, and in your XT run command, you 
specify your app's main python script.

Alternately, you can specify a Shell script (or Windows .bat file) with the run command.  Doing so enables you to run any code needed to
initialize the compute node for your app (generate datasets, installing dependencies, etc).  It also allows you to do 
custom post-processing after your python script has completed.

Here is a simple example of such a shell script::

    conda activate py37_torch
    pip install -r requirements.txt
    python myscript.py  --epochs=125  --lr=.02

Note: using a run script is optional; the pre and post dependencies for most jobs can be handled by the settings in the XT config file.

------------------------
Upload: Dataset 
------------------------

If you job needs to access a dataset when it runs, you will want do a one-time upload of the dataset to your XT data share.  The
following command is an example of how to upload your dataset::

    xt upload data/MNIST/** MNIST --share=data

The above commands uploads the files found in the local directory **data/MNIST** to the MNIST path on your XT data share.  

After the command completes, you can verify your data is in the data share with this command::

    xt list blobs MNIST --share=data --subdir=-1 

------------------------
Upload: Model
------------------------

If you job needs to access a model when it runs (for evaluation or analysis), you can do a an upload of the model to your XT models share.  The
following command is an example of how to upload your model::

    xt upload models/MNIST/** MNIST --share=models

The above commands uploads the model file(s) found in the local directory **models/MNIST** to the MNIST path on your XT models share.  

After the command completes, you can verify your model is in the models share with this command::

    xt list blobs MNIST --share=models --subdir=-1 

--------------------------------------
Config: Copying to your new project
--------------------------------------

For this step, you should first identify the working directory of your new project.  This
is the directory of your project from which your typically start a training or eval run.

Next, you should copy your **xt_config.yaml** file from one of your previous XT projects
to your new project's working directory.  

If this is your first project, you can copy the **xt_config.yaml** file that was created during 
the creation of your XT services.  If you are using a set of pre-configured Sandbox services, 
you can start with a empty **xt_config.yaml** file.  

For editing your XT config file in the following steps, you can use your favorite editor or 
the **xt config** command.

--------------------------------------
Config: target.docker property 
--------------------------------------

Docker is a tool that enable you to capture all of the software dependencies of an complex 
application and reassemble them on the same or another computer, so the application runs
as expected.  

If your ML app is going to run in a docker container image, you will need to ensure that
the **docker** property of the **compute-target** you will be using has been set to the an 
entry in the **dockers** section that describes your docker image.  For more information,
refer to the **XT and Docker** link at the bottom of this page.

--------------------------------------
Config: target.setup property 
--------------------------------------

The **setup** property of a **compute-target** specifies an entry in the **setups** section.
These **setup** entries define how to configure a compute node to be able run your ML app.

You should ensure that the **setup** referred to by the **compute-target** that your project will 
use correctly specifies the steps needed to configure a node of the **compute-target**.

Refer to the **XT Config File** link at the bottom of the page for more details on the
**setups** section.

--------------------------------------
Config: general.workspace property 
--------------------------------------

For your new project, you may want to change the name of your default workspace. A workspace
is like a folder where your XT runs and experiments are stored.

Workspace names are limited by the rules of Azure storage container names::

    A blob container name must be between 3 and 63 characters in length; 
    start with a letter or number; and contain only letters, numbers, 
    and the hyphen. All letters used in blob container names must be lowercase.

--------------------------------------
Config: general.experiment property 
--------------------------------------

An XT experiment name is a string that you can associate with XT jobs when you 
submit them (with the **run** command).  If you don't specify an experiment name on
the command line, it will use the value of the general.experiment property in the 
XT config file.

For your new project, you may want to change the experment name.

-----------------------------------------
Config: general.primary-metric property 
-----------------------------------------

If you are plan to perform XT hyperparameter searches, you should set the 
**primary-metric** property to the name of the metric that to  be 
used by the hyperparameter search algorithm to select more promising 
hyperparameter sets on each search.  

-----------------------------------------
Config: general.maximize-metric property 
-----------------------------------------

If you are plan to perform XT hyperparameter searches, you should set the 
**maximize-metric** property to **true** if the higher values of the **primary-metric**
are desired (for example **accuracy**) and to **false** otherwise (for example, **loss**).

--------------------------------------
Config: code section
--------------------------------------

The **code** section defines which files should be uploaded to each compute node
for the ML run to proceed.  The primary settings here are a list of directories or 
file wildcards to upload, and a list of wildcard names to omit from uploading.

You should review the **code** settings and ensure they are correct for your 
new project.

See the **XT Config file** link at the bottom of this page for more details 
on the **code** section.

--------------------------------------
Config: after-files section
--------------------------------------

The **after-files** section defines which files should be uploaded from each compute node
at the completion of your ML app.  The primary settings here are a list of directories or 
file wildcards to upload, and a list of wildcard names to omit from uploading.

You should review the **after-files** settings and ensure they are correct for your 
new project.

See the **XT Config file** link at the bottom of this page for more details 
on the **after-files** section.

--------------------------------------
Config: data section
--------------------------------------

If you would like your app to have access to a dataset that you have uploaded,
you should set the **data-share-path** property (in the **data** section) to the path on the data share 
where you have uploaded the dataset.  Then you should set **data-action** to 
either **mount** (if you want to access the data thru a mapped drive) or **download** 
(if you want to access the data as actual local files).  If you need to open your 
dataset files multiple times during a run, we recommend that you use the 
**download** value.

--------------------------------------
Config: model section
--------------------------------------

If you would like your app to have access to a model that you have uploaded,
you should set the **model-share-path** property (in the **model** section) to the path on the models share 
where you have uploaded the model.  Then you should set **model-action** to 
either **mount** (if you want to access the model thru a mapped drive) or **download** 
(if you want to access the model as actual local files).  If you need to open your 
model files multiple times during a run, we recommend that you use the 
**download** value.

--------------------------------------
Config: run-reports section
--------------------------------------

Use the **columns** property of the **run-reports** section to specify the hyperparameters and metrics
of your new project that will be shown as columns in the **list runs** command.  
Be sure to prefix hyperparameter names by **hparams.** and metric names by **metrics.**.

You can also use these string to specify column aliases and column formatting.  For more information, refer
to the **XT Config File** link at the bottom of this page.

--------------------------------------
Config: tensorboard section
--------------------------------------

Use the **template** property of the **tensorboard** section to specify the standard run columns, hyperparameter
values, and literal strings that you want to appear in tensorboard for each log file. This helps you associate logs
with the runs they represent, and can also be used to filter the logs by hyperparameter values and other properties.

For more information, refer to the **XT Config File** link at the bottom of this page.

--------------------------------------
Config: aml-options section
--------------------------------------

If your new project will be using Azure Machine Leaarning, you may want to specify your ML **framework**, the **fw-version**, 
and **distributed-training** properties in the **aml-options** section.

For more information, refer to the **XT Config File** link at the bottom of this page.

--------------------------------------
Config: early-stopping section
--------------------------------------

If your new project will be using Azure Machine Leaarning and are doing AML hyperparameter searches,
you may want to specify properties in the **early-stopping** section to control how unpromosing runs
can be detected and terminated early in their training.

For more information, refer to the **XT Config File** link at the bottom of this page.

.. seealso:: 

    - :ref:`Creating XT Services <creating_xt_services>` 
    - :ref:`Azure VM sizes<https://docs.microsoft.com/en-us/azure/virtual-machines/linux/sizes>`
    - :ref:`xt config command <config>` 
    - :ref:`XT config file<xt_config_file>` 
    - :ref:`Using Tensorboard with XT<tensorboard>` 
    - :ref:`XT and Docker XT<xt_and_docker>` 

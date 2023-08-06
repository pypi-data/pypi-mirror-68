.. _getting_started:

========================================
Getting Started with XT
========================================

XT is a command line tool to manage and scale machine learning experiments, with a 
uniform model of workspaces and runs, across a variety of compute services.  It includes
services like live and post Tensorboard viewing, hyperparameter searching :ref:`hyperparameter searching <hyperparameter_search>`, and ad-hoc plotting.

-----------------------
XT Requirements
-----------------------

Requirements for installing and running XT are:
    - Windows or Linux OS
    - Python 3.5 or later   (recommended: Python 3.6)
    - Anaconda or other virtual Python environment (recommended: Anaconda)
    - User must have an Azure account (required for authenticated access to Azure computing storage and resources)
    - For Linux users who will be using the Microsoft internal Philly services, you should install **curl**::

        https://www.cyberciti.biz/faq/how-to-install-curl-command-on-a-ubuntu-linux/

----------------------------------
XT's Core Services
----------------------------------

XT has many machine learning features and commands, which revolve around three core operations:

+------------+------------+-----------+-----------+-----------+-----------+-----------+--+
| Core Operations         | Description                       | Azure Services Used      |
+============+============+===========+===========+===========+===========+===========+==+
| **Job submissions**     | Submit and run jobs with XT.      | Azure ML, Azure Batch    |
+------------+------------+-----------+-----------+-----------+-----------+-----------+--+
| **Experiment            | Jobs store their data artifacts in| Azure Storage,           |
| Storage**               | your Azure Storage Service.       | Container Registry       |
+------------+------------+-----------+-----------+-----------+-----------+-----------+--+
| **Experiment            | Stats include Job properties, Run | Azure Storage, MongoDB   |
| Statistics**            | properties, metrics, and          |                          |
|                         | hyperparameter settings.          |                          |
+------------+------------+-----------+-----------+-----------+-----------+-----------+--+

In this documentation, you will learn how to install and use all of these cloud services with XT.

.. Note:: XT supports all Machine Learning frameworks. The following procedure installs PyTorch because it supports the XT demo. 

------------------
Installing XT
------------------

XT package installation is straightforward. Follow these steps to set up XT on your computer. You may `need to install Anaconda <https://www.anaconda.com/distribution/>`_ on your system in order to follow these steps:

    **1. PREPARE a conda virtual environment with PyTorch (only need to do this once):**
        
        .. code-block::

            > conda create -n MyEnvName python=3.6
            > conda activate MyEnvName
            > conda install pytorch torchvision cudatoolkit=10.1 -c pytorch

    **2. INSTALL XT:**

        .. code-block::

            > pip install -U xtlib

------------
Next Steps
------------

After installation, we recommend running the **XT demo**.  It walks you through
executing a series of XT commands that demonstate it as an ML platform. See :ref:`Run the XT Demo <xt_demo>` for more information.

To learn more about running jobs using the **xt run** command, see :ref:`XT run command <run>`.
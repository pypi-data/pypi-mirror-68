.. _xt_cmd_piping:

========================================
XT Command Piping
========================================

Two XT commands support query options: **xt list runs** and **xt_list_jobs**.  Several other XT commands accept a list of runs or jobs, but don't support the same query options.

For commands that don't support query options, you can use *command line piping* to pipe runs or jobs matched by a query command to another XT command. You can use them in Windows or Linux command lines.

Consider a case where you want to take the top 15 highest scoring runs and tag them with "top15".  Use the **xt list runs** command with the necessary filters and sorting, and then copy/paste (or read and type) the run names into the "set tags" command.

With XT command piping, you can do this in one step. A *pipe* symbol (|) enables you to chain two XT commands to achieve a result:

        .. code-block::

            > xt list runs --sort=metrics.test-acc --last=15 | xt set tags $ top15

In the  *xt set tags* command, we specify a '$' in the location where we want the run names from the first command to be inserted.  The '$' is required; without it, names from the incoming command will be ignored.

Consider a case where you include the most recently completed 10 runs in a set of plots.  This can be done with the following command:

        .. code-block::

            > xt list runs --status=completed --last=10 | xt plot $ train-acc, test-acc --layout=2x5

After the pipe, the **xt plot** command receives the specified data and formats it into a table.

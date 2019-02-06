#!usr/bin/env python

class pbs:
    """It creates sbatch files needed to run Gaussian jobs"""

    def __init__(self,base_name = 'input', walltime = '24:00:00', nodes = 1, task_per_node = '16',
                 email = 'jcgarcia@anl.gov', ):

        self.walltime = walltime
        self.nodes= nodes
        self.task_per_node = task_per_node
        self.email = email
        self.base_name = base_name
        self.header  = ("#!/bin/bash\n\n"
                        "#PBS -N {0}\n"
                        "#PBS -l walltime={1}\n"
                        "#PBS -l nodes={2}:ppn={3}\n" 
                        "#PBS -j oe\n" 
                        "#PBS -m bea\n" 
                        "#PBS -M {4}\n").format(self.base_name,self.walltime,self.nodes,
                                                  self.task_per_node,self.email)
        self.body    = ("\nnp=`wc -l < $PBS_NODEFILE`\n" 
                        "nn=`sort -u $PBS_NODEFILE | wc -l`\n" 
                        "node_list=`sort -u $PBS_NODEFILE | paste -s -d','`\n" 
                        "let shared=np/nn\n" 
                        "echo Number of nodes is $nn\n" 
                        "echo Number of processors is $np\n" 
                        "echo Node list is $node_list\n\n" 
                        "cd $PBS_O_WORKDIR\n\n" 
                        "echo '%NProcShared='$shared > header\n" 
                        "echo '%LindaWorkers='$node_list >> header\n\n" 
                        "export GAUSS_SCRDIR=$TMPDIR\n\n"
                        "cat header {0}.com | g09 > {0}.log" ).format(self.base_name)

    def write_file(self,filename):
        submit_file = open(filename,'w')
        submit_file.write(self.header)
        submit_file.write(self.body)
        submit_file.close()



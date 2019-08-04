import networkx as nx

class FMP_algo:

    def __init__(self,graph):
        self.map={}
        self.graph=graph

    def start(self,gene1,gene2,max_length):
        """
        :param gene1:
        :param gene2:
        :param max_length: max length of meta path.
        :return:score_list
                like [
                {
                'mPath': 'GMDMG',
                'score': 0.4,
                'ins': 3,   instance of meta Path
                'gene1': 'G:HGNC:17256',
                'gene2': 'G:HGNC:21497'
                }
                ]
        """
        self.map = {}
        graph = self.graph
        max_step=max_length-1
        meta_paths=self.find_meta_paths(gene1,gene2,graph,max_step)
        if len(meta_paths)==0:
            print("there is no meta paths between " + gene1 + " and " + gene2)
            return []
        return meta_paths

    def is_connected(self,gene1,gene2,graph,max_step):
        """
        Check if the two gene node is connected or not.
        Find a shortest path between two nodes.
        Return False if there is no path or the length of the path is
        longer than the max step.
        :param gene1:
        :param gene2:
        :param graph:
        :param max_step:
        :return:True,False
        """

        try:
            sp = nx.astar_path_length(graph, gene1, gene2)
        except:
            return False

        if sp>max_step:
            return False
        else:
            return True

    def find_meta_paths(self,gene1,gene2,graph,max_step):
        """
        Find all meta paths between two nodes within max_step.
        Meanwhile record all the meta paths which connect each nodes
        to the center node, in order to compute the score after.
        :param gene1:
        :param gene2:
        :param graph:
        :param max_step:
        :return:mPaths: meta paths between gene1 and gene2
                hmPaths: meta paths between gene1 and center nodes
                tmPaths: meta paths between gene2 and center nodes
        """
        self.find_meta_paths_between_g1_g2(gene1, gene2, graph,max_step, self.get_node_type(gene1), {})
        mPaths =self.map
        return mPaths

    def find_meta_paths_between_g1_g2(self,gene1,gene2,graph,k,mPathName,old_node=None):
        """
        Find all meta paths between two nodes within max_step.
        The loop stops only when k = 0.
        And the paths it find restore in self.map.
        :param gene1:
        :param gene2:
        :param graph:
        :param k:
        :param mPathName:
        :param old_node:
        :return: None
        """
        if k==0:
            return 0
        else:
            k-=1
        for neighbors in graph.neighbors(gene1):
            # avoid creating circle in the meta path
            if neighbors==old_node:
                continue
            type2=self.get_node_type(neighbors)
            mPathName2=mPathName+type2
            # find a meta path, then record it in dict and do the pruning as the same time.
            if neighbors == gene2:
                if self.map.__contains__(mPathName2):
                    self.map[mPathName2]+=1
                else:
                    self.map[mPathName2]=1
                continue
            # use pruning strategy
            if self.pruning(mPathName2):
                continue

            self.find_meta_paths_between_g1_g2(neighbors,gene2,graph,k,mPathName2,gene1)
    def pruning(self,mPathName):
        """
        pruning strategy
        use the pruning strategy to reduce the searching space
        :param mPathName: String
        :return: True or False
        """
        if mPathName[-1]=="G":
            return True
        else:
            return False
    def get_node_type(self,node):
        """
        Get node type
        :param node:
        :return: type
        """
        type=node[0]
        return type



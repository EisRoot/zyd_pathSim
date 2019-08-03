from build_graph import init_graph
import networkx as nx

import math

class zyd_pathSim_algo:
    """
    1.score阈值，超过既定的阈值的pair可以直接舍弃掉；或者没有我们所要的meta_path的pair也可以舍弃掉

    """

    def __init__(self):
        self.map={}
        self.map1={}
        self.map2={}

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
        self.map1 = {}
        self.map2 = {}

        graph = init_graph()
        max_step=max_length-1

        if not self.is_connected(gene1,gene2,graph,max_step):
            print( "there is no meta paths between "+gene1+" and "+gene2)
            return []
        meta_paths, meta_paths_from_gene1, meta_path_from_gene2=self.find_meta_paths(gene1,gene2,graph,max_step)
        if len(meta_paths)==0:
            return []
        score_list=self.score(meta_paths,meta_paths_from_gene1,meta_path_from_gene2)
        for i in score_list:
            i['gene1']=gene1
            i['gene2']=gene2
        return score_list

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
        center=int(max_step/2)
        self.find_meta_paths_between_g1_g2(gene1, gene2, graph,max_step, self.get_node_type(gene1), {})
        mPaths =self.map
        if len(mPaths)==0:
            return [],[],[]


        self.find_meta_paths_g1_center(gene1, graph, center, self.get_node_type(gene1))
        hmPaths = self.map1
        self.find_meta_paths_g2_center(gene2, graph, center, self.get_node_type(gene2))
        tmPaths = self.map2


        return mPaths,hmPaths,tmPaths

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

    def find_meta_paths_g1_center(self, gene, graph, k, mPathName, old_node=None):
        """
        Find all meta paths between two nodes within max_step.
        The loop stops only when k = 0.
        And the paths it find restore in self.map1.
        :param gene:
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

        for neighbors in graph.neighbors(gene):
            # avoid creating circle in the meta path
            if neighbors == old_node:
                continue
            type2=self.get_node_type(neighbors)
            mPathName2=mPathName+type2
            #use pruning strategy
            if self.pruning(mPathName2):
                continue
            if self.map1.__contains__(mPathName2):
                self.map1[mPathName2]+=1
            else:
                self.map1[mPathName2]=1
            self.find_meta_paths_g1_center(neighbors, graph, k, mPathName2, gene)

    def find_meta_paths_g2_center(self, gene, graph, k, mPathName, old_node=None):
        """
        Find all meta paths between two nodes within max_step.
        The loop stops only when k = 0.
        And the paths it find restore in self.map2.
        :param gene:
        :param graph:
        :param k:
        :param mPathName:
        :param old_node:
        :return: None
        """
        if k == 0:
            return 0
        else:
            k -= 1
        for neighbors in graph.neighbors(gene):
            # avoid creating circle in the meta path
            if neighbors == old_node:
                continue
            type2 = self.get_node_type(neighbors)
            mPathName2 = mPathName + type2
            # use pruning strategy
            if self.pruning(mPathName2):
                continue
            if self.map2.__contains__(mPathName2):
                self.map2[mPathName2] += 1
            else:
                self.map2[mPathName2] = 1

            self.find_meta_paths_g2_center(neighbors, graph, k, mPathName2, gene)

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

    def parse_meta_path_dict(self,mPaths):
        list=[]
        for mPath,ins in mPaths.items():
            hmPath,tmPath=self.cut_meta_path(mPath)
            list.append({
                'mPath':mPath,
                'ins':ins,
                'hmPath':hmPath,
                'tmPath':tmPath
            })
        return list

    def get_ins_of_meta_path(self,mPath,mPathDict):
        ins=mPathDict[mPath]
        return ins

    def cut_meta_path(self,mPath):
        """
        Cut meta_path string into two part.
        One is a meta_path from the started gene node to the center node.
        Another is from the ended gene node.
        For example, input mPath like 'GDPdG' and the output are 'GDP' and 'Gdp"
        :param mPath:
        :return: head2center,tail2center
        """
        le=len(mPath)
        if le%2==0:
            # 'GDDG'
            center=int(le/2)
            head2center=mPath[0:center]
            tail2center=mPath[center:le][::-1]
            return head2center,tail2center
        else:
            #'GDG' 'GDPG
            center = math.floor(le / 2)
            head2center=mPath[0:center+1]
            tail2center=mPath[center:le][::-1]
            return head2center,tail2center

    def score(self,mPaths,mPathDict1,mPathDict2):
        """

        :param mPaths: meta paths between gene1 and gene2
        :param mPathDict1: meta paths between gene1 and center nodes
        :param mPathDict2: meta paths between gene2 and center nodes
        :return: score_list:
        """
        score_list=[]
        list=self.parse_meta_path_dict(mPaths)
        for a in list:
            mPath=a['mPath']
            ins=a['ins']
            hmPath=a['hmPath']
            tmPath=a['tmPath']
            hmIns=self.get_ins_of_meta_path(hmPath,mPathDict1)
            tmIns=self.get_ins_of_meta_path(tmPath,mPathDict2)
            score=self.score_kernal_function(ins,hmIns,tmIns)
            score_list.append({
                'mPath':mPath,
                'score':score,
                'ins':ins
            })

        return score_list

    def score_kernal_function(self,ins,hmIns,tmIns):
        """
        The score function
        :param ins: instance of meta path
        :param hmIns: instance of meta path from head to center node
        :param tmIns: instance of meta path from tail to center node
        :return: score
        """
        score=2*ins/(hmIns+tmIns)
        return score



from collections import deque
import sys
import time
import matplotlib.pyplot as plt

class AhoCorasick:
    def __init__(self, keywords):
        # Create the root node of the trie
        self.root = {'next': {}, 'fail': None, 'output': set()}
        
        # Add each keyword to the trie
        for keyword in keywords:
            current_node = self.root
            for char in keyword:
                if char not in current_node['next']:
                    current_node['next'][char] = {'next': {}, 'fail': None, 'output': set()}
                current_node = current_node['next'][char]
            current_node['output'].add(keyword)
        #print(self.root)
        # Compute the fail function for each node in the trie
        self.fail()
        
    def fail(self):
        queue = deque()
        for char, node in self.root['next'].items():
            queue.append(node)
            node['fail'] = self.root
        while queue:
            current_node = queue.popleft()
            for char, child_node in current_node['next'].items():
                queue.append(child_node)
                fail_node = current_node['fail']
                while fail_node is not None and char not in fail_node['next']:
                    fail_node = fail_node['fail']
                child_node['fail'] = fail_node['next'][char] if fail_node else self.root
                child_node['output'].update(child_node['fail']['output'])
    
    def search(self, text):
        current_node = self.root
        results = []
        for i, char in enumerate(text):
            while current_node is not None and char not in current_node['next']:
                current_node = current_node['fail']
            if current_node is None:
                current_node = self.root
                continue
            current_node = current_node['next'][char]
            results.extend(current_node['output'])
        return results
    
def main():
    #args = sys.argv
    apoe_file = "apoe.txt"
    dna_one = "GCA_000002125.2_HuRef_genomic.fna"
    dna_two = "GCA_000004845.2_YH_2.0_genomic.fna"
    dna_three = "GCF_000306695.2_CHM1_1.1_genomic.fna"
    dna_four = "GCA_009914755.4_T2T-CHM13v2.0_genomic.fna"
    dna_five = "GCF_000001405.40_GRCh38.p14_genomic.fna"
    list_of_dna = [dna_one, dna_two, dna_three, dna_four, dna_five]

    f = open(apoe_file)
    apoe = ""

    for char in f.read():
        if char != "\n":
            apoe += char

    for dna in list_of_dna:
        human_genome = ""
        pre_process_start = time.time()
        with open(dna, 'r') as file:
            human_genome = file.read().replace('\n', '')
        pre_process_end = time.time()
        
        keywords = [apoe]

        algorithm_start = time.time()
        ac = AhoCorasick(keywords)
        result = ac.search(human_genome)
        algorithm_end = time.time()
            
        print(dna, "========================")
        print("Preprocessing data runtime: ", pre_process_end - pre_process_start)
        print("Algorithm runtime: ", algorithm_end - algorithm_start)
 
    #y = ['Contains', 'Does not']
    #list_of_d = ["1", "2", "3", "4", "5"]
    #plt.xlabel('Contains/Does not contain APOE4', fontsize=14)
    #plt.ylabel("Number of human DNA tested", fontsize=14)
    #plt.bar(list_of_d, y)
    #plt.show()

def test_main():
    with open("sample.txt", 'r') as file:
        human_genome = file.read().replace('\n', '')
    keywords = ["AAA", "GAT"]
    ac = AhoCorasick(keywords)
    result = ac.search(human_genome)
    print(result)

if __name__ == "__main__":
    test_main()

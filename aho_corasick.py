from collections import deque
import sys

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
        return results, i
    
def main():
    args = sys.argv
    file1 = args[1]
    file2 = args[2]

    f = open(file1)
    sample = open(file2)

    apoe = ""
    human_genome = ""

    for char in f.read():
        if char != "\n":
            apoe += char

    for char in sample.read():
        if char != "\n":
            human_genome += char
    
    keywords = [apoe]
    ac = AhoCorasick(keywords)
    results = ac.search(human_genome)
    print(results)

if __name__ == "__main__":
    main()

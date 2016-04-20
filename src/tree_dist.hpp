/* Provides various functions for tree edit distance */


/*
class T need to provide root() method which return one node
Each node need to provide:
	std::vector<Node*> get_childrens() -- return vector of childs
	size_t size() -- size of subtree
	std::string name() -- name of the node
*/
template<typename T>
int trees_edit_distance(const T& f_tree, const T& s_tree);

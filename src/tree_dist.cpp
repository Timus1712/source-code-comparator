#include "tree_dist.hpp"

#include <vector>

/// Find most left descendent for node
// TODO: optimize this (remember)
template<typename T>
T find_leftmost(const T& node) {
	while (node->size() != 1) {
		node = node->get_childs()[0];
	}

	return node;
}


/// Find keyroot for element
// TODO: optimize this (remember)
template<typename T>
T find_keyroot(const T& node) {
	while (node->parent && node->parent->get_childs[0] == node) {
		node = node->parent;
	}

	return node;
}

template<typename T>
void tree_dist(const T& f_node, const T& s_node) {

}


template<typename T>
int trees_edit_distance(const T& f_tree, const T& s_tree) {
	auto f_root = f_tree.root(); // pointer for root node of first tree
	auto s_root = s_tree.root(); // pointer for root node of second tree

	auto f_nodes = all_nodes(f_root);
	auto s_nodes = all_nodes(s_root);

	for (auto f_node : f_nodes) {
		for (auto s_node : s_nodes) {
			auto f_node_key = find_keyroot(f_node);
			auto s_node_key = find_keyroot(s_node);
			tree_dist(f_node_key, s_node_key);
		}
	}
}

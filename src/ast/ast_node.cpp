#include "ast_node.hpp"


ASTNode::ASTNode(const ASTNodePtr& parent, const std::string& kind,
				 const std::string& label) :
				 	parent(parent), kind(kind), label(label), size_(1) {}


void ASTNode::add_child(const ASTNodePtr& child) {
	this->childrens.push_back(child);
	this->size_++;
}


ASTNodePtr ASTNode::add_child(const std::string& kind, const std::string& label) {
	auto new_node = new ASTNode(this, kind, label);
	this->add_child(new_node);
	return new_node;
}


std::vector<ASTNodePtr> ASTNode::get_childs() {
	return this->childrens;
}


ASTNodePtr ASTNode::get_parent() {
	return this->parent;
}


size_t ASTNode::size() {
	return this->size_;
}

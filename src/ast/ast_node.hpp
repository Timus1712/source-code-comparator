#include <vector>
#include <string>

class ASTNode;

typedef ASTNode* ASTNodePtr;

/// Class to represent one node of AST Tree
class ASTNode {
private:
	/// List of childs of this node
	std::vector<ASTNodePtr> childrens;

	/// Pointer to parent of this node (NULL for root)
	ASTNodePtr parent;

	/// Kind of this node
	std::string kind;

	/// Label of this node
	std::string label;

	/// Size of the subtree
	size_t size_;

public:
	/// Construct node as child of the another node
	ASTNode(const ASTNodePtr& parent, const std::string& kind,
			const std::string& label);

	/// Add one child
	void add_child(const ASTNodePtr& child);

	/// Add one child and return ASTNodePtr for it
	ASTNodePtr add_child(const std::string& kind, const std::string& label);

	/// Returns list of childs
	std::vector<ASTNodePtr> get_childs();

	/// Returns parent of the node
	ASTNodePtr get_parent();

	/// Return size of subtree
	size_t size();
};

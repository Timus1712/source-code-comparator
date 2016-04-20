#include <string>

#include "ast_node.hpp"

class AST {
private:
	/// Root of the tree
	ASTNodePtr root;

	/// Original source code file
	std::string ast_filename;

public:
	/// Build AST from prebuilded file
	AST(const std::string& ast_filename);

	/// Get count of nodes in the tree
	size_t size();
};

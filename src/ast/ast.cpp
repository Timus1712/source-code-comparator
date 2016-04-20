#include "ast.hpp"


AST::AST(const std::string& ast_filename) : ast_filename(ast_filename) {

}

size_t AST::size() {
	if (root) return root->size();
	else return 0;
}

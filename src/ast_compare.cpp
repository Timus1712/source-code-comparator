#include <string>
#include <iostream>

#include "ast/ast.hpp"
#include "tree_dist.hpp"


double run(AST f_ast, AST s_ast) {
	return trees_edit_distance(f_ast, s_ast) * 1.0 / (f_ast.size() + s_ast.size());
}


int main(int argc, char * argv[]) {
	std::string ast_filename;
	// Open first AST
	AST first_ast(ast_filename);

	// Open second AST
	AST second_ast(ast_filename);

	auto result = run(first_ast, second_ast);

	std::cout << result << std::endl;

	return 0;
}

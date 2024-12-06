def process_parentheses(expr):
    """Process expressions with parentheses and handle negative signs.
    Parentheses are only used for negating single variables."""
    # Remove spaces if any
    expr = expr.replace(" ", "")
    
    # Handle expressions like b(-A)C or (-a)
    while "(-" in expr:
        # Find the complete term containing the parentheses
        start_term = expr.rfind("+", 0, expr.find("(-"))
        if start_term == -1:
            start_term = expr.rfind("-", 0, expr.find("(-"))
        if start_term == -1:
            start_term = 0
        else:
            start_term += 1
            
        paren_start = expr.find("(-", start_term)
        paren_end = expr.find(")", paren_start)
        end_term = expr.find("+", paren_end)
        if end_term == -1:
            end_term = expr.find("-", paren_end)
        if end_term == -1:
            end_term = len(expr)
            
        # Get the parts of the term
        before_paren = expr[start_term:paren_start]
        var_in_paren = expr[paren_start+2:paren_end]
        after_paren = expr[paren_end+1:end_term]
        
        # Create the new term with negative sign
        new_term = f"-{before_paren}{var_in_paren}{after_paren}"
        
        # Replace the old term with the new one
        expr = expr[:start_term] + new_term + expr[end_term:]
    
    return expr

def remove_zero_terms(expr):
    """Remove any terms that contain '0'."""
    if not expr:
        return expr
        
    # Split into terms
    terms = []
    current_term = ""
    current_sign = ""
    
    # Handle first character
    if expr[0] == '-':
        current_sign = '-'
        expr = expr[1:]
    
    for i, char in enumerate(expr):
        if char in ['+', '-'] and i > 0:
            # Check if current term contains '0'
            if current_term and '0' not in current_term:
                terms.append(current_sign + current_term)
            current_term = ""
            current_sign = char
        else:
            current_term += char
    
    # Handle last term
    if current_term and '0' not in current_term:
        terms.append(current_sign + current_term)
    
    # Join non-zero terms
    result = ''.join(terms)
    if result and result[0] == '+':
        result = result[1:]
    return result if result else "0"

def simplify_ones(expr):
    """Simplify expressions by removing all 1s except when they appear alone."""
    if not expr or expr == "0":
        return expr
        
    # Split into terms
    terms = []
    current_term = ""
    current_sign = ""
    
    # Handle first character
    if expr[0] == '-':
        current_sign = '-'
        expr = expr[1:]
    
    for i, char in enumerate(expr):
        if char in ['+', '-'] and i > 0:
            # Simplify current term
            if current_term:
                # Remove all 1s unless it's the only character
                simplified = current_term.replace('1', '')
                if not simplified:
                    simplified = '1'  # If term was just '1' or '11...', keep a single '1'
                terms.append(current_sign + simplified)
            current_term = ""
            current_sign = char
        else:
            current_term += char
    
    # Handle last term
    if current_term:
        # Remove all 1s unless it's the only character
        simplified = current_term.replace('1', '')
        if not simplified:
            simplified = '1'  # If term was just '1' or '11...', keep a single '1'
        terms.append(current_sign + simplified)
    
    # Join terms
    result = ''.join(terms)
    if result and result[0] == '+':
        result = result[1:]
    return result if result else "0"

def parse_expression(expr):
    """Parse a string expression into terms."""
    if not expr:
        return []
    
    # First process any parentheses
    expr = process_parentheses(expr)
    
    # Remove zero terms
    expr = remove_zero_terms(expr)
    
    # Split the expression into terms
    terms = []
    current_term = ""
    sign = 1
    
    # Handle first character
    if expr[0] == '-':
        sign = -1
        expr = expr[1:]
    
    for i, char in enumerate(expr):
        if char in ['+', '-'] and i > 0:
            if current_term:
                terms.append((sign, current_term))
                current_term = ""
                sign = 1 if char == '+' else -1
        else:
            current_term += char
    
    if current_term:
        terms.append((sign, current_term))
    
    return terms

def add_expressions(expr1, expr2):
    """Add two string expressions."""
    if not expr1:
        return expr2
    if not expr2:
        return expr1
    
    expr1 = remove_zero_terms(expr1)
    expr2 = remove_zero_terms(expr2)
    
    if expr1 == "0":
        return expr2
    if expr2 == "0":
        return expr1
    
    # If either expression starts with a + or -, handle it
    if expr1[0] not in ['+', '-']:
        expr1 = '+' + expr1
    if expr2[0] not in ['+', '-']:
        expr2 = '+' + expr2
        
    result = expr1 + expr2
    result = simplify_ones(remove_zero_terms(result))
    return sort_expression(result)  # Sort the final result

def sort_characters(term):
    """Sort characters within a term."""
    if not term or term == '0':
        return term
    
    # Handle negative sign
    sign = '-' if term.startswith('-') else ''
    chars = term[1:] if sign else term
    
    # Sort only alphabetic characters
    sorted_chars = ''.join(sorted(chars))
    return sign + sorted_chars

def multiply_expressions(expr1, expr2):
    """Multiply two string expressions that may contain multiple terms."""
    if not expr1 or not expr2 or expr1 == '0' or expr2 == '0':
        return '0'
        
    # Process any parentheses first
    expr1 = process_parentheses(expr1)
    expr2 = process_parentheses(expr2)
    
    # Split expressions into terms
    terms1 = parse_expression(expr1)
    terms2 = parse_expression(expr2)
    
    # Multiply each term from expr1 with each term from expr2
    result_terms = []
    for sign1, term1 in terms1:
        for sign2, term2 in terms2:
            # Determine final sign
            final_sign = '-' if sign1 * sign2 < 0 else ''
            # Sort characters in the combined term
            product = final_sign + sort_characters(term1 + term2)
            result_terms.append(product)
    
    # Combine all terms
    result = result_terms[0] if result_terms else '0'
    for term in result_terms[1:]:
        if term.startswith('-'):
            result += term
        else:
            result += '+' + term
    
    result = simplify_ones(remove_zero_terms(result))
    return sort_expression(result) if result else "0"  # Sort the final result

def sort_expression(expr):
    """Sort terms in an expression alphabetically."""
    if not expr or expr == '0':
        return expr
        
    # Process any parentheses first
    expr = process_parentheses(expr)
    
    # Parse the expression into terms
    terms = parse_expression(expr)
    
    # Sort terms based on the actual term (ignoring sign)
    sorted_terms = sorted(terms, key=lambda x: x[1])
    
    # Reconstruct the expression
    result = ''
    for sign, term in sorted_terms:
        if result and sign > 0:
            result += '+'
        if sign < 0:
            result += '-'
        result += term
    
    return result if result else "0"

def matrix_multiply(matrix1, matrix2):
    """
    Multiply two 4x4 matrices where elements are string expressions.
    Each element in the result is a sum of products of corresponding elements.
    """
    # Initialize result matrix with empty strings
    result = [['' for _ in range(4)] for _ in range(4)]
    
    # Perform matrix multiplication
    for i in range(4):
        for j in range(4):
            # Calculate each element in the result matrix
            for k in range(4):
                # Multiply corresponding elements and add to result
                product = multiply_expressions(matrix1[i][k], matrix2[k][j])
                result[i][j] = add_expressions(result[i][j], product)
    
    return result

def print_matrix(matrix):
    """Print matrix in a readable format."""
    for row in matrix:
        print([elem if elem else '0' for elem in row])

# Example usage
if __name__ == "__main__":
    # Example matrices with string expressions containing multiple terms
    matrix1 = [
["b(-A)C-cAB", "bcA-ABC", "a", "wb(-A)"],
["ab(-C)-acB", "abc-aBC", "-A", "w(-a)b"],
["BC-bc", "b(-C)-cB", "0", "wB"],
["0", "0", "0", "1"]
    ]
    
    matrix2 = [
["DEF-df", "d(-F)-fDE", "eD", "x-zd"],
["dEF+fD", "DF-dfE", "de", "zD"],
["e(-F)", "ef", "E", "y"],
["0", "0", "0", "1"]
    ]
    
    print("Matrix 1:")
    print_matrix(matrix1)
    print("\nMatrix 2:")
    print_matrix(matrix2)
    
    result = matrix_multiply(matrix1, matrix2)
    print("\nResult of matrix multiplication:")
    print_matrix(result)
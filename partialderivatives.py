def partial_derivative(expression, theta_num):
    """
    Takes partial derivative of expression with respect to theta_num (1-6)
    by converting appropriate sin/cos terms according to rules:
    For theta_i: 
        - sin(theta_i) (lowercase) becomes cos(theta_i) (uppercase)
        - cos(theta_i) (uppercase) becomes -sin(theta_i) (negative lowercase)
    """
    # Map of letters to their position (1-6)
    sin_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    cos_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}
    
    # Split expression into terms
    terms = []
    current_term = ''
    for char in expression:
        if char in ['+', '-'] and current_term:
            terms.append(current_term)
            current_term = char
        else:
            current_term += char
    if current_term:
        terms.append(current_term)
    
    # Process each term
    new_terms = []
    for term in terms:
        new_term = ''
        sign = 1
        # Handle leading sign
        if term.startswith('-'):
            sign = -1
            term = term[1:]
        elif term.startswith('+'):
            term = term[1:]
            
        # Process each character in the term
        for char in term:
            if char.isupper() and cos_map.get(char) == theta_num:
                # Convert cos to -sin (uppercase to negative lowercase)
                sign *= -1
                new_term += char.lower()
            elif char.islower() and sin_map.get(char) == theta_num:
                # Convert sin to cos (lowercase to uppercase)
                new_term += char.upper()
            else:
                new_term += char
                
        # Apply final sign
        if sign == -1:
            new_terms.append('-' + new_term)
        else:
            if new_terms:  # If not the first term, add explicit plus
                new_terms.append('+' + new_term)
            else:  # First term doesn't need plus
                new_terms.append(new_term)
    
    return ''.join(new_terms)

# Original expressions
p_x = '-ABCDz+ABcdz-ABcx+ACbdz-ACbx+ADbcz-Abw+ay'
p_y = '-Ay-BCDaz+Bacdz-Bacx+Cabdz-Cabx+Dabcz-abw'
p_z = '-BCdz+BCx-BDcz+Bw-CDbz+bcdz-bcx'

# Lists to store partial derivatives
px_partials = []
py_partials = []
pz_partials = []

# Calculate partial derivatives for each theta (1-6)
for theta in range(1, 7):
    px_partials.append(partial_derivative(p_x, theta))
    py_partials.append(partial_derivative(p_y, theta))
    pz_partials.append(partial_derivative(p_z, theta))

# Print results
print("Partial derivatives with respect to theta_1 through theta_6:")
print("\nFor p_x:")
for i, deriv in enumerate(px_partials, 1):
    print(f"d/dθ_{i}: {deriv}")

print("\nFor p_y:")
for i, deriv in enumerate(py_partials, 1):
    print(f"d/dθ_{i}: {deriv}")

print("\nFor p_z:")
for i, deriv in enumerate(pz_partials, 1):
    print(f"d/dθ_{i}: {deriv}")

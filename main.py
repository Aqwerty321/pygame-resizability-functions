import pygame
import sys
import re
import math

def restricted_eval(expression, variables):
    """
    Safely evaluates a mathematical expression containing specified variables.

    This function replaces the variable names in the given expression with their
    corresponding values from the `variables` dictionary. It then evaluates the 
    expression using only a predefined set of safe math functions and constants.

    Args:
        expression (str): The mathematical expression to evaluate, which may 
                          contain variable names as placeholders.
        variables (dict): A dictionary mapping variable names (as keys) to their 
                          values (as values). These variables are substituted into 
                          the expression before evaluation.

    Returns:
        float: The result of evaluating the expression after variable substitution.

    Raises:
        SystemExit: If the expression contains invalid or dangerous operations, the 
                    program will print an error and exit.
    """

    # Create a regex pattern to find and replace variable names in the expression.
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(key) for key in variables.keys()) + r")\b"
    )

    # Replace variables in the expression with their corresponding values.
    def replace_var(match):
        return str(variables[match.group(0)])

    expression = pattern.sub(replace_var, expression)

    # Define a dictionary of allowed functions and constants from the math module.
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        **{k: v for k, v in math.__dict__.items() if not k.startswith("__")},
    }

    # Create a safe evaluation environment with no built-in functions except the allowed ones.
    safe_env = {"__builtins__": None}
    safe_env.update(allowed_names)

    try:
        # Evaluate the expression in the restricted environment.
        result = eval(expression, safe_env, {})
    except Exception as e:
        print(f"Encountered '{e}' error in evaluating expression : {expression}")
        pygame.quit()
        sys.exit()

    return result

def get_scale_and_position_as_function_of_pygame_surface_dimensions(
    surface,
    x_pos_function,
    y_pos_function,
    x_scale_function,
    y_scale_function,
    surface_name="surface",
):
    """
    Calculates the scale and position of a surface based on its dimensions and provided 
    scaling and position functions. You can also provide a custom name for the surface 
    to reference in the position and scale calculations.

    Args:
        surface (pygame.Surface): The reference surface whose dimensions are used for scaling.
        x_pos_function (str): A mathematical expression as a string to determine the X position.
                              It can reference variables like 'surface_width', 'x_scale', and custom surface name.
        y_pos_function (str): A mathematical expression as a string to determine the Y position.
                              It can reference variables like 'surface_height', 'y_scale', and custom surface name.
        x_scale_function (str): A mathematical expression as a string to determine the X scale factor.
                                It can reference 'surface_width', 'surface_height', and custom surface name.
        y_scale_function (str): A mathematical expression as a string to determine the Y scale factor.
                                It can reference 'surface_width', 'surface_height', and custom surface name.
        surface_name (str, optional): A custom name for the surface to use in the functions. Defaults to "surface".

    Returns:
        Four separate float values:
            - X position (float)
            - Y position (float)
            - X scale factor (float)
            - Y scale factor (float)
    """
    # Retrieve the width and height of the given surface.
    surface_width = surface.get_width()
    surface_height = surface.get_height()

    # Create a variables dictionary including the custom surface name.
    variables = {
        f"{surface_name}_width": surface_width,
        f"{surface_name}_height": surface_height,
    }

    # Evaluate the scaling functions using the custom surface name and dimensions.
    x_scale = restricted_eval(x_scale_function, variables)
    y_scale = restricted_eval(y_scale_function, variables)

    # Add scale values to the variables dictionary for position calculation.
    variables[f"x_scale"] = x_scale
    variables[f"y_scale"] = y_scale

    # Evaluate the position functions using the custom surface name and scale values.
    x = restricted_eval(x_pos_function, variables)
    y = restricted_eval(y_pos_function, variables)

    return x, y, x_scale, y_scale

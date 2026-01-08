import ast
import os

def format_value(value: str) -> str | bool | int | float:
    """ Convert the string value to its appropriate Python data type. """
    # Handle boolean values
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    
    # Try to evaluate the value as a Python literal (int, float, etc.)
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If evaluation fails, treat the value as a string and encapsulate it with quotes
        return f'"{value}"'

def set_config_value(config_type: str, config_key: str , config_value: str, fail_silently: bool = False) -> None:
    """ Update the config file with the given key and value.
    
        :param config_type: The type of the config file. This is the config file name, excluding the '.py' extension. (e.g. 'secrets', 'authentication')
        :type config_type: str
        :param config_key: The key to update in the config file.
        :type config_key: str
        :param config_value: The value to set for the given key.
        :type config_value: str
        :param fail_silently: Whether to raise an exception if the config file does not exist. Defaults to False.
        :type fail_silently: bool
    """

    # Determine the path to the config file
    config_file_path = os.path.join('CONFIG', f'{config_type}.py')
    
    if not os.path.exists(config_file_path):
        if fail_silently:
            return
        
        raise FileNotFoundError(f"Config file '{config_file_path}' does not exist.")
    
    # Read the config file content
    with open(config_file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize a variable to check if the key is found
    key_found = False

    # Format the config value using the format_value function
    formatted_value = format_value(config_value)

    # Process each line to find the config key
    for i, line in enumerate(lines):
        if line.strip().startswith(f'{config_key} =') or line.strip().startswith(f'{config_key}='):
            # Update the line with the new formatted value
            lines[i] = f"{config_key} = {formatted_value}\n"
            key_found = True
            break
    
    if not key_found:
        # If the key wasn't found, append it to the file
        lines.append(f"{config_key} = {formatted_value}\n")
    
    # Write the updated content back to the config file
    with open(config_file_path, 'w') as file:
        file.writelines(lines)
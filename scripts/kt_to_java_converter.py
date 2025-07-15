
import os
import re
from collections import defaultdict

class RedundantValueException(Exception):
    """Custom exception for redundant constant values."""
    def __init__(self, redundant_values):
        self.redundant_values = redundant_values
        super().__init__(self._generate_message())

    def _generate_message(self):
        message = "Redundant values found:\n"
        for value, objects in self.redundant_values.items():
            message += f" ->  Value '{value}' is used in objects: {', '.join(objects)}\n"
        return message

def convert_kt_to_java(input_kt_file, output_java_file):
    # Regex patterns
    val_pattern = re.compile(r"const val (\w+) = \"([^\"]+)\"")
    object_pattern = re.compile(r"object (\w+)")

    # Java file content
    java_content = []
    java_content.append("/*")
    java_content.append(" * Auto-generated Java file from Kotlin AutomationsIds for Android platform")
    java_content.append(" */")
    java_content.append("public class AutomationIdLocatorsAndroid {")
    java_content.append("")

    # Track processed objects and constants to avoid redundancy
    processed_objects = {}
    value_to_objects = defaultdict(set)

    # Read the Kotlin file
    current_object = None
    with open(input_kt_file, "r", encoding="utf-8") as kt_file:
        lines = kt_file.readlines()

    for line in lines:
        line = line.strip()

        # Match object declarations
        object_match = object_pattern.match(line)
        if object_match:
            current_object = object_match.group(1)
            # Skip the master object name (AutomationsIds)
            if current_object == "AutomationsIds":
                current_object = None
                continue
            # Initialize the object in the processed_objects dictionary if not already present
            if current_object not in processed_objects:
                processed_objects[current_object] = set()
            continue

        # Match val declarations
        val_match = val_pattern.match(line)
        if val_match and current_object:
            constant_name = val_match.group(1).upper()  # Convert to uppercase
            constant_value = val_match.group(2)

            # Track constant values and their associated objects
            value_to_objects[constant_value].add(current_object)

            # Add the constant to the current object
            processed_objects[current_object].add((constant_name, constant_value))

    # Check for redundant values
    redundant_values = {value: objects for value, objects in value_to_objects.items() if len(objects) > 1}
    if redundant_values:
        raise RedundantValueException(redundant_values)

    # Generate Java content from processed objects
    for object_name, constants in processed_objects.items():
        java_content.append(f"    public static class {object_name} {{")
        for constant_name, constant_value in sorted(constants):
            java_content.append(f"        public static final String {constant_name} = \"{constant_value}\";")
        java_content.append("    }")
        java_content.append("")

    # Close the main Java class
    java_content.append("}")

    # Write to the output Java file
    with open(output_java_file, "w", encoding="utf-8") as java_file:
        java_file.write("\n".join(java_content))

    print(f"\033[32mJava file '{output_java_file}' has been generated successfully.\033[0m")

# If running as a script
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/kt_to_java_converter.py <input_kt_file> <output_java_file>")
        sys.exit(1)

    input_kt_file = sys.argv[1]
    output_java_file = sys.argv[2]

    try:
        convert_kt_to_java(input_kt_file, output_java_file)
    except RedundantValueException as e:
        print(f"\033[91mError: {e}\033[0m")

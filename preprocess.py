import re


def preprocess(input_code, challenge_name):
    if challenge_name == "eval_order":
        return input_code


original_code = '''
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self."car color" = "Yellow"
        self.'single quote' = "Red"
        self."""triple quote

        """ = "Green"
        self.123 = "Blue"

    def display_info(self):
        print(self.brand, self.model, self."car color", self.'single quote', self."""triple quote

        """, self.123)
        

def main():
    car1 = Car("Toyota", "Corolla")
    car1.display_info()
    car1.brand = "Honda"
    car1.display_info()
    car1."car color" = "Blue"
    car1.'single quote' = "Purple"
    car1."""triple quote

        """ = "Orange"
    car1.123 = "Cyan"
    print(car1."car color", car1.'single quote', car1."""triple quote

        """, car1.123, 5.5)
    print('hello.world')
    print('hello."world"')
    print("hello.'world'")
'''

preprocessed_code = preprocess_code(original_code)
print(preprocessed_code)


def preprocess_code(code):
    # Regular expression pattern to find valid identifiers followed by string or numeric attributes
    # Exclude matches that are part of a larger string literal (look-behind for quote characters)
    pattern = re.compile(
        r'(?<!["\'])\b([a-zA-Z_]\w*\.)((?:"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|".*?"|\'.*?\')|\b\d+\b)')

    def replace_with_valid_attr(match):
        identifier, attr = match.groups()
        if attr[0] in "\"'":  # String literal
            # Remove outer quotes, replace internal whitespace with underscores, prepend 'str_attr_'
            attr_name = re.sub(
                r'[\s\n]+', '_', attr.strip("\"'").replace('"""', '').replace("'''", ''))
            return identifier + 'str_attr_' + attr_name
        else:  # Numeric
            # Prepend 'num_attr_'
            return identifier + 'num_attr_' + attr

    # Replace all occurrences of the pattern with valid attribute names
    return pattern.sub(replace_with_valid_attr, code)


# Example usage
original_code = '''
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self."car color" = "Yellow"
        self.'single quote' = "Red"
        self.123 = "Blue"

    def display_info(self):
        print(self.brand, self.model, self."car color", self.'single quote', self.123)
        

def main():
    car1 = Car("Toyota", "Corolla")
    car1.display_info()
    car1.brand = "Honda"
    car1.display_info()
    car1."car color" = "Blue"
    car1.'single quote' = "Purple"
    car1.123 = "Cyan"
    print(car1."car color", car1.'single quote', car1.123, 5.5)
    print('hello.world')
    print('hello."world"')
    print("hello.'world'")
'''

preprocessed_code = preprocess_code(original_code)
print(preprocessed_code)


def preprocess_code_num(code):
    # Regular expression pattern to find valid identifiers followed only by string literal attributes
    pattern = re.compile(
        r'(?<!["\'])\b([a-zA-Z_]\w*\.)("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|".*?"|\'.*?\')')

    def replace_with_valid_attr(match):
        identifier, attr = match.groups()
        # Remove outer quotes, replace internal whitespace with underscores, prepend 'str_attr_'
        attr_name = re.sub(
            r'[\s\n]+', '_', attr.strip("\"'").replace('"""', '').replace("'''", ''))
        return identifier + 'str_attr_' + attr_name

    # Replace all occurrences of the pattern with valid attribute names
    return pattern.sub(replace_with_valid_attr, code)

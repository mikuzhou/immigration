import openai

PROBLEM_DEFINITION_PROMPT = """
Create a Python implementation that can read, validate, and manipulate problem definitions based on a detailed JSON specification. The JSON specification outlines a structure for defining a problem, which includes various fields and nested objects. Here's a summary of the JSON structure:

### Top-Level Problem JSON Structure:
- **identifier**: A string representing the unique identifier of the problem definition.
- **prompts**: An array of objects representing the prompts.
- **function_prototype**: An object representing the function prototype.
- **correctness_test_suite**: An optional array of objects representing the test cases for correctness.
- **optimal_solution**: An optional string representing the optimal solution to the problem.
- **tags**: An optional array of strings representing tags associated with the problem definition.

### Nested JSON Structures:
- **Prompt**: Contains fields like `prompt_id`, `prompt`, `genericize`, `sample_inputs_outputs`, and `input_code`.
- **FunctionPrototype**: Contains fields like `function_name`, `parameters`, and `return_value`.
- **TestCase**: Contains fields like `input` and `expected_output`.
- **Parameter**: Contains fields like `name` and `type`.
- **ReturnValue**: Contains a field `type`.

The implementation should include classes for each of the JSON structures (`Problem`, `Prompt`, `FunctionPrototype`, `TestCase`, `Parameter`, `ReturnValue`) and should have methods for validating the JSON against the specification, as well as methods for manipulating the problem definition (e.g., adding/removing prompts or test cases). Additionally, provide a function that can take a problem JSON string as input, and return a `Problem` object. Ensure to handle optional fields appropriately, and include type annotations for all methods and functions.

For validation, ensure that:
1. Required fields are present and of the correct type.
2. Optional fields, if present, are of the correct type.
3. Field values adhere to any restrictions outlined in the specification (e.g., string length, array size).

Include unit tests to verify the correctness of your implementation, covering various scenarios to ensure robustness.
"""

LLM_INPUT_PROMPT = """
Design a Python class named `LLMProblemInput`. This class should encapsulate information related to a problem to be solved by a Large Language Model (LLM). The class should have the following attributes:

1. `problem_id`: a string that serves as a unique identifier for the problem.
2. `prompt_id`: a string that serves as a unique identifier for the prompt associated with the problem.
3. `prompt`: a string containing the text of the prompt that will be passed to the LLM.
4. `sample_inputs_outputs`: a list of `TestCase` objects, where each `TestCase` object represents a pair of sample input and expected output for the problem.
5. `input_code`: a string containing any initial code provided for the problem (default to an empty string if no input code is provided).
6. `function_prototype`: an instance of a `FunctionPrototype` class, which should represent the function signature for the problem. The `FunctionPrototype` class should contain two attributes: `name`, a string representing the name of the function, and `parameters`, a list of strings representing the parameter names of the function.

Your implementation should include the `LLMProblemInput` class and the `FunctionPrototype` class, along with any necessary constructors, methods, and properties to ensure the encapsulation and management of the data as per the outlined attributes.
"""

LLM_OUTPUT_PROMPT = """
**Prompt:**

Design a Python class named `LLMSolution`. This class should encapsulate information related to a solution generated by a Large Language Model (LLM) for a particular problem. The class should have the following attributes:

1. `problem_identifier`: a string that serves as a unique identifier for the problem.
2. `model_identifier`: a string that serves as a unique identifier for the model that generated the solution.
3. `prompt_identifier`: a string that serves as a unique identifier for the prompt associated with the problem.
4. `solution_code`: a string containing the code generated by the model as the solution for the problem.
5. `feedback`: an optional dictionary containing feedback information (default to None if no feedback is provided).

Your implementation should include the `LLMSolution` class, along with any necessary constructors, methods, and properties to ensure the encapsulation and management of the data as per the outlined attributes. The class should have a method named `display_solution` that prints the `solution_code` to the console, and a method named `apply_feedback` that accepts a dictionary argument and updates the `feedback` attribute accordingly.
"""

GRADER_PROMPT = """
Implement a Python program for a grading system based on the following specifications:

1. Create a class named `Issue` with the following attributes:
	- `issue_category` (string): Category of the issue.
	- `issue_description` (string): Description of the issue.

2. Create a class named `SolutionGrade` with the following attributes:
	- `problem_identifier` (string): A unique identifier for the problem.
	- `prompt_identifier` (string): A unique identifier for the prompt.
	- `model_identifier` (string): A unique identifier for the model.
	- `score` (float): The score for the solution.
	- `sub_criteria_scores` (dictionary): Key-value pairs where the key is the sub-criteria identifier and the value is the score for that sub-criteria.
	- `issues` (list of `Issue` objects): List of issue objects, each containing an `issue_category` (string) and `issue_description` (string).

3. Create a class named `GradingOutput` with the following attributes:
	- `solution_grades` (list of `SolutionGrade` objects): List of `SolutionGrade` objects, each containing the fields as specified in the `SolutionGrade` class.
	- `grader_identifier` (string): A unique identifier for the grader.

Ensure that the program can serialize and deserialize objects of these classes to and from JSON following the provided specifications. Include methods for calculating the average score across all `SolutionGrade` objects in a `GradingOutput` object, as well as methods for adding new `Issue` objects to a `SolutionGrade` object and new `SolutionGrade` objects to a `GradingOutput` object.
"""

OVERALL_PROMPT = """
Now, use the code you have generated to implement a Python framework named 'LLM Coding Ability Benchmark Suite' to evaluate the coding and problem-solving capabilities of AI models in the domain of programming challenges. The framework should have three main components:

1. **Problem Definition**:
	- Allow users to define programming challenges in a structured format within a directory, e.g., `problem_sets/bugfixing/problems`.
	- Each challenge should have a problem statement, input/output specifications, and a set of example test cases.

2. **Solution Generation**:
	- Enable AI models to generate solutions for the defined programming challenges.
	- Take a problem definition as input and produce a Python code solution as output.

3. **Grading**:
	- Evaluate the generated solutions against a set of predefined test cases to ensure they solve the problem as required.
	- Assess adherence to good coding practices and specified criteria such as correctness and performance.

The framework should provide a standardized approach to evaluating different AI models on a common ground of programming challenges. It should be capable of interfacing with different AI models like GPT-4. Ensure that the framework is modular, well-documented, and has a user-friendly interface for defining problems, generating solutions, and grading. Include a mechanism for users to add custom test cases and grading criteria.

Provide a script named `benchmark.py` to demonstrate how users can get started with the framework. The script should accept flags for specifying the base path of problem sets, the model to be used, and the grading criteria, e.g., 
```bash
python3 benchmark.py --base_path problem_sets/bugfixing/ --grade --model gpt-4 --grader performance correctness
"""

remainingInputs = [PROBLEM_DEFINITION_PROMPT, LLM_INPUT_PROMPT, LLM_OUTPUT_PROMPT, GRADER_PROMPT, OVERALL_PROMPT]
messages = []

while len(remainingInputs) > 0:
	input = remainingInputs.pop(0)

	messages.append({"role": "user", "content": input})
	
	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo-16k",
		max_tokens=5000,
		messages = messages)
	
	response_message = response.choices[0].message
	
	messages.append(response_message)
	print(response_message.content)

# # Extract the generated code
# response = response.choices[0].message.content.strip()


import concurrent.futures
import streamlit as st
import requests
import subprocess
import openai
# Set up your OpenAI API credentials
openai.api_key = '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'
def get_user_repositories(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'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'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        return None


def calculate_cyclomatic_complexity(repo_url):
    try:
        response = requests.get(repo_url)
        if response.status_code == 200:
            source_code = response.text
            # Write the source code to a temporary file
            temp_file_path = "./temp.py"
            with open(temp_file_path, "w") as temp_file:
                temp_file.write(source_code)
            # Calculate cyclomatic complexity using flake8
            result = subprocess.run(["flake8", "--max-complexity", "10", temp_file_path], stdout=subprocess.PIPE)
            complexity_output = result.stdout.decode("utf-8")
            complexity_lines = complexity_output.strip().split("\n")
            # Extract and return the total complexity
            total_complexity = 0
            for line in complexity_lines:
                if "temp.py" in line:
                    parts = line.split(":")
                    if len(parts) >= 3:
                        complexity = int(parts[2])
                        total_complexity += complexity
            return total_complexity
        else:
            return None
    except Exception as e:
        print("Error calculating cyclomatic complexity:", e)
        return None

def calculate_coupling_score(repository):
    # Calculate a coupling score based on the number of external package imports
    try:
        repo_url = repository['html_url']
        response = requests.get(repo_url)
        if response.status_code == 200:
            source_code = response.text
            # Example: Count the number of occurrences of the string "import" in the source code
            coupling_score = source_code.count("import")
            return coupling_score
        else:
            return None
    except Exception as e:
        print("Error calculating coupling score:", e)
        return None

def calculate_cohesion_score(repository):
    try:
        repo_url = repository['html_url']
        response = requests.get(repo_url)
        if response.status_code == 200:
            source_code = response.text
            # Example: Count the number of occurrences of "def " to count functions
            num_functions = source_code.count("def ")
            # Example: Count the number of occurrences of "class " to count classes
            num_classes = source_code.count("class ")
            # Calculate the cohesion score as a combination of functions and classes
            cohesion_score = num_functions + num_classes
            return cohesion_score
        else:
            return None
    except Exception as e:
        print("Error calculating cohesion score:", e)
        return None


def calculate_issue_complexity(repository):
    try:
        repo_url = repository['html_url']
        issues_url = f'{repo_url}/issues'
        response = requests.get(issues_url)
        if response.status_code == 200:
            issues_data = response.json()
            # Example: Calculate the issue complexity based on the number of open issues
            issue_complexity = len([issue for issue in issues_data if issue['state'] == 'open'])
            return issue_complexity
        else:
            print("Error fetching issue data. Status code:", response.status_code)
            print("Response content:", response.content)
            return None
    except Exception as e:
        return None


def calculate_documentation_score(repository):
    try:
        repo_url = repository['html_url']
        readme_url = f'{repo_url}/blob/master/README.md'
        response = requests.get(readme_url)
        if response.status_code == 200:
            readme_content = response.text
            # Example: Calculate documentation score based on the presence of keywords
            documentation_score = 0
            if "documentation" in readme_content.lower():
                documentation_score += 1
            if "usage" in readme_content.lower():
                documentation_score += 1
            return documentation_score
        else:
            return 0  # Return a default score of 0 if documentation cannot be fetched
    except Exception as e:
        return 0  # Return a default score of 0 if an error occurs


def calculate_code_smells_score(repository):
    try:
        repo_url = repository['html_url']
        response = requests.get(f'{repo_url}/archive/master.tar.gz')
        if response.status_code == 200:
            # Extract the downloaded tar.gz file and analyze the code for code smells
            # Example: Calculate code smells score based on the presence of specific patterns or indications
            code_smells_score = 0
            # Placeholder logic: Analyze the code for code smells and update the score
            # code_smells_score = analyze_code_for_smells(response.content)
            return code_smells_score
        else:
            return 0  # Return a default score of 0 if code smells assessment cannot be done
    except Exception as e:
        print("Error calculating code smells score:", e)
        return 0  # Return a default score of 0 if an error occurs

def calculate_technical_debt_score(repository):
    try:
        # Example: Calculate technical debt score based on the presence of TODO comments
        todo_comments_url = f'{repository["html_url"]}/archive/master.tar.gz'
        response = requests.get(todo_comments_url)
        if response.status_code == 200:
            # Example: Calculate technical debt score based on the presence of TODO comments
            technical_debt_score = 0
            # Placeholder logic: Analyze the code for TODO comments and update the score
            # technical_debt_score = analyze_code_for_technical_debt(response.content)
            return technical_debt_score
        else:
            return 0  # Return a default score of 0 if technical debt assessment cannot be done
    except Exception as e:
        print("Error calculating technical debt score:", e)
        return 0  # Return a default score of 0 if an error occurs


def calculate_contributor_activity_score(repository):
    try:
        contributor_activity_score = 0

        # Retrieve contributor data using GitHub API
        contributor_data_url = f'{repository["url"]}/contributors'
        response = requests.get(contributor_data_url)

        if response.status_code == 200:
            contributors = response.json()

            # Calculate contributor activity score based on factors like commits, pull requests, etc.
            for contributor in contributors:
                commits = contributor.get('contributions', 0)
                pull_requests = contributor.get('contributions', 0)  # Placeholder: Replace with actual pull request count
                comments = contributor.get('contributions', 0)  # Placeholder: Replace with actual comment count
                # ... Calculate other activity metrics as needed
                activity_score = commits + pull_requests + comments
                contributor_activity_score += activity_score

            return contributor_activity_score

        else:
            return 0  # Return a default score of 0 if contributor activity data cannot be retrieved

    except Exception as e:
        print("Error calculating contributor activity score:", e)
        return 0  # Return a default score of 0 if an error occurs


def calculate_complexity_score(repository):
    # Calculate complexity score based on available metrics
    complexity_score = (
        repository['stargazers_count'] +
        repository['forks_count'] +
        repository['size']
    )

    # Retrieve and calculate cyclomatic complexity
    cc = calculate_cyclomatic_complexity(repository['html_url'])
    if cc is not None:
        complexity_score += cc

    # Calculate coupling score
    coupling = calculate_coupling_score(repository)
    complexity_score += coupling

    # Calculate cohesion score
    cohesion = calculate_cohesion_score(repository)
    complexity_score += cohesion

    # Calculate issue complexity
    issue_complexity = calculate_issue_complexity(repository)
    if issue_complexity is not None:
        complexity_score += issue_complexity

    # Calculate documentation score
    documentation_score = calculate_documentation_score(repository)
    complexity_score += documentation_score

    # Calculate code smells score
    code_smells_score = calculate_code_smells_score(repository)
    complexity_score += code_smells_score

    # Calculate technical debt score
    technical_debt_score = calculate_technical_debt_score(repository)
    complexity_score += technical_debt_score

    contributor_activity = calculate_contributor_activity_score(repository)
    complexity_score += contributor_activity

    return complexity_score


def find_most_complex_repository(repositories):
    most_complex_repo = None
    highest_complexity_score = 0

    for repo in repositories:
        complexity_score = calculate_complexity_score(repo)

        if complexity_score > highest_complexity_score:
            highest_complexity_score = complexity_score
            most_complex_repo = repo

    return most_complex_repo
def process_repository(repository):
    complexity_score = calculate_complexity_score(repository)
    return repository, complexity_score

# Wrap your main code in a Streamlit app
def streamlit_app():
    st.title("GitHub Repository Complexity Analyzer")

    github_username = st.text_input("Enter the GitHub username:")
    if st.button("Process Repositories"):
        repositories = get_user_repositories(github_username)

        if repositories is None:
            st.error("Failed to retrieve user repositories. Please check the username.")
            return

        st.write("Processing repositories...")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Process repositories in parallel
            future_to_repo = {executor.submit(process_repository, repo): repo for repo in repositories}

            most_complex_repo = None
            highest_complexity_score = 0

            for future in concurrent.futures.as_completed(future_to_repo):
                repo = future_to_repo[future]
                try:
                    repo, complexity_score = future.result()
                    st.write("Processed Repository:", repo["name"])
                    st.write("Complexity Score:", complexity_score)
                    if complexity_score > highest_complexity_score:
                        highest_complexity_score = complexity_score
                        most_complex_repo = repo
                except Exception as e:
                    st.write(f"Error processing repository {repo['name']}: {e}")

            if most_complex_repo is not None:
                st.success("Analysis complete!")
                st.write("Most technically complex repository:")
                st.write("Repository Name:", most_complex_repo["name"])
                st.write("Repository URL:", most_complex_repo["html_url"])
                st.write("Complexity Score:", highest_complexity_score)

# Run the Streamlit app
if __name__ == '__main__':
    streamlit_app()

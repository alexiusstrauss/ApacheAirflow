# Project Folders
TARGET_FOLDERS="."
MAX_ACCEPTABLE_COMPLEXITY=6

# Run tools
echo "Running isort" && \
isort --recursive --check-only --diff $TARGET_FOLDERS && \
echo "Running black" && \
black --check $TARGET_FOLDERS && \
echo "Running flake8" && \
flake8 $TARGET_FOLDERS && \
echo "Running pylint" && \
pylint --max-complexity=$MAX_ACCEPTABLE_COMPLEXITY $TARGET_FOLDERS && \
echo "Running mypy" && \
mypy $TARGET_FOLDERS && \
echo "Running common security flaws" && \
bandit -r $TARGET_FOLDERS -x ./dags/tests/
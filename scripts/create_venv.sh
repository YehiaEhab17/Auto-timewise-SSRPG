# NOTE: Pine, you know there are Windows users, hon?
#       So maybe have an edge case for that since venvs
#       are not needed in a Windows environment.

cd "$(dirname "$0")/.."

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# start_production steps
# Set working directory to project root and start virtual Evironment 
cd C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform
.venv\Scripts\Activate

# Start Qdrant Docker container
"C:\Program Files\Docker\Docker\Docker Desktop.exe"
docker run -p 6333:6333 qdrant/qdrant

	🧠 Helpful Docker Commands
	Command	Description
	docker ps	Show running containers
	docker ps -a	Show all containers (even stopped)
	docker stop <id>	Stop a running container
	docker start <id>	Start a stopped container
	docker images	Show downloaded images
	docker rm <id>	Remove a container
	docker rmi <image_id>	Remove an image

# Start FastAPI backend with virtual environment and uvicorn
uvicorn backend.mcp.server:app --reload


# Start React frontend
cd C:\Users\natha\Py_Coding_Projects\Keyhole_Automation_Platform\frontend\Keyhole-Solution-App
npm start

## Stage Github commits
git add <file>: Stages a specific file.
git add <directory>: Stages all changes within a directory.
git add .: Stages all changes in the current directory and its subdirectories (use this with caution!).
git add -p: (Interactive staging) Allows you to review changes chunk by chunk and selectively stage them. This is highly recommended for more complex commits, as it gives you fine-grained control.
# Write commit message
git commit -m "Fixed bug in login form validation"
# Pushes changes to the 'main' branch on the 'origin' remote
git push origin main
import os
from git import Repo


class GitManager:
    def __init__(self, repo_url, local_path):
        self.repo_url = repo_url
        self.local_path = local_path

    def clone_repository(self):
        try:
            Repo.clone_from(self.repo_url, self.local_path)
            print("Repository cloned successfully!")
        except Exception as e:
            print(f"Error cloning repository: {e}")

    def fetch_updates(self):
        try:
            repo = Repo(self.local_path)
            origin = repo.remote()
            origin.fetch()
            print("Updates fetched successfully!")
        except Exception as e:
            print(f"Error fetching updates: {e}")

    def generate_statistics(self):
        try:
            repo = Repo(self.local_path)
            commits = list(repo.iter_commits())
            print(f"Total number of commits: {len(commits)}")

        except Exception as e:
            print(f"Error generating statistics: {e}")


if __name__ == "__main__":
    repo_url = "https://github.com/example/repository.git"
    local_path = "repository"

    git_manager = GitManager(repo_url, local_path)
    git_manager.clone_repository()
    git_manager.fetch_updates()
    git_manager.generate_statistics()

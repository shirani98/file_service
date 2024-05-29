import os
import requests
import subprocess


class FileSyncManager:
    FTP_USERNAME = "admin"  # Change_data
    FTP_PASSWORD = "admin"  # Change_data

    def __init__(
        self,
        django_server_url,
        ftp_ip,
        ftp_server_directory,
    ):
        self.django_server_url = django_server_url
        self.ftp_server_directory = ftp_server_directory
        self.ftp_ip = ftp_ip
        self.jwt_token = ""

        self.local_directory = "/home/mahdi/test_server"  # Change_data
        self.rsync_script = "/home/mahdi/ftp_service/sync_files.sh"  # Change_data

    def auth(self):
        data = {"username": self.FTP_USERNAME, "password": self.FTP_PASSWORD}
        response = requests.post(f"{self.django_server_url}/api/token/", data=data)
        try:
            if response.status_code == 200:
                self.jwt_token = response.json()["access"]
                print("Auth Process Successfully!")
            else:
                raise KeyError()
        except Exception:
            raise AttributeError("Auth Process UnSuccessfully!")

    def get_file_list(self):
        response = requests.get(f"{self.django_server_url}/api/files")
        if response.status_code == 200:
            file_names = []
            for file in response.json():
                file_names.append(file["name"])
            return file_names
        else:
            print(f"Error fetching file list from server: {response.status_code}")
            return []

    def download_missing_files(self, files):
        missing_files = [
            file_name
            for file_name in files
            if not os.path.exists(os.path.join(self.local_directory, file_name))
        ]
        if not missing_files:
            return missing_files
        self.auth()
        headers = {"Authorization": f"Bearer {self.jwt_token}"}
        for file_name in missing_files:
            local_file_path = os.path.join(self.local_directory, file_name)
            file_url = f"{self.django_server_url}/api/files/download/{file_name}/"
            response = requests.get(file_url, headers=headers, stream=True)
            if response.status_code == 200:
                with open(local_file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded {file_name}")
            else:
                print(f"Failed to download {file_name}: {response.status_code}")

    def sync_local_files_to_ftp_server(self, files):
        local_files = set(os.listdir(self.local_directory))
        server_files = set(files)
        files_to_sync = local_files - server_files
        if files_to_sync:
            print("Syncing files to FTP server...")
            for file_name in files_to_sync:
                subprocess.run(
                    [
                        self.rsync_script,
                        self.ftp_ip,
                        f"{self.ftp_server_directory}/{file_name}",
                    ],
                    check=True,
                )
                print(f"Synced {file_name} to FTP server")
        else:
            print("No files to sync.")

    def run(self):
        server_files = self.get_file_list()
        self.download_missing_files(server_files)
        self.sync_local_files_to_ftp_server(server_files)


if __name__ == "__main__":
    DJANGO_SERVER_URL = "http://localhost:8000"
    FTP_SERVER_DIRECTORY = "/home/mahdi/test_mehdi"  # Change_data
    FTP_IP = "127.0.0.1"  # Change_data

    file_sync_manager = FileSyncManager(
        DJANGO_SERVER_URL,
        FTP_IP,
        FTP_SERVER_DIRECTORY,
    )
    file_sync_manager.run()

import pandas as pd

LOG_FILE = "logs.txt"


def load_logs(filename):

    try:
        df = pd.read_csv(filename, delimiter=":", names=["Timestamp", "Log Message"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
        return df
    except FileNotFoundError:
        print(f"Log file '{filename}' not found.")
        return None


def search_logs(df, keyword):

    if df is not None:
        keyword_found = df[df["Log Message"].str.contains(keyword, case=False)]
        return keyword_found
    else:
        return None


if __name__ == "__main__":
    keyword = input("Enter keyword to search in logs: ")
    logs_df = load_logs(LOG_FILE)

    if logs_df is not None:
        keyword_logs = search_logs(logs_df, keyword)
        if keyword_logs is not None and not keyword_logs.empty:
            print("Found logs containing the keyword:")
            print(keyword_logs)
        else:
            print("No logs found containing the keyword.")

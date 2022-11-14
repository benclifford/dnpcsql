import matplotlib.pyplot as plt
import numpy as np
import sqlalchemy
import sqlite3

if __name__ == "__main__":
    print("task end latency analysis on cori, november 2022")

    db_name = "../da/runinfo/monitoring.db"
    db = sqlite3.connect(db_name,
                     detect_types=sqlite3.PARSE_DECLTYPES |
                     sqlite3.PARSE_COLNAMES)

    cursor = db.cursor()

    query = 'select (julianday(end_status.timestamp) - julianday(start_status.timestamp)) * 86400 as D from task inner join status as end_status on end_status.task_id = task.task_id inner join status as start_status on start_status.task_id = task.task_id where end_status.task_status_name = "running_ended" and start_status.task_status_name = "running";'
    rows = list(cursor.execute(query))

    print(f"there are {len(rows)} relevant status transitions in the db")
    assert len(rows)==32000

    durations_running_ended_exec_done = np.array([t for (t,) in rows])
    fig, ax = plt.subplots()

    ax.hist(durations_running_ended_exec_done, bins=100, color="#0000FF")
    ax.axvline(durations_running_ended_exec_done.mean(), linestyle='dashed', linewidth=1, label="mean", color = "#009900")
    ax.axvline(np.percentile(durations_running_ended_exec_done, 50), linestyle='dashed', linewidth=1, label="median", color = "#FF00AA")
    ax.axvline(np.percentile(durations_running_ended_exec_done, 95), linestyle='dashed', linewidth=1, label="95%", color = "#AA0000")
    ax.axvline(np.percentile(durations_running_ended_exec_done, 100), linestyle='dashed', linewidth=1, label="maximum", color = "#FF4400")
    ax.legend()

    plt.xlabel("seconds")
    plt.ylabel("number of tasks in bin")

    plt.savefig("taskdurations.png")


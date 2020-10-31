import os

def main(taskQueue):
    task = taskQueue.get()
    print("Soy backup controller ", os.getpid() ,task.ip, task.port, task.path, flush = True)

if __name__ == "__main__":
    main()

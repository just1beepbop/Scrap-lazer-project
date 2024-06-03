from multiprocessing import Process, Queue
from Choosing_plate import Plate
from level_Editor import Level_Editor

def main():
    fir = Plate()
    sec = Level_Editor()
    queue = Queue()
    process1 = Process(target=fir.update, args=(queue,))
    process2 = Process(target=sec.update, args=(queue,))

    process1.start()
    process2.start()

    process1.join()
    process2.join()
if __name__ == "__main__":
    main()
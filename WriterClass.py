COLUMNS = 'xAccel, yAccel, zAccel, xGyro, yGyro, zGyro, temp\n'


class WriterClass:
    def __init__(self, path: str) -> None:
        self.PATH_TO_JSON = path
        #open(path, "w")
        #self.writeData(COLUMNS)

    def writeData(self, data) -> None:
        f = open(self.PATH_TO_JSON, "a")
        f.write(f'{data}\n')
        f.close()

class Stamp:
    serinumber = None
    time = None
    status = None
    id_batch = None

    def __init__(self, serinumber, time, status, id_batch):
        self.serinumber = serinumber
        self.time = time
        self.status = status
        self.id_batch = id_batch

    # phương thức
    def set_serinumber(self, serinumber):
        self.serinumber = serinumber
    def get_serinumber(self):
        return self.serinumber

    def set_time(self, time):
        self.time = time
    def get_time(self):
        return self.time

    def set_status(self, status):
        self.status = status
    def get_status(self):
        return self.status

    def set_id_batch(self, id_batch):
        self.id_batch = id_batch
    def get_id_batch(self):
        return self.id_batch
class Config_seri:
    name_production_batch = "tran trung"
    id_producers = 0
    id_product = 0
    id_production_batch = 0
    num_MAX = 0
    num_MIN = 0

    def __init__(self, name_production_batch, id_producers, id_product, id_production_batch, num_MAX, num_MIN):
        self.name_production_batch = name_production_batch
        self.id_producers = id_producers
        self.id_product = id_product
        self.id_production_batch = id_production_batch
        self.num_MAX = num_MAX
        self.num_MIN = num_MIN

    # phương thức
    def set_name_production_batch(self, name_production_batch):
        self.name_production_batch = name_production_batch
    def get_name_production_batch(self):
        return self.name_production_batch

    def set_id_producers(self, id_producers):
        self.id_producers = id_producers
    def get_id_producers(self):
        return self.id_producers

    def set_id_product(self, id_product):
        self.id_product = id_product
    def get_id_product(self):
        return self.id_product

    def set_id_production_batch(self, id_production_batch):
        self.id_production_batch = id_production_batch
    def get_id_production_batch(self):
        return self.id_production_batch

    def set_num_MAX(self, num_MAX):
        self.num_MAX = num_MAX
    def get_num_MAX(self):
        return self.num_MAX

    def set_num_MIN(self, num_MIN):
        self.num_MIN = num_MIN
    def get_name_production_batch(self):
        return self.num_MIN
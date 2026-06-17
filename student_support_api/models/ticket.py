class TicketCreate():
    def __init__(self, id,title,description, priority, createdby):
        self.id          = id
        self.title       = title
        self.description = description
        self.priority    = priority
        self.status      = "Open"
        self.owner_id    = createdby

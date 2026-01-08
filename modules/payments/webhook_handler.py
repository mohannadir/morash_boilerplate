webhook_handlers = {}

def receive(event_type):
    def decorator(func):
        if event_type not in webhook_handlers:
            webhook_handlers[event_type] = []
        webhook_handlers[event_type].append(func)
        return func
    return decorator

def handle_event(event):
    event_type = event['type']
    handlers = webhook_handlers.get(event_type, [])
    for handler in handlers:
        handler(event)
import json
import mouse
import keyboard

isRecording = True
lastEvent = None
listOfEvents = []

def serialiseEvent(event):
    if isinstance(event, keyboard.KeyboardEvent):
        return {
            "name": event.name,
            "scan_code": event.scan_code,
            "timestamp": event.time,
            "device": "keyboard",
            "type": event.event_type,
        }
    elif isinstance(event, mouse.MoveEvent):
        return {
            "device": "mouse",
            "type": "move",
            "x": event.x,
            "y": event.y,
            "timestamp": event.time,
        }
    elif isinstance(event, mouse.ButtonEvent):
        return {
            "device": "mouse",
            "type": event.event_type,
            "button": event.button,
            "x": mouse.get_position()[0],
            "y":mouse.get_position()[1],
            "timestamp": event.time,
        }
    elif isinstance(event, mouse.WheelEvent):
        return {
            "device": "mouse",
            "type": "wheel",
            "delta": event.delta,
            "timestamp": event.time,
        }

def mouseListener(event):
    global isRecording
    global lastEvent
    global listOfEvents
    if isRecording:
        if isinstance(lastEvent, mouse.MoveEvent) and isinstance(event, mouse.MoveEvent):
            listOfEvents[len(listOfEvents)-1] = serialiseEvent(event)
            lastEvent = event
        else:
            listOfEvents.append(serialiseEvent(event))
            lastEvent = event

def keyboardListener(event: keyboard.KeyboardEvent):
    global isRecording
    global lastEvent
    global listOfEvents
    if isRecording:
        listOfEvents.append(serialiseEvent(event))
        lastEvent = event

def init():
    mouse.unhook_all()
    keyboard.unhook_all()
    mouse.hook(mouseListener)
    keyboard.hook(keyboardListener)

def moveMouse(x, y):
    mouse.move(x, y, True)
    return ""

def pressKey(c):
    keyboard.press(c)
    return ""

def releaseKey(c):
    keyboard.release(c)
    return ""

def tapKey(c):
    keyboard.press(c)
    keyboard.release(c)
    return ""

def startRecording():
    global isRecording
    global listOfEvents
    global lastEvent
    isRecording = True
    listOfEvents = []
    lastEvent = None
    return ""

def stopRecording():
    global isRecording
    isRecording = False
    return json.dumps(listOfEvents)
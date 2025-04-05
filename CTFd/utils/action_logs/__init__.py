from flask_socketio import emit


def send_action_logs_to_client(logs):
    try:
        data = {"type": "action_logs", "logs": logs}
        emit("action_logs", data, broadcast=True, namespace="/")
    except Exception as e:
        print(f"Error sending action logs to client: {e}")

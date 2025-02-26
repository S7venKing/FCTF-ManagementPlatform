from typing import List
from flask import request
from flask_restx import Namespace, Resource
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError

from CTFd.api.v1.helpers.schemas import sqlalchemy_to_pydantic
from CTFd.api.v1.schemas import APIDetailedSuccessResponse, APIListSuccessResponse
from CTFd.models import ActionLogs, db
from CTFd.utils.decorators import admins_only
from CTFd.utils.user import get_current_user

action_logs_namespace = Namespace("action_logs", description="Endpoint for action logging")

# Convert SQLAlchemy model to Pydantic schema for validation
ActionLogModel = sqlalchemy_to_pydantic(ActionLogs)

class ActionLogDetailedSuccessResponse(APIDetailedSuccessResponse):
    data: ActionLogModel

class ActionLogListSuccessResponse(APIListSuccessResponse):
    data: List[ActionLogModel]

# Register schema models in Swagger docs
action_logs_namespace.schema_model(
    "ActionLogDetailedSuccessResponse", ActionLogDetailedSuccessResponse.apidoc()
)
action_logs_namespace.schema_model(
    "ActionLogListSuccessResponse", ActionLogListSuccessResponse.apidoc()
)

# Define input validation schema using Pydantic
class ActionLogCreateSchema(BaseModel):
    actionType: int = Field(..., description="Type of action", ge=0)
    actionDetail: str = Field(..., description="Details of the action", min_length=1, max_length=500)

@action_logs_namespace.route("")
class ActionLogList(Resource):
    """List and create action logs"""

    @action_logs_namespace.doc(
        description="Retrieve all action logs (Admins) or user's logs (Contestants)",
        responses={200: ("Success", "ActionLogListSuccessResponse")},
    )
    def get(self):
        """
        Retrieve action logs:
        - Contestants see only their logs.
        - Admins can see all logs by passing `?all=true`.
        """
        user = get_current_user()

        if not user:
            return {"success": False, "error": "User not authenticated"}, 403

        if user.type == "admin" and request.args.get("all"):
            # Admins can fetch all logs
            logs = ActionLogs.query.order_by(ActionLogs.actionTime.desc()).all()
        else:
            # Normal users only see their logs
            logs = ActionLogs.query.filter_by(userId=user.id).order_by(ActionLogs.actionTime.desc()).all()

        response = [log.to_dict() for log in logs]
        return {"success": True, "data": response}, 200

    @action_logs_namespace.doc(
        description="Create a new action log",
        responses={200: ("Success", "ActionLogDetailedSuccessResponse")},
    )
    def post(self):
        """Log an action (Available for contestants)"""
        user = get_current_user()

        if not user:
            return {"success": False, "error": "User not authenticated"}, 403

        req_data = request.get_json()
        
        try:
            validated_data = ActionLogCreateSchema.parse_obj(req_data)  # Validate input
        except ValidationError as e:
            return {"success": False, "error": e.errors()}, 400  # Return validation errors

        log = ActionLogs(
            userId=user.id,
            actionTime=datetime.utcnow(),
            actionType=validated_data.actionType,
            actionDetail=validated_data.actionDetail
        )
        db.session.add(log)
        db.session.commit()

        return {"success": True, "data": log.to_dict()}, 200

@action_logs_namespace.route("/<int:log_id>")
class ActionLog(Resource):
    """Retrieve or delete specific action logs"""

    @action_logs_namespace.doc(
        description="Retrieve a specific action log (Only Admins or Owner)",
        responses={200: ("Success", "ActionLogDetailedSuccessResponse")},
    )
    def get(self, log_id):
        """Get details of a specific action log (Only if the user owns it or is an Admin)"""
        user = get_current_user()
        if not user:
            return {"success": False, "error": "User not authenticated"}, 403

        log = ActionLogs.query.filter_by(actionId=log_id).first_or_404()

        # Admins can see any log, users can see only their own logs
        if log.userId != user.id and user.type != "admin":
            return {"success": False, "error": "Permission denied"}, 403

        return {"success": True, "data": log.to_dict()}, 200

    @admins_only
    @action_logs_namespace.doc(
        description="Delete a specific action log (Admins only)",
        responses={200: ("Success", "APISimpleSuccessResponse")},
    )
    def delete(self, log_id):
        """Delete an action log (Admins only)"""
        log = ActionLogs.query.filter_by(actionId=log_id).first_or_404()
        db.session.delete(log)
        db.session.commit()

        return {"success": True}, 200

@action_logs_namespace.route("/user/<int:user_id>")
class UserActionLog(Resource):
    """Retrieve or delete action logs of a specific user"""

    @action_logs_namespace.doc(
        description="Retrieve all action logs of a specific User by Id",
        responses={200: ("Success", "ActionLogDetailedSuccessResponse")},
    )
    def get(self, user_id):
        """Get a list of action logs for a specific user (Only if the user owns them or is an Admin)"""
        user = get_current_user()
        if not user:
            return {"success": False, "error": "User not authenticated"}, 403

        # Retrieve all action logs for that user
        logs = ActionLogs.query.filter_by(userId=user_id).all()

        # Admins can see any logs, users can only see their own
        if user.type != "admin" and user.id != user_id:
            return {"success": False, "error": "Permission denied"}, 403

        # Convert logs to a list of dictionaries
        logs_data = [log.to_dict() for log in logs]

        return {"success": True, "data": logs_data}, 200
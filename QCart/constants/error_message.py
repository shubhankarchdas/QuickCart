from enum import Enum


class ErrorMessage(Enum):
    E00001 = "Invalid login credentials🧐."
    E00002 = "Invalid activation link🔗."
    E00003 = "Error sending email. Contact support."
    E00004 = "⚠️Passwords does not match. Please try again."
    E00005 = "Account with this email does not exist! Please try again."
    E00006 = "This link has expired. Please request a new password reset link."
    E00007 = "⚠️Please enter valid current password."
    

    

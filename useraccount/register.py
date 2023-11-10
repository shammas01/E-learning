from .models import User
from useraccount import views


def register_social_user(user_id, email, name):
    try:
        registered_user = User.objects.get(email=email)
        return {
            "username": registered_user.username,
            "email": registered_user.email,
            "tokens": views.get_tokens_for_user(registered_user),
        }
    except:
        user = {
            "username": name,
            "email": email,
        }
        
        try:
            user = User.objects.create_user(**user)
            user.save()

            return {
                "username": user.username,
                "email": user.email,
                "tokens": views.get_tokens_for_user(user),
            }
        except:
            return "Something Went Wrong..."

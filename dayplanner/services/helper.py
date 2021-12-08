def handle_message(request, context):
    if "Error_Message" in request.session:
        context["error"] = request.session["Error_Message"]
        del request.session["Error_Message"]
    elif "Success_Message" in request.session:
        context["message"] = request.session["Success_Message"]
        del request.session["Success_Message"]

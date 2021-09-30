def get_number(number):
    negative = False
    if "(" in number:
        number = number.replace("(", "").replace(")", "")
        negative = True
    number = number.replace(",", "").replace("%", "").replace("$", "")
    if negative:
        return -float(number)
    else:
        return float(number)
